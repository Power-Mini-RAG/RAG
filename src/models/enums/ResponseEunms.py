from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATE_SUCCESS ="file_validate_success"
    FILE_TYPE_NOT_SUPPORTED ="file_type_not-supported"
    FILE_SIZE_EXCEEDED ="file_size_exceeded"
    FILE_UPLOADED_Success="file_uploaded_success"
    FILE_UPLOADED_FAILED = "file_uploaded_failed"