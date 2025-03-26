from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEunms import DataBaseEunms

class ProjectModel(BaseDataModel):
    
    def __init__(self,db_client:object):
        super().__init__(self ,db_client = db_client)
        self.collection = self.db_client[DataBaseEunms.COLLECTION_PROJECT_NAME.value]
        
        
    async def create_project(self,project = project):
        
        result = await self.collection.insert_one(project.dict())
        project._id = result.inserted_id
        return  project
    
    async def get_project_or_create_one(self,project_id : str):
        record =await self.collection.find_one({
            
            "project_id" : project_id,
 
        })
        
        if record is None :
            #create new project
            Project =  Project(
                project_id =project_id
            )
            
            Project =await self.create_project(Project = Project)
            
            return Project
        
        return Project(**record)
    
    
    async def get_all_projects(self ,page : int =1 ,page_size :int = 10 ):
        
        #count totle number of documents
        totle_documents =await self.collection.count_documents({})
        
        totle_pages = totle_documents // page_size
        if totle_documents % page_size > 0:
            totle_pages +=1
            
        
        cursor = self.collection.find().skip((page-1)*page_size).limit(page_size)
        
        projects =[]
        async for document in cursor:
            projects.append(
                Project(**document)
                )
         
         return projects , totle_pages
            
            
         