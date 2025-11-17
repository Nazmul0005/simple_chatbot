# import logging
# import logging.handlers
# from pathlib import Path
# from datetime import datetime
# from com.mhire.app.database.database_manager import db_manager
# from com.mhire.app.services.conversation.conversation_schema import LoadConversationRequest
# from com.mhire.app.logger.logger import ConversationEndpoint

# logger = ConversationEndpoint.setup_conversation_logger()

# async def load_all_conversation(user_id: str, session_id: str):
#     """Load all conversation messages for a specific user_id and session_id"""
#     try:
#         logger.debug(f"Loading all conversation for user_id: {user_id}, session_id: {session_id}")
#         session = await db_manager.collection.find_one(
#             {"user_id": user_id, "session_id": session_id}
#         )
        
#         if session:
#             total_messages = len(session.get("messages", []))
#             logger.debug(f"Fetching session title from sessions collection")
            
#             # Fetch session title from sessions collection
#             sessions_collection = db_manager.db["sessions"]
#             session_metadata = await sessions_collection.find_one(
#                 {"user_id": user_id, "session_id": session_id}
#             )
            
#             title = session_metadata.get("title", "New Chat") if session_metadata else "New Chat"
#             logger.debug(f"Retrieved title: {title}")
            
#             logger.info(f"Successfully loaded conversation with {total_messages} messages for user_id: {user_id}, session_id: {session_id}")
#             return {
#                 "user_id": session["user_id"],
#                 "session_id": session["session_id"],
#                 "title": title,
#                 "messages": session.get("messages", []),
#                 "created_at": session.get("created_at"),
#                 "updated_at": session.get("updated_at"),
#                 "total_messages": total_messages
#             }
#         logger.warning(f"No conversation found for user_id: {user_id}, session_id: {session_id}")
#         return None
#     except Exception as e:
#         error_msg = f"Failed to load conversation for user_id: {user_id}, session_id: {session_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise Exception(error_msg) from e

# async def get_conversation(request: LoadConversationRequest):
#     """Get conversation data for a specific user and session"""
#     try:
#         logger.info(f"Getting conversation for user_id: {request.user_id}, session_id: {request.session_id}")
#         conversation_data = await load_all_conversation(request.user_id, request.session_id)
#         return conversation_data
#     except Exception as e:
#         error_msg = f"Failed to get conversation for user_id: {request.user_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise Exception(error_msg) from e
