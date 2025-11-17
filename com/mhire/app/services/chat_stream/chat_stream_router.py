# from fastapi import APIRouter
# from fastapi.responses import StreamingResponse
# import logging
# import logging.handlers
# from pathlib import Path
# from datetime import datetime
# from com.mhire.app.services.chat_stream.chat_stream_schema import ChatStreamRequest
# from com.mhire.app.services.chat_stream.chat_stream import generate_stream
# from com.mhire.app.logger.logger import ChatStreamEndpoint

# logger = ChatStreamEndpoint.setup_stream_router_logger()

# router = APIRouter(prefix="/api/v1", tags=["Chat Stream"])

# @router.post("/chat_stream")
# async def chat_stream_endpoint(request: ChatStreamRequest):
#     """
#     Streaming chat endpoint that sends response chunks in real-time
    
#     Parameters:
#     - user_id: Unique identifier for the user
#     - session_id: Unique identifier for the conversation session
#     - query: User's current question/message
    
#     Returns: Server-Sent Events (SSE) stream
#     """
#     try:
#         logger.info(f"Chat stream endpoint called for user_id: {request.user_id}, session_id: {request.session_id}")
#         logger.debug(f"Query: {request.query}")
#         logger.info(f"Initiating streaming response for user_id: {request.user_id}")
        
#         return StreamingResponse(
#             generate_stream(request),
#             media_type="text/event-stream",
#             headers={
#                 "Cache-Control": "no-cache",
#                 "Connection": "keep-alive",
#                 "X-Accel-Buffering": "no"
#             }
#         )
#     except Exception as e:
#         error_msg = f"Error in chat stream endpoint for user_id: {request.user_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise
