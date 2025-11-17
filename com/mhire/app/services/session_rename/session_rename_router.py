# from fastapi import APIRouter, HTTPException
# import logging
# import logging.handlers
# from pathlib import Path
# from datetime import datetime
# from com.mhire.app.services.session_rename.session_rename_schema import SessionRenameRequest, SessionRenameResponse
# from com.mhire.app.services.session_rename.session_rename import update_session_title
# from com.mhire.app.logger.logger import SessionRenameEndpoint

# logger = SessionRenameEndpoint.setup_session_rename_router_logger()

# router = APIRouter(prefix="/api/v1", tags=["Session Rename"])

# @router.put("/session_rename", response_model=SessionRenameResponse)
# async def rename_session_endpoint(request: SessionRenameRequest):
#     """
#     Rename/update session title
    
#     Parameters:
#     - user_id: Unique identifier for the user
#     - session_id: Unique identifier for the conversation session
#     - title: New title for the session
#     """
#     try:
#         logger.info(f"Rename session endpoint called for user_id: {request.user_id}, session_id: {request.session_id}")
#         logger.debug(f"New title: {request.title}")
        
#         result = await update_session_title(request.user_id, request.session_id, request.title)
        
#         if result["success"]:
#             logger.info(f"Session renamed successfully for user_id: {request.user_id}")
#             return SessionRenameResponse(
#                 success=result["success"],
#                 message=result["message"],
#                 updated=result["updated"],
#                 user_id=result.get("user_id"),
#                 session_id=result.get("session_id"),
#                 title=result.get("title"),
#                 auto_named=result.get("auto_named"),
#                 updated_at=result.get("updated_at")
#             )
#         else:
#             logger.warning(f"Session rename failed for user_id: {request.user_id}: {result['message']}")
#             raise HTTPException(status_code=404, detail=result["message"])
            
#     except HTTPException:
#         raise
#     except Exception as e:
#         error_msg = f"Error renaming session for user_id: {request.user_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise HTTPException(status_code=500, detail=error_msg)
