from .BaseController import BaseController
from models.db_schemes import Project , DataChunk
from helpers.config import Settings
from typing import List
from ..Stores.llm.LLMEnums import DocumentTypeEnums


class NLPController(BaseController):
    
    def __init__(self,VectorDB_client , Generation_client ,Embedding_Client):
        super().__init__()
        
        self.VectorDB_client = VectorDB_client
        self.Generation_client = Generation_client
        self.Embedding_Client = Embedding_Client
        
        
    def create_collection_name(self ,project_id :str):
        return f"Collection_{project_id}".strip()
        
    
    def reset_vector_db_collection(self ,project :Project ):
        
        collection_name =self.create_collection_name(project_id =project.project_id)
        return self.VectorDB_client.delete_collection(collection_name =collection_name)
    
    
    def get_vector_db_collection_info(self ,project :Project):
        
        collection_name =self.create_collection_name(project_id =project.project_id)
        collection_info = self.VectorDB_client.get_collection_info(collection_name =collection_name)
        return collection_info
    
    def index_into_vector_db(self ,project :Project, chunks : List[DataChunk],
                                                            do_reset :bool = False):
        """"
        #step1 :get collection name
        
        #step2 :manage items 
        
        #step3 : create collection if not exists
        
        #step4 : insert into vector database
        
        """
        
        collection_name =self.create_collection_name(project_id =project.project_id)
        
        texts =[ 
            
            i.chunk_text
            for i in chunks
        ]
        
        matedata =[
            i.chunk_metadata
            for i in chunks
        ]
        
        
        vectors= [
            
            self.Embedding_Client.embed_text(
                
                text = text,
                document_type = DocumentTypeEnums.Document.value
            )
            
            for text in texts

            
        ]
        
        
        _ =self.VectorDB_client.create_collection(
            collection_name = collection_name,
            embedding_size = Settings.EMBEDDING_MODEL_SIZE,
            do_reset = do_reset
        )
        
        
        _ = self.VectorDB_client.insert_many(
            
            collection_name =collection_name,
            texts = texts,
            vectors = vectors,
            metadata = matedata,
  
        )
        
        return True
        
        
        
        
        
    
    
    
    
    
        
        
        
        