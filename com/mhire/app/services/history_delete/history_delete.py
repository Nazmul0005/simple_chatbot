# import logging
# import logging.handlers
# from pathlib import Path
# from datetime import datetime
# from com.mhire.app.database.database_manager import db_manager
# from com.mhire.app.logger.logger import HistoryDeleteEndpoint

# logger = HistoryDeleteEndpoint.setup_history_delete_logger()

# async def delete_session(user_id: str, session_id: str):
#     """Delete all conversation history and session data for a specific session"""
#     try:
#         logger.info(f"Attempting to delete session history for user_id: {user_id}, session_id: {session_id}")
        
#         # Delete from conversation collection
#         conversation_result = await db_manager.collection.delete_one({
#             "user_id": user_id,
#             "session_id": session_id
#         })
        
#         # Delete from sessions collection
#         session_result = await db_manager.session_collection.delete_one({
#             "user_id": user_id,
#             "session_id": session_id
#         })
        
#         # Check if either deletion was successful
#         total_deleted = conversation_result.deleted_count + session_result.deleted_count
        
#         if total_deleted > 0:
#             logger.info(
#                 f"Successfully deleted session data for user_id: {user_id}, session_id: {session_id} "
#                 f"(conversation: {conversation_result.deleted_count}, session: {session_result.deleted_count})"
#             )
#         else:
#             logger.warning(f"No session found to delete for user_id: {user_id}, session_id: {session_id}")
        
#         return {
#             "message": "Session history deleted",
#             "deleted": total_deleted > 0,
#             "conversation_deleted": conversation_result.deleted_count > 0,
#             "session_deleted": session_result.deleted_count > 0
#         }
#     except Exception as e:
#         error_msg = f"Failed to delete session history for user_id: {user_id}, session_id: {session_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise Exception(error_msg) from e