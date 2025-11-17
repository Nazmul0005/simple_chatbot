from fastapi import APIRouter, HTTPException
from com.mhire.app.services.ai_chat.ai_chat import process_ai_chat
from com.mhire.app.services.ai_chat.ai_chat_schema import AIChatRequest, AIChatResponse
from com.mhire.app.logger.logger import ChatEndpoint

logger = ChatEndpoint.setup_router_logger()

router = APIRouter(prefix="/api/v1", tags=["AI_Chat"])

@router.post("/ai_chat", response_model=AIChatResponse)
async def ai_chat_endpoint(request: AIChatRequest):
    """
    AI Chat endpoint that processes user query with provided conversation history
    
    Parameters:
    - user_id: Unique identifier for the user
    - session_id: Unique identifier for the conversation session
    - query: User's current question/message
    - history: Last 10 messages from conversation (optional, max 10 messages)
    
    Returns:
    - query: The user's query
    - response: AI generated response
    - timestamp: When the response was generated
    
    Note: This endpoint does NOT perform any database operations.
    History must be provided in the request.
    """
    try:
        logger.info(f"AI chat endpoint called for user_id: {request.user_id}, session_id: {request.session_id}")
        logger.debug(f"Query: {request.query}")
        logger.debug(f"History length: {len(request.history)}")
        
        result = await process_ai_chat(request)
        
        logger.info(f"AI chat endpoint completed successfully for user_id: {request.user_id}")
        return result
    except Exception as e:
        error_str = str(e)
        logger.error(f"Error processing AI chat for user_id: {request.user_id}: {error_str}", exc_info=True)
        
        # Custom error messages for specific errors
        if "API_KEY_INVALID" in error_str or "API key not valid" in error_str:
            raise HTTPException(
                status_code=500, 
                detail="AI service configuration error. Please contact support."
            )
        elif "quota" in error_str.lower() or "rate limit" in error_str.lower():
            raise HTTPException(
                status_code=429, 
                detail="Service temporarily unavailable. Please try again later."
            )
        elif "timeout" in error_str.lower():
            raise HTTPException(
                status_code=504, 
                detail="Request timeout. Please try again."
            )
        else:
            # Generic error for unknown issues
            raise HTTPException(
                status_code=500, 
                detail="Unable to process your request. Please try again later."
            )