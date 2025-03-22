from fastapi import FastAPI, APIRouter
import os 

base_router = APIRouter(
    prefix ="/api/v1",
    tags =["api_v1"],
)

@base_router.get('/')
def welcome():
    App_name = os.getenv('APP_NAME')
    App_version = os.getenv('APP_VERSION')

    return {
        "App_name": App_name,
        "App_version": App_version,

    }