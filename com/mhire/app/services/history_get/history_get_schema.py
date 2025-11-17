# from pydantic import BaseModel, field_validator
# from typing import List
# from datetime import datetime
# import logging
# import logging.handlers
# from pathlib import Path
# from com.mhire.app.logger.logger import HistoryGetEndpoint

# logger = HistoryGetEndpoint.setup_history_get_schema_logger()


# class HistoryResponse(BaseModel):
#     user_id: str
#     session_id: str
#     history: List[dict]
#     count: int
    
#     def __init__(self, **data):
#         try:
#             super().__init__(**data)
#             logger.debug(f"HistoryResponse created for user_id: {self.user_id}, session_id: {self.session_id}, count: {self.count}")
#         except Exception as e:
#             error_msg = f"Failed to create HistoryResponse: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise
