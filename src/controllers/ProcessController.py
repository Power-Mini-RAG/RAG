from.BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader

class ProcessController(BaseController):
    
    def __init__(self , project_id :str):
        super().__init__()
        
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id)
    
    
    def get_file_extension(self, file_id :str):
        return os.path.splitext()[-1]
    
    
    def get_file_loader(self ,file_id :str):
        
        file_ext =self.get_file_extension(file_id)
        
        