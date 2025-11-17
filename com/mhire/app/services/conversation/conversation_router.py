# from fastapi import APIRouter, HTTPException
# import logging
# import logging.handlers
# from pathlib import Path
# from datetime import datetime

# from com.mhire.app.services.conversation.conversation_schema import LoadConversationRequest, ConversationResponse
# from com.mhire.app.services.conversation.conversation import get_conversation
# from com.mhire.app.logger.logger import ConversationEndpoint




# logger = ConversationEndpoint.setup_conversation_router_logger()

# router = APIRouter(prefix="/api/v1", tags=["Conversation"])

# @router.post("/conversation")
# async def load_conversation_endpoint(request: LoadConversationRequest):
#     """
#     Load all conversation messages for a specific user_id and session_id
    
#     Parameters:
#     - user_id: Unique identifier for the user
#     - session_id: Unique identifier for the conversation session
    
#     Returns: All messages in the conversation along with metadata
#     """
#     try:
#         logger.info(f"Load conversation endpoint called for user_id: {request.user_id}, session_id: {request.session_id}")
#         conversation_data = await get_conversation(request)
        
#         if conversation_data is None:
#             error_msg = f"No conversation found for user_id: {request.user_id} and session_id: {request.session_id}"
#             logger.warning(error_msg)
#             raise HTTPException(status_code=404, detail=error_msg)
        
#         logger.info(f"Load conversation completed for user_id: {request.user_id}, total_messages: {conversation_data.get('total_messages', 0)}")
#         return {
#             "success": True,
#             "data": conversation_data
#         }
    
#     except HTTPException:
#         raise
#     except Exception as e:
#         error_msg = f"Error loading conversation for user_id: {request.user_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise HTTPException(status_code=500, detail=error_msg)
