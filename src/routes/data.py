from fastapi import FastAPI, APIRouter ,Depends,UploadFile
import os 
from helpers.config import get_settings ,settings


base_router = APIRouter(
    prefix ="/api/v1/data",
    tags =["api_v1/","data"],
)

@base_router.post('/upload/{project_id}')
async def upload_data(project_id:str ,file : UploadFile,
                   app_settings:settings =Depends(get_settings)):

    
