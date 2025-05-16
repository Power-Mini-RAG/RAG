APP_NAME="mini-RAG"
APP_VERSION="0.1"
OPENAI_API_KEY="ollama"

#======================upload congig=============================
FILE_ALLOWED_TYPES=["text/plain","application/pdf"]
FILE_MAX_SIZE=10
FILE_DEFAULT_CHUNK_SIZE= 512000 # 512KB
#===========================database config =======================
POSTGRES_USER=postgres
POSTGRES_PASSWORD="postgres_password"
POSTGRES_HOST= "pgvector"
POSTGRES_PORT="5432"
POSTGRES_MAIN_DATABASE="minirag"
#=======================llm config =================================
GENERATION_BACKEND_LITERAL=["OPENAI","COHERE","OLLAMA"]
GENERATION_BACKEND="OLLAMA"
EMBEDDING_BACKEND="OLLAMA"


OPENAI_API_URL=  "https://adf7-34-127-31-112.ngrok-free.app/v1"
EMBEDDING_API_URL= "https://4232-34-127-31-112.ngrok-free.app/v1"

COHERE_API_KEY="K7n2choLxcGFp7bPHHOwO3d8ZH"

GENERATION_MODEL_ID="gemma2:9b-instruct-q5_0"
EMBEDDING_MODEL_ID= "paraphrase-multilingual"        
EMBEDDING_MODEL_SIZE= 768


DEFAULT_INPUT_MAX_CHARACTERS= 1000
DEFAULT_GENERATION_MAX_OUTPUT_TOKENS= 1000
DEFAULT_GENERATION_TEMPERATURE= 0.1


#========================vector database ===========================
VECTOR_DB_BACKEND_LITERAL=["pgvector" ,"qdrant"]
VECTOR_DB_BACKEND="pgvector"
VECTOR_DB_PATH= "qdrant_db"
VECTOR_DB_DISTANCE_METHOD="COSINE"
VECTOR_DB_PGVEC_INDEX_THRESHOLD= 1000

#=======================templates configs=====================================
PRIMARY_LANG="ar"
DEFAULT_LANG="en"



