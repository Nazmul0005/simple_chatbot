from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
# from com.mhire.app.database.database_manager import db_manager
# from com.mhire.app.services.chat_stream.chat_stream_router import router as chat_stream_router
# from com.mhire.app.services.chat.chat_router import router as chat_router
from com.mhire.app.services.ai_chat.ai_chat_router import router as ai_chat_router  # NEW
# from com.mhire.app.services.conversation.conversation_router import router as conversation_router
# from com.mhire.app.services.session_rename.session_rename_router import router as session_rename_router
# from com.mhire.app.services.history_get.history_get_router import router as history_get_router
# from com.mhire.app.services.history_delete.history_delete_router import router as history_delete_router
# from com.mhire.app.services.session.session_router import router as session_router

# Initialize FastAPI
app = FastAPI(title="Gemini Chatbot API")

# Global exception handler for 422 validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle all 422 validation errors globally with custom message"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Invalid request format. Please check your input and try again."
        }
    )


# Include routers
# app.include_router(chat_router)
app.include_router(ai_chat_router)  # NEW - No DB operations
# app.include_router(conversation_router)
# app.include_router(session_rename_router)
# app.include_router(history_delete_router)
# app.include_router(chat_stream_router)
# app.include_router(history_get_router)
# app.include_router(session_router)

# @app.on_event("startup")
# async def startup_db_client():
#     """Initialize database connection on startup"""
#     try:
#         await db_manager.test_connection()
#         await db_manager.setup_indexes()
#     except Exception as e:
#         print(f"Error connecting to MongoDB: {e}")

# @app.on_event("shutdown")
# async def shutdown_db_client():
#     """Close database connection on shutdown"""
#     db_manager.close()

@app.get("/")
async def root():
    return {
        "message": "Sora Chatbot API with Long-term Memory",
        "endpoints": {
            # "chat": "POST /api/v1/chat (non-streaming with DB)",
            "ai_chat": "POST /api/v1/ai-chat", 
            # "chat_stream": "POST /api/v1/chat_stream (streaming with SSE)",
            # "load_conversation": "POST /api/v1/conversation (load all messages for a session)",
            # "history": "GET /api/v1/history/{user_id}/{session_id}",
            # "sessions": "POST /api/v1/session (get user sessions)",
            # "delete_history": "DELETE /api/v1/history/delete (delete session history)",
            # "session_rename": "PUT /api/v1/session_rename (rename session title)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)