# from fastapi import APIRouter, HTTPException
# import logging
# import logging.handlers
# from pathlib import Path
# from datetime import datetime
# from com.mhire.app.services.history_get.history_get_schema import HistoryResponse
# from com.mhire.app.services.history_get.history_get import fetch_conversation_history
# from com.mhire.app.logger.logger import HistoryGetEndpoint

# logger = HistoryGetEndpoint.setup_history_get_router_logger()

# router = APIRouter(prefix="/api/v1/history", tags=["History"])

# @router.get("/{user_id}/{session_id}", response_model=HistoryResponse)
# async def get_conversation_history(user_id: str, session_id: str, limit: int = 50):
#     """
#     Retrieve conversation history for a user session
    
#     Parameters:
#     - user_id: Unique identifier for the user
#     - session_id: Unique identifier for the conversation session
#     - limit: Maximum number of messages to retrieve (default: 50)
#     """
#     try:
#         logger.info(f"Get history endpoint called for user_id: {user_id}, session_id: {session_id}, limit: {limit}")
#         result = await fetch_conversation_history(user_id, session_id, limit)
#         logger.info(f"Get history completed for user_id: {user_id}, retrieved {result['count']} messages")
#         return result
#     except Exception as e:
#         error_msg = f"Error retrieving history for user_id: {user_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise HTTPException(status_code=500, detail=error_msg)
