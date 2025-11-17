# import logging
# import logging.handlers
# from pathlib import Path
# from datetime import datetime
# from com.mhire.app.database.database_manager import db_manager
# from com.mhire.app.logger.logger import SessionEndpoint

# logger = SessionEndpoint.setup_session_logger()

# async def get_user_sessions(user_id: str, limit: int = 20):
#     """Get all sessions for a user with titles"""
#     try:
#         logger.info(f"Fetching sessions for user_id: {user_id}, limit: {limit}")
        
#         # Fetch conversations
#         cursor = db_manager.collection.find(
#             {"user_id": user_id},
#             {"session_id": 1, "created_at": 1, "updated_at": 1, "messages": {"$slice": 1}}
#         ).sort("updated_at", -1).limit(limit)
        
#         sessions = []
#         async for doc in cursor:
#             session_id = doc["session_id"]
            
#             # Fetch session title from sessions collection
#             session_doc = await db_manager.session_collection.find_one(
#                 {"user_id": user_id, "session_id": session_id},
#                 {"title": 1, "auto_named": 1}
#             )
            
#             session_info = {
#                 "session_id": session_id,
#                 "title": session_doc.get("title", "New Chat") if session_doc else "New Chat",
#                 "auto_named": session_doc.get("auto_named", True) if session_doc else True,
#                 "created_at": doc["created_at"],
#                 "updated_at": doc["updated_at"],
#                 "first_message": doc["messages"][0]["content"] if doc.get("messages") else ""
#             }
#             sessions.append(session_info)
#             logger.debug(f"Added session: {session_id} with title: {session_info['title']}")
        
#         logger.info(f"Successfully retrieved {len(sessions)} sessions for user_id: {user_id}")
#         return {
#             "user_id": user_id,
#             "sessions": sessions,
#             "count": len(sessions)
#         }
#     except Exception as e:
#         error_msg = f"Failed to fetch sessions for user_id: {user_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise Exception(error_msg) from e