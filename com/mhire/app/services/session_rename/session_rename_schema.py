# from pydantic import BaseModel, field_validator
# from datetime import datetime
# from typing import Optional
# import logging
# import logging.handlers
# from pathlib import Path
# from com.mhire.app.logger.logger import SessionRenameEndpoint

# logger = SessionRenameEndpoint.setup_session_rename_schema_logger()

# class SessionRenameRequest(BaseModel):
#     user_id: str
#     session_id: str
#     title: str
    
#     @field_validator('user_id', 'session_id', 'title')
#     @classmethod
#     def validate_not_empty(cls, v):
#         try:
#             if not v or not v.strip():
#                 error_msg = "user_id, session_id, and title cannot be empty"
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
#             logger.debug(f"SessionRenameRequest created for user_id: {self.user_id}, session_id: {self.session_id}")
#         except Exception as e:
#             error_msg = f"Failed to create SessionRenameRequest: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise


# class SessionRenameResponse(BaseModel):
#     success: bool
#     message: str
#     updated: bool
#     user_id: Optional[str] = None
#     session_id: Optional[str] = None
#     title: Optional[str] = None
#     auto_named: Optional[bool] = None
#     updated_at: Optional[datetime] = None
    
#     def __init__(self, **data):
#         try:
#             super().__init__(**data)
#             logger.debug(f"SessionRenameResponse created with success: {self.success}")
#         except Exception as e:
#             error_msg = f"Failed to create SessionRenameResponse: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise
