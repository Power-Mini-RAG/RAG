from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from Stores.llm.LLMProviderFactory import LLMProviderFactory

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    
    llm_Provider_Factory = LLMProviderFactory(
                config =settings
    )
    
    # generation Client 
    app.Generation_client = llm_Provider_Factory.create(
        provider = settings.GENERATION_BACKEND
    )
    
    app.Generation_client.set_generation_model(
        model_id = settings.GENERATION_MODEL_ID
    )
    
    # Embedding Client 
    app.Embedding_Client = llm_Provider_Factory.create(
        provider = settings.EMBEDDING_BACKEND
        
    )
    
    app.Embedding_Client.set_generation_model(
        model_id = settings.EMBEDDING_MODEL_ID,
        embedding_size = settings.EMBEDDING_MODEL_SIZE
        
    )
    
app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()


# app.router.lifespan.on_startup.append(startup_db_client)
# app.router.lifespan.on_shutdown.append(shutdown_db_client)

app.include_router(base.base_router)
app.include_router(data.data_router)