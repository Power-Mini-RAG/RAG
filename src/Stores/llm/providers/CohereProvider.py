from LLMInterface import LLMInterface
from LLMEnums import CohereEnums ,DocumentTypeEnums
import logging
import cohere 



class CohereProvider(LLMInterface):

    def __init__(self , api_key : str ,default_input_max_characters : int =1000 ,
                                      default_generation_max_output_tokens : int = 1000,
                                      default_generation_temperature : float =0.1):
        
        
        self.api_key = api_key
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature
        
        
        self.generation_model_id = None
        self.embedding_model_id  = None 
        self.embedding_size      = None
        
        
        self.client = cohere.ClientV2(
            
            api_key = self.api_key
        )
        
        
        self.logger = logging.getLogger(__name__)
        
        
        
    def set_generation_model(self , model_id :str ):
        self.generation_model_id  = model_id
        
    
    def set_embedding_model(self , model_id :str,  embedding_size :int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
        
    
    def process_text (self , text : str):
        return text[:self.default_input_max_characters].strip()
    
    
    def generation_text(self , prompt: str ,chat_history :list =[], max_output_tokens : int =None , 
                        temperature : float =None): 
              
        if not self.client:
            self.logger.error("cohere client was not set")
            return None
        
        if not self.generation_model_id:
            self.logger.error(" generation model id for cohere was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        
        temperature = temperature if temperature else self.default_generation_temperature
        
        
        response =self.client.chat(
            model =self.generation_model_id,
            chat_history =chat_history ,
            messages = self.process_text(prompt),
            max_tokens = max_output_tokens ,
            temperature = temperature
        )
        
        
        if not response or not response.message or len(response.message)==0 or not response.message.content[0]:
           self.logger.error("Error while generation text with cohere")
           return None
       
            
        return response.message.content[0].text
    
    
    
    def embed_text(self, text: str , document_type: str = None ):
        
        if not self.client:
            self.logger.error("Cohere client was not set")
            return None
    
        if not self.embedding_model_id:
            self.logger.error("Embedding model name for Cohere was not set")
            return None
        
        input_type =  CohereEnums.Document.value
        
        if document_type == DocumentTypeEnums.QUERY.value:
            input_type = CohereEnums.QUERY.value
        
        
        response = self.client.embed(
            
            model =self.generation_model_id,
            texts = [self.process_text(text)],
            input_type = input_type ,
            embedding_types=["float"]
            
        )
        
        if not response or not response.embeddings or len(response.embeddings) or not response.embeddings.float:
            self.logger.error("Error while embedding text with Cohere")
            return None
        
        return response.embeddings.float[0]


    def construct_prompt(self , prompt: str , role: str ):
        
        return {
            
            "role" : role ,
            "text" : self.process_text(prompt)     
            
            
        }
    

        
        