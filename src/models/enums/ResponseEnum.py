from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATE_SUCCESS ="file_validate_success"
    FILE_TYPE_NOT_SUPPORTED ="file_type_not-supported"
    FILE_SIZE_EXCEEDED ="file_size_exceeded"
    FILE_UPLOADED_Success="file_uploaded_success"
    FILE_UPLOADED_FAILED = "file_uploaded_failed"
    PROCESSING_SUCCESS ="processing_success"
    PROCESSING_FAILED ="processing_failed"
    NO_FILE_ERROR ="not found file"
    FILE_ID_ERROR ="not file found with this id "
    PROJECT_NOT_FOUND_ERROR ="project_not_found"
    INSERT_INTO_VECTORDB_ERROR ="insert_into_vectordb_error"
    INSERT_INTO_VECTORDB_SUCCESS ="insert_into_vectordb_success"
    VECTORDB_COLLECTION_RETRIVED ="vectordb_collection_retrived"
    VECTORDB_SEARCH_ERROR ="vectordb_search_error"
    VECTORDB_SEARCH_SUCCESS ="vectordb_search_success"
    
    