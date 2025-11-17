# from pydantic import BaseModel, field_validator
# from typing import List, Optional
# from datetime import datetime
# import logging
# import logging.handlers
# from pathlib import Path
# from com.mhire.app.logger.logger import ConversationEndpoint

# logger = ConversationEndpoint.setup_conversation_schema_logger()

# class LoadConversationRequest(BaseModel):
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
    
#     def __init__(self, **data):
#         try:
#             super().__init__(**data)
#             logger.debug(f"LoadConversationRequest created for user_id: {self.user_id}, session_id: {self.session_id}")
#         except Exception as e:
#             error_msg = f"Failed to create LoadConversationRequest: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise


# class Message(BaseModel):
#     role: str
#     content: str
#     timestamp: Optional[datetime] = None


# class ConversationResponse(BaseModel):
#     success: bool
#     data: dict
    
#     def __init__(self, **data):
#         try:
#             super().__init__(**data)
#             logger.debug(f"ConversationResponse created with success: {self.success}")
#         except Exception as e:
#             error_msg = f"Failed to create ConversationResponse: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise
