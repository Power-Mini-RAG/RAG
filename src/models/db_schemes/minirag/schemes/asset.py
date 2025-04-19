from .minirag_base import SQLAlchemy_Base
from sqlalchemy import column ,Integer,DateTime,func ,String,ForeignKey
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Index
import uuid


class Asset(SQLAlchemy_Base):
    
    __tablename__ ="assets"
     
     
    asset_id  = column(Integer ,primary_key = True,autoincerment =True)
    asset_uuid =column(UUID(as_uuid=True),default =uuid.uuid4,unique =True, nullable =False)
    
    asset_type =column(String,nullable =False)
    asset_name =column(String,nullable =False)
    asset_size = column(Integer,nullable =False)
    asset_config =column(JSONB,nullable =True)
    
    # This is foreign_key
    asset_project_id = column(Integer,ForeignKey("projects.project_id"),nullable =False)
    
    created_at =column(DateTime(timezone=True),server_default =func.now(),nullable =False)
    updated_at =column(DateTime(timezone=True),onupdate = func.now(), nullable =True)
    
    project =relationship("Project",back_populates="assets")
    
    # create index for two tables foreign_key and type
    __table_args__ =(
        Index("ix_asset_project_id",asset_project_id),
        Index("ix_asset_type",asset_type),
    )
      
     
