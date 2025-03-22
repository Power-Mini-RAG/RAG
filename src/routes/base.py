from fastapi import FastAPI, APIRouter
from helpers.config import get_settings
import os 

base_router = APIRouter(
    prefix ="/api/v1",
    tags =["api_v1"],
)

@base_router.get('/')
async def welcome():
    app_settings = get_settings
    App_name = app_settings.APP_NAME
    App_version = app_settings.APP_VERSION

    return {
        "App_name": App_name,
        "App_version": App_version,

    }