# from pydantic import BaseModel, field_validator
# from datetime import datetime
# import logging
# import logging.handlers
# from pathlib import Path
# from com.mhire.app.logger.logger import ChatStreamEndpoint

# logger = ChatStreamEndpoint.setup_stream_schema_logger()


# class ChatStreamRequest(BaseModel):
#     user_id: str
#     session_id: str
#     query: str
    
#     @field_validator('user_id', 'session_id', 'query')
#     @classmethod
#     def validate_not_empty(cls, v):
#         try:
#             if not v or not v.strip():
#                 error_msg = "user_id, session_id, and query cannot be empty"
#                 logger.error(error_msg)
#                 raise ValueError(error_msg)
#             logger.debug(f"Validated field: {v[:50]}...")
#             return v
#         except Exception as e:
#             error_msg = f"Validation error: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise
    
#     def __init__(self, **data):
#         try:
#             super().__init__(**data)
#             logger.debug(f"ChatStreamRequest created for user_id: {self.user_id}, session_id: {self.session_id}")
#         except Exception as e:
#             error_msg = f"Failed to create ChatStreamRequest: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise
