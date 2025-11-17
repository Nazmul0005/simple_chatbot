# import logging
# import logging.handlers
# from pathlib import Path
# from datetime import datetime
# from com.mhire.app.database.database_manager import db_manager
# from com.mhire.app.logger.logger import HistoryGetEndpoint

# logger = HistoryGetEndpoint.setup_history_get_logger()

# async def get_session_history(user_id: str, session_id: str, limit: int = 50):
#     """Retrieve conversation history from MongoDB"""
#     try:
#         logger.debug(f"Fetching session history for user_id: {user_id}, session_id: {session_id}, limit: {limit}")
#         session = await db_manager.collection.find_one(
#             {"user_id": user_id, "session_id": session_id},
#             {"messages": {"$slice": -limit}}
#         )
        
#         if session and "messages" in session:
#             logger.debug(f"Retrieved {len(session['messages'])} messages from database")
#             return session["messages"]
#         logger.debug("No messages found for this session")
#         return []
#     except Exception as e:
#         error_msg = f"Failed to fetch session history for user_id: {user_id}, session_id: {session_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise Exception(error_msg) from e

# async def fetch_conversation_history(user_id: str, session_id: str, limit: int = 50):
#     """Fetch conversation history for a user session"""
#     try:
#         logger.info(f"Fetching conversation history for user_id: {user_id}, session_id: {session_id}")
#         history = await get_session_history(user_id, session_id, limit)
#         logger.info(f"Successfully retrieved {len(history)} messages for user_id: {user_id}")
#         return {
#             "user_id": user_id,
#             "session_id": session_id,
#             "history": history,
#             "count": len(history)
#         }
#     except Exception as e:
#         error_msg = f"Failed to fetch conversation history for user_id: {user_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise Exception(error_msg) from e
