from .minirag_base import SQLAlchemy_Base
from sqlalchemy import column ,Integer,DateTime,func
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Project(SQLAlchemy_Base):
    
    __tablename__ ="projects"
    
    project_id  = column(Integer ,primary_key = True,autoincerment =True)
    project_uuid =column(UUID(as_uuid=True),default =uuid.uuid4,unique =True, nullable =False)
    
    created_at =column(DateTime(timezone=True),server_default =func.now(),nullable =False)
    updated_at =column(DateTime(timezone=True),onupdate = func.now(), nullable =True)