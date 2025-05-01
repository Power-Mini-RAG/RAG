from enum import Enum

class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    OLLAMA = "OLLAMA"
    
    
class OpenAIEnums(Enum):
    SYSTEM    = "system"
    USER      =  "user"
    ASSASTANT ="assastant"
    


class CohereEnums(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT ="CHATBOT"
    
    Document ="search_document"
    QUERY  ="search_query"
    

class OllamaEnums(Enum):
    SYSTEM    = "system"
    USER      =  "user"
    ASSASTANT ="assastant"
    
    

class DocumentTypeEnum(Enum):
    Document ="document"
    QUERY    = "query"
    