from fastapi import FastAPI, APIRouter ,Depends,UploadFile,status,Request
from fastapi.responses import JSONResponse
import os 
from helpers.config import get_settings ,settings
from  controllers import DataController ,ProjectController,ProcessController
import aiofiles
from models import ResponseSignal
import logging
from.Schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel

logger =logging.getLogger('uvcorn.error')

data_router = APIRouter(
    prefix ="/api/v1/data",
    tags =["api_v1/","data"],
)

@data_router.post('/upload/{project_id}')
async def upload_data(Request : Request ,project_id:str ,file : UploadFile,
                   app_settings:settings =Depends(get_settings)):

    project_model = ProjectModel(
        db_client = Request.app.db_client
        
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
                    "Signal" : result_signal
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
                "Signal" : ResponseSignal.FILE_UPLOADED_FAILED.value
            },
        )


    return JSONResponse(
                content ={
                    "Signal" : ResponseSignal.FILE_UPLOADED_Success.value,
                    "file_id" :file_id,
                    "project_id": str(project._id)

                }
        )
    

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, process_request: ProcessRequest):

    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size

    process_controller = ProcessController(project_id=project_id)

    file_content = process_controller.get_file_content(file_id=file_id)

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

    return file_chunks
        
        
  
    
    
    
    

   
