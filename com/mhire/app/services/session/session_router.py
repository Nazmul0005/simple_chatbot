# from fastapi import APIRouter, HTTPException
# import logging
# import logging.handlers
# from pathlib import Path
# from datetime import datetime
# from com.mhire.app.services.session.session_schema import UserSessionsResponse, UserSessionRequest
# from com.mhire.app.services.session.session import get_user_sessions
# from com.mhire.app.logger.logger import SessionEndpoint




# logger = SessionEndpoint.setup_session_router_logger()

# router = APIRouter(prefix="/api/v1", tags=["Sessions"])

# @router.post("/session", response_model=UserSessionsResponse)
# async def get_sessions_endpoint(request: UserSessionRequest):
#     """
#     Get all sessions for a user
    
#     Parameters:
#     - request: JSON containing user_id and limit
#     """
#     try:
#         logger.info(f"Get sessions endpoint called for user_id: {request.user_id}, limit: {request.limit}")
#         # Convert limit from string to integer
#         limit = int(request.limit)
#         logger.debug(f"Converted limit to integer: {limit}")
#         result = await get_user_sessions(request.user_id, limit)
#         logger.info(f"Get sessions completed for user_id: {request.user_id}, retrieved {result['count']} sessions")
#         return result
#     except ValueError as e:
#         error_msg = f"Invalid limit value: {request.limit}"
#         logger.error(error_msg, exc_info=True)
#         raise HTTPException(status_code=400, detail=error_msg)
#     except Exception as e:
#         error_msg = f"Error retrieving sessions for user_id: {request.user_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise HTTPException(status_code=500, detail=error_msg)
