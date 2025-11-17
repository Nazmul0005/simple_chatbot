# import logging
# import logging.handlers
# from pathlib import Path
# from datetime import datetime
# from com.mhire.app.database.database_manager import db_manager
# from com.mhire.app.logger.logger import SessionRenameEndpoint

# logger = SessionRenameEndpoint.setup_session_rename_logger()

# async def update_session_title(user_id: str, session_id: str, title: str):
#     """Update session title in sessions collection"""
#     try:
#         logger.info(f"Updating session title for user_id: {user_id}, session_id: {session_id}")
#         timestamp = datetime.utcnow()
#         sessions_collection = db_manager.db["sessions"]
        
#         logger.debug(f"Searching for session with user_id: {user_id}, session_id: {session_id}")
#         existing_session = await sessions_collection.find_one({
#             "user_id": user_id,
#             "session_id": session_id
#         })
        
#         if not existing_session:
#             error_msg = f"Session not found for user_id: {user_id}, session_id: {session_id}"
#             logger.warning(error_msg)
#             return {
#                 "success": False,
#                 "message": error_msg,
#                 "updated": False
#             }
        
#         result = await sessions_collection.update_one(
#             {"user_id": user_id, "session_id": session_id},
#             {
#                 "$set": {
#                     "title": title,
#                     "auto_named": False,
#                     "updated_at": timestamp
#                 }
#             }
#         )
        
#         if result.modified_count > 0:
#             logger.info(f"Session title updated to '{title}' for user_id: {user_id}, session_id: {session_id}")
#             return {
#                 "success": True,
#                 "message": f"Session title updated to '{title}'",
#                 "updated": True,
#                 "user_id": user_id,
#                 "session_id": session_id,
#                 "title": title,
#                 "auto_named": False,
#                 "updated_at": timestamp
#             }
#         else:
#             logger.warning(f"No changes made for user_id: {user_id}, session_id: {session_id}")
#             return {
#                 "success": False,
#                 "message": "No changes made",
#                 "updated": False
#             }
            
#     except Exception as e:
#         error_msg = f"Failed to update session title for user_id: {user_id}, session_id: {session_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise Exception(error_msg) from e
