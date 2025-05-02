from fastapi import FastAPI, APIRouter ,Depends,UploadFile,status,Request
from fastapi.responses import JSONResponse
import os 
from helpers.config import get_settings ,Settings
from controllers import DataController ,ProjectController,ProcessController
import aiofiles
from models import ResponseSignal
from models.enums.AssetTypeEnum import AssetTypeEnum
import logging
from.Schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
from models.db_schemes import DataChunk ,Asset
import json
from controllers import NLPController



logger =logging.getLogger('uvcorn.error')

data_router = APIRouter(
    prefix ="/api/v1/data",
    tags =["api_v1","data"],
)

@data_router.post('/upload/{project_id}')
async def upload_data(request : Request ,project_id:int ,file : UploadFile,
                   app_settings:Settings =Depends(get_settings)):

    project_model = await ProjectModel.create_instance( 
        db_client = request.app.db_client
        
    )
    
    project =await project_model.get_project_or_create_one(
        project_id = project_id
    )
    
    
    data_controller = DataController()
    # validate the file properties
    is_valid, result_signal = data_controller.validate_uploaded_file(file =file)

    if not is_valid :
        return JSONResponse(
                status_code =status.HTTP_400_BAD_REQUEST,
                content ={
                    "signal" : result_signal
                },
        )


    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path,file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )
       
    try:
        async with aiofiles.open(file_path,"wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)

    except Exception as e :
        logger.error(f"Error while uploding file : {e}")
        return JSONResponse(
            status_code =status.HTTP_400_BAD_REQUEST,
            content ={
                "signal" : ResponseSignal.FILE_UPLOADED_FAILED.value
            },
        )

    asset_model = await AssetModel.create_instance( 
        db_client = request.app.db_client
        
        )
    
    asset_resource = Asset(
        asset_project_id = project.project_id,
        asset_type = AssetTypeEnum.FILE.value,
        asset_name = file_id ,
        asset_size = os.path.getsize(file_path)
    
       )
    
    
    asset_record =await asset_model.create_asset(
        asset = asset_resource
    )
       
    return JSONResponse(
                content ={
                    "signal" : ResponseSignal.FILE_UPLOADED_Success.value,
                    "file_id" : str(asset_record.asset_id)
                    
                }
        )
    
@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: int, process_request: ProcessRequest):

    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    nlp_controller = NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
        template_parser=request.app.template_parser,
    )

    asset_model = await AssetModel.create_instance(
            db_client=request.app.db_client
        )

    project_files_ids = {}
    if process_request.file_id:
        asset_record = await asset_model.get_asset_record(
            asset_project_id=project.project_id,
            asset_name=process_request.file_id
        )

        if asset_record is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.FILE_ID_ERROR.value,
                }
            )

        project_files_ids = {
            asset_record.asset_id: asset_record.asset_name
        }
    
    else:
        

        project_files = await asset_model.get_all_project_assets(
            asset_project_id=project.project_id,
            asset_type=AssetTypeEnum.FILE.value,
        )

        project_files_ids = {
            record.asset_id: record.asset_name
            for record in project_files
        }

    if len(project_files_ids) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.NO_FILES_ERROR.value,
            }
        )
    
    process_controller = ProcessController(project_id=project_id)

    no_records = 0
    no_files = 0

    chunk_model = await ChunkModel.create_instance(
                        db_client=request.app.db_client
                    )

    if do_reset == 1:
        # delete associated vectors collection
        collection_name = nlp_controller.create_collection_name(project_id=project.project_id)
        _ = await request.app.vectordb_client.delete_collection(collection_name=collection_name)

        # delete associated chunks
        _ = await chunk_model.delete_chunks_by_project_id(
            project_id=project.project_id
        )
    

    for asset_id, file_id in project_files_ids.items():
    
        file_content = process_controller.get_file_content(file_id=file_id)

        if file_content is None:
            logger.error(f"Error while processing file: {file_id}")
            continue

        file_chunks = process_controller.process_file_content(
            file_content=file_content,
            file_id=file_id,
            chunk_size=chunk_size,
            overlap_size=overlap_size
        )

        if file_chunks is None or len(file_chunks) == 0:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.PROCESSING_FAILED.value
                }
            )

        file_chunks_records = [
            DataChunk(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i+1,
                chunk_project_id=project.project_id,
                chunk_asset_id=asset_id
            )
            for i, chunk in enumerate(file_chunks)
        ]

        no_records += await chunk_model.insert_many_chunks(chunks=file_chunks_records)
        no_files += 1

    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_records,
            "processed_files": no_files
        }
    )
# @data_router.post("/process/{project_id}")
# async def process_endpoint(request : Request ,project_id: int, process_request: ProcessRequest):
    
#     chunk_size = process_request.chunk_size
#     overlap_size = process_request.overlap_size
#     do_reset = process_request.do_reset
    
    
#     project_model =await ProjectModel.create_instance( 
#         db_client = request.app.db_client
        
#     )
    
#     project =await project_model.get_project_or_create_one(
#         project_id = project_id
#     )
    
#     nlp_controller = NLPController(
#         vectordb_client = request.app.vectordb_client,
#         generation_client = request.app.generation_client,
#         embedding_client = request.app.embedding_client,
#         template_parser = request.app.template_parser
        
#                     )
    
#     asset_model = await AssetModel.create_instance( 
#             db_client = request.app.db_client
        
#             )
    
#     project_file_ids = {}
#     if process_request.file_id:
#         asset_record = await asset_model.get_asset_record(
#             asset_project_id = project.project_id,
#             asset_name = process_request.file_id
            
#         )
#         if asset_record is None:
#              return  JSONResponse(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 content={
                
#                         "signal": ResponseSignal.FILE_ID_ERROR.value ,
   
#                         }
#                     ) 
        
    
            
#         project_file_ids = {
#              asset_record.asset_id : asset_record.asset_name
            
#         }
        
#     else: 
       
#         project_files = await asset_model.get_all_project_assets(
#             asset_project_id = project.project_id,
#             asset_type = AssetTypeEnum.FILE.value

#          )
#         project_file_ids ={
#             record.asset_id : record.asset_name
#             for record in project_files
#         }
        
    
    
#     if len(project_file_ids) ==0:
#         return  JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             content={
                
#                 "signal": ResponseSignal.NO_FILE_ERROR.value ,
   
#                  }
#             ) 
        
    
#     process_controller = ProcessController(project_id=project_id)
    
#     no_records =0
#     no_file  =0
   
#     chunk_model =await ChunkModel.create_instance( 
#             db_client = request.app.db_client
            
#         )
        
#     if do_reset == 1:
#         collection_name = nlp_controller.create_collection_name(project_id = project.project_id)
        
#         # delete the Embedding for this collection name 
#         delete_embedding =  await request.app.vectordb_client.delete_collection(
#             collection_name = collection_name)
        
#         if delete_embedding:
#             print(f"Delete embedding {collection_name} in endpoint process")
#         else:
#             print(f"dont Delete embedding {collection_name} in endpoint process")
            
#         # delete the chunk text for this collection name
#         delete_chunk = await chunk_model.delete_chunks_by_project_id(
#             project_id = project.project_id
#             )
        
#         if delete_chunk:
#             print(f"Delete chunk { project.project_id} in endpoint process")
#         else:
#             print(f"dont Delete chunk { project.project_id} in endpoint process")
            
        
    
#     for asset_id ,file_id in project_file_ids.items():

#         file_content = process_controller.get_file_content(file_id=file_id)

#         if file_content is None:
#             logger.error(f"Error while processing file {file_id}")
#             continue
            

#         file_chunks = process_controller.process_file_content(
            
#             file_content=file_content,
#             file_id=file_id,
#             chunk_size=chunk_size,
#             overlap_size=overlap_size
#         )
        
        

#         if file_chunks is None or len(file_chunks) == 0:
#             return JSONResponse(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 content={
#                     "signal": ResponseSignal.PROCESSING_FAILED.value
#                 }
#             )

#         file_chunk_records =[
            
#             DataChunk(
                
#                 chunk_text=chunk.page_content,
#                 chunk_metadata=chunk.metadata,
#                 chunk_order = i+1,
#                 chunk_project_id= project.project_id,
#                 chunk_asset_id = asset_id
#             )
#             for i , chunk in enumerate(file_chunks)
            
#         ]
        
        
#         no_records +=await chunk_model.insert_many_chunks(
#                                                 chunks = file_chunk_records
        
#                                         )
        
#         no_file +=1
        
#     return  JSONResponse(
#             content={
#                 "signal": ResponseSignal.PROCESSING_SUCCESS.value ,
#                 "inserted_chunks":no_records,
#                 "Processed_file" : no_file
#                 }
#             )
    
    
    
        
        
  
    
    
    
    

   
