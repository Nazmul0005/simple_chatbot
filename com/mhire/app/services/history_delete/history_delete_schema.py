# from pydantic import BaseModel, field_validator
# from datetime import datetime
# import logging
# import logging.handlers
# from pathlib import Path
# from com.mhire.app.logger.logger import HistoryDeleteEndpoint



# logger = HistoryDeleteEndpoint.setup_history_delete_schema_logger()


# class DeleteHistoryResponse(BaseModel):
#     message: str
#     deleted: bool
#     conversation_deleted: bool
#     session_deleted: bool
    


# class DeleteHistoryRequest(BaseModel):
#     user_id: str
#     session_id: str
    
#     @field_validator('user_id', 'session_id')
#     @classmethod
#     def validate_not_empty(cls, v):
#         try:
#             if not v or not v.strip():
#                 error_msg = "user_id and session_id cannot be empty"
#                 logger.error(error_msg)
#                 raise ValueError(error_msg)
#             logger.debug(f"Validated field: {v[:50]}...")
#             return v
#         except Exception as e:
#             error_msg = f"Validation error: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise
