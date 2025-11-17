# from pydantic import BaseModel, field_validator
# from typing import List
# from datetime import datetime
# import logging
# import logging.handlers
# from pathlib import Path
# from com.mhire.app.logger.logger import SessionEndpoint

# logger = SessionEndpoint.setup_session_schema_logger()

# class SessionInfo(BaseModel):
#     session_id: str
#     title: str
#     auto_named: bool
#     created_at: datetime
#     updated_at: datetime
#     first_message: str

# class UserSessionRequest(BaseModel):
#     user_id: str
#     limit: str
    
#     @field_validator('user_id')
#     @classmethod
#     def validate_user_id(cls, v):
#         try:
#             if not v or not v.strip():
#                 error_msg = "user_id cannot be empty"
#                 logger.error(error_msg)
#                 raise ValueError(error_msg)
#             logger.debug(f"Validated user_id: {v[:50]}...")
#             return v
#         except Exception as e:
#             error_msg = f"Validation error: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise
    
#     @field_validator('limit')
#     @classmethod
#     def validate_limit(cls, v):
#         try:
#             limit_int = int(v)
#             if limit_int <= 0:
#                 error_msg = "limit must be greater than 0"
#                 logger.error(error_msg)
#                 raise ValueError(error_msg)
#             logger.debug(f"Validated limit: {limit_int}")
#             return v
#         except ValueError as e:
#             error_msg = f"Invalid limit value: {v}"
#             logger.error(error_msg, exc_info=True)
#             raise

# class UserSessionsResponse(BaseModel):
#     user_id: str
#     sessions: List[SessionInfo]
#     count: int
    
#     def __init__(self, **data):
#         try:
#             super().__init__(**data)
#             logger.debug(f"UserSessionsResponse created for user_id: {self.user_id}, count: {self.count}")
#         except Exception as e:
#             error_msg = f"Failed to create UserSessionsResponse: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise