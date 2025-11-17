from pydantic import BaseModel, field_validator
from typing import List, Dict, Optional
from datetime import datetime
from com.mhire.app.logger.logger import ChatEndpoint

logger = ChatEndpoint.setup_schema_logger()

class MessageHistory(BaseModel):
    role: str
    content: str
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        if v not in ['user', 'assistant']:
            error_msg = "Role must be either 'user' or 'assistant'"
            logger.error(error_msg)
            raise ValueError(error_msg)
        return v

class AIChatRequest(BaseModel):
    user_id: str
    session_id: str
    query: str
    history: Optional[List[MessageHistory]] = []
    
    @field_validator('user_id', 'session_id', 'query')
    @classmethod
    def validate_not_empty(cls, v):
        try:
            if not v or not v.strip():
                error_msg = "user_id, session_id, and query cannot be empty"
                logger.error(error_msg)
                raise ValueError(error_msg)
            logger.debug(f"Validated field: {v[:50]}...")
            return v
        except Exception as e:
            error_msg = f"Validation error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise
    
    @field_validator('history')
    @classmethod
    def validate_history_length(cls, v):
        if len(v) > 10:
            logger.warning(f"History has {len(v)} messages, truncating to last 10")
            return v[-10:]
        return v

class AIChatResponse(BaseModel):
    query: str
    response: str
    timestamp: datetime
    
    def __init__(self, **data):
        try:
            super().__init__(**data)
            logger.debug(f"AIChatResponse created for query: {self.query[:50]}...")
        except Exception as e:
            error_msg = f"Failed to create AIChatResponse: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise