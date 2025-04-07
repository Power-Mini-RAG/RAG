from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from Stores.llm.LLMProviderFactory import LLMProviderFactory
from Stores.Vectordb.VectorDBProviderFactory import VectorDBProviderFactory

app = FastAPI()

@app.on_event("startup")
async def startup_span():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    
    llm_Provider_Factory = LLMProviderFactory(config =settings)
    Vector_provider_factory = VectorDBProviderFactory(config =settings)
    
    # generation Client 
    app.Generation_client = llm_Provider_Factory.create(provider = settings.GENERATION_BACKEND)
    
    app.Generation_client.set_generation_model(model_id = settings.GENERATION_MODEL_ID)
    
    # Embedding Client 
    app.Embedding_Client = llm_Provider_Factory.create(provider = settings.EMBEDDING_BACKEND)
    
    app.Embedding_Client.set_generation_model(
        model_id = settings.EMBEDDING_MODEL_ID,
        embedding_size = settings.EMBEDDING_MODEL_SIZE
        
    )
    
    app.VectorDB_client = Vector_provider_factory.create(provider =settings.VECTOR_DB_BACKEND )
    
    app.VectorDB_client.connect()
    
@app.on_event("shutdown")
async def shutdown_span():
    app.mongo_conn.close()
    app.VectorDB_client.disconnect()


# app.router.lifespan.on_startup.append(startup_span)
# app.router.lifespan.on_shutdown.append(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)