from .minirag_base import SQLAlchemy_Base
from sqlalchemy import column ,Integer,DateTime,func ,String,ForeignKey
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Index
from pydantic import BaseModel
import uuid


class DataChunk(SQLAlchemy_Base):
    
    __tablename__ ="chunks"
    
    chunk_id  = column(Integer ,primary_key = True,autoincerment =True)
    chunk_uuid =column(UUID(as_uuid=True),default =uuid.uuid4,unique =True, nullable =False)
    
    
    chunk_text = column(String ,nullable =False)
    chunk_metadata = column(JSONB,nullable =True)
    chunk_order = column(Integer,nullable =False)
    
    chunk_project_id = column(Integer,ForeignKey("projects.project_id"),nullable =False)
    chunk_asset_id =column(Integer,ForeignKey("assets.asset_id"),nullable =False)
    
    created_at =column(DateTime(timezone=True),server_default =func.now(),nullable =False)
    updated_at =column(DateTime(timezone=True),onupdate = func.now(), nullable =True)
    
    project =relationship("Project",back_populates="chunks")
    asset   =relationship("Asset",back_populates="chunks")
    
    
    # create index for two tables foreign_key and type
    __table_args__ =(
        Index("ix_chunk_project_id",chunk_project_id),
        Index("ix_chunk_asset_id",chunk_asset_id),
    )


class RetrievedDocument(BaseModel):
    text: str
    score: float
    
    