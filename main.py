from fastapi import FastAPI
from routes import base


app =FastAPI()

app.inculde_router(base.base_router)