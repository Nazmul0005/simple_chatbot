# from fastapi import APIRouter, HTTPException
# import logging
# import logging.handlers
# from pathlib import Path
# from datetime import datetime
# from com.mhire.app.services.history_delete.history_delete_schema import DeleteHistoryResponse, DeleteHistoryRequest
# from com.mhire.app.services.history_delete.history_delete import delete_session
# from com.mhire.app.logger.logger import HistoryDeleteEndpoint




# logger = HistoryDeleteEndpoint.setup_history_delete_router_logger()

# router = APIRouter(prefix="/api/v1/history", tags=["History"])

# @router.delete("/delete", response_model=DeleteHistoryResponse)
# async def delete_session_history(request: DeleteHistoryRequest):
#     """
#     Delete all conversation history for a specific session
    
#     Parameters:
#     - user_id: Unique identifier for the user
#     - session_id: Unique identifier for the conversation session
#     """
#     try:
#         logger.info(f"Delete history endpoint called for user_id: {request.user_id}, session_id: {request.session_id}")
#         result = await delete_session(request.user_id, request.session_id)
#         logger.info(f"Delete history completed for user_id: {request.user_id}")
#         return result
#     except Exception as e:
#         error_msg = f"Error deleting history for user_id: {request.user_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise HTTPException(status_code=500, detail=error_msg)
