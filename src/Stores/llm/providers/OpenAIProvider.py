from LLMInterface import LLMInterface
from openai import OpenAI 
import logging

class OpenAIProvider(LLMInterface):
    
    def __init__(self , api_key : str , api_url : str =None , 
                                      default_input_max_characters : int =1000 ,
                                      default_generation_max_output_tokens : int = 1000,
                                      default_generation_temperature : float =0.1):
        
        
        self.api_key = api_key
        self.api_url = api_url
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature
        
        self.generation_model_id = None
        
        self.embedding_model_id  = None 
        self.embedding_size      = None
        
        
        self.client = OpenAI(
            api_key = self.api_key,
            api_url =self.api_url
            
        )
        
        self.logger = logging.getLogger(__name__)
        
        
        
    def set_generation_model(self , model_id :str ):
        self.generation_model_id  = model_id
        
    
    def set_embedding_model(self , model_id :str,  embedding_size :int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
    
    
    def generation_text(self , prompt: str ,max_output_tokens : int = None , 
                        temperature : float =None): 
              
        if not self.client:
            self.logger.error("openai client was not set")
            return None
        
        if not self.generation_model_id:
            self.logger.error(" generation model id for openai was not set")
            return None
        
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        
        temperature = temperature if temperature else self.default_generation_temperature
        
        
        pass
        
    
    
    
    def embed_text(self, text: str , document_type: str ):
        
        if not self.client:
            self.logger.error("openai client was not set")
            return None
    
        if not self.embedding_model_id:
            self.logger.error("Embedding model name  for openai was not set")
            return None
        
        
        response = self.client.embeddings.create(
            
            model = self.embedding_model_id,
            input = text
        )
        
        if not response or response.data or len(response.data)== 0 or not response.data[0].embedding:
            self.logger.error("Error while embedding text with openai")
            return None
        
        
        return response.data[0].embedding
        
    
        
        
    


