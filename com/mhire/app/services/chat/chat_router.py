# from fastapi import APIRouter, HTTPException
# from com.mhire.app.services.chat.chat import process_chat
# from com.mhire.app.services.chat.chat_schema import ChatRequest, ChatResponse
# from com.mhire.app.logger.logger import ChatEndpoint

# logger = ChatEndpoint.setup_router_logger()

# router = APIRouter(prefix="/api/v1", tags=["Chat"])

# @router.post("/chat", response_model=ChatResponse)
# async def chat_endpoint(request: ChatRequest):
#     """
#     Chat endpoint that processes user query with conversation history
    
#     Parameters:
#     - user_id: Unique identifier for the user
#     - session_id: Unique identifier for the conversation session
#     - query: User's current question/message
    
#     The endpoint automatically fetches the last 10 messages from the database
#     """
#     try:
#         logger.info(f"Chat endpoint called for user_id: {request.user_id}, session_id: {request.session_id}")
#         logger.debug(f"Query: {request.query}")
#         result = await process_chat(request)
#         logger.info(f"Chat endpoint completed successfully for user_id: {request.user_id}")
#         return result
#     except Exception as e:
#         error_msg = f"Error processing chat for user_id: {request.user_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise HTTPException(status_code=500, detail=error_msg)
