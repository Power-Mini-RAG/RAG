from .BaseController import BaseController
from models.db_schemes import Project , DataChunk
from helpers.config import Settings
from typing import List
from Stores.llm.LLMEnums import DocumentTypeEnums
import json


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
        
        return json.loads(
            
            json.dumps(collection_info,default=lambda X: X.__dict__)
        )
    
    def index_into_vector_db(self ,project :Project, chunks : List[DataChunk],
                                                          chunks_ids: List[int] ,do_reset :bool = False):
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
            embedding_size = self.Embedding_Client.embedding_size,
            do_reset = do_reset
        )
        
        
        _ = self.VectorDB_client.insert_many(
            
            collection_name =collection_name,
            texts = texts,
            vectors = vectors,
            metadata = matedata,
            chunks_ids = chunks_ids,
            
  
        )
        
        return True
    
    
    def search_vector_db_collection(self ,project :Project,text : str ,limit:int =10):
        
        """
        step_1 : get collection name 
        step_2 : get text embedding vector
        step_3 : do semantic search  
        
        """
        
        collection_name =self.create_collection_name(project_id =project.project_id)
        
        vector = self.Embedding_Client.embed_text(
            text = text ,
            document_type = DocumentTypeEnums.QUERY.value
        )
        
        if not vector or len(vector) ==0:
            return False
        
        results =self.VectorDB_client.search_by_vector(
            
            collection_name = collection_name ,
            vector = vector ,
            limit = limit
        )
        
        
        if not results :
            return False
        
        return results
    
    def answer_rag_quesion(self ,project :Project, Query : str ,limit:int =10):
        
        """
        step_1 : retrieve related documents
        step_2 : construct LLm prompt
        
        """
        
        retrieved_documents =self.search_vector_db_collection(
            project =project,
            text = Query , 
            limit =limit
            
            )
        
        if not retrieved_documents or len(retrieved_documents) ==0:
            return None
    
        
        
        
        
        
        
        
    
    
    
    
    
        
        
        
        