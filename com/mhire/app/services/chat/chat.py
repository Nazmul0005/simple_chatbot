# from datetime import datetime
# from typing import List
# import logging
# import logging.handlers
# from pathlib import Path
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import HumanMessage, AIMessage
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from com.mhire.app.config.config import Config
# from com.mhire.app.database.database_manager import db_manager
# from com.mhire.app.services.chat.chat_schema import ChatRequest, ChatResponse
# from com.mhire.app.utils.prompt.prompt import HEALTH_SYSTEM_PROMPT
# from com.mhire.app.logger.logger import ChatEndpoint




# logger = ChatEndpoint.setup_chat_logger()

# # Initialize Gemini Model
# config = Config()
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=config.GEMINI_API_KEY,
#     temperature=0.7,
#     convert_system_message_to_human=True
# )

# async def get_last_n_messages(user_id: str, session_id: str, n: int = 10):
#     """Get last N messages from a session"""
#     try:
#         logger.debug(f"Fetching last {n} messages for user_id: {user_id}, session_id: {session_id}")
#         session = await db_manager.collection.find_one(
#             {"user_id": user_id, "session_id": session_id},
#             {"messages": {"$slice": -n}}
#         )
        
#         if session and "messages" in session:
#             logger.debug(f"Retrieved {len(session['messages'])} messages from database")
#             return session["messages"]
#         logger.debug("No messages found for this session")
#         return []
#     except Exception as e:
#         error_msg = f"Failed to fetch messages for user_id: {user_id}, session_id: {session_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise Exception(error_msg) from e

# async def save_conversation_to_db(
#     user_id: str,
#     session_id: str,
#     user_message: str,
#     ai_response: str,
#     timestamp: datetime
# ):
#     """Save conversation to MongoDB and create/update session metadata"""
#     try:
#         logger.debug(f"Saving conversation for user_id: {user_id}, session_id: {session_id}")
#         existing_session = await db_manager.collection.find_one({
#             "user_id": user_id,
#             "session_id": session_id
#         })
        
#         new_messages = [
#             {
#                 "role": "user",
#                 "content": user_message,
#                 "timestamp": timestamp
#             },
#             {
#                 "role": "assistant",
#                 "content": ai_response,
#                 "timestamp": timestamp
#             }
#         ]
        
#         if existing_session:
#             # Update existing conversation in conversations collection
#             logger.debug(f"Updating existing session for user_id: {user_id}")
#             await db_manager.collection.update_one(
#                 {"user_id": user_id, "session_id": session_id},
#                 {
#                     "$push": {"messages": {"$each": new_messages}},
#                     "$set": {"updated_at": timestamp}
#                 }
#             )
#             logger.info(f"Session updated for user_id: {user_id}, session_id: {session_id}")
            
#             # Update session metadata in sessions collection
#             sessions_collection = db_manager.db["sessions"]
#             await sessions_collection.update_one(
#                 {"user_id": user_id, "session_id": session_id},
#                 {"$set": {"updated_at": timestamp}}
#             )
#             logger.debug(f"Session metadata updated_at for user_id: {user_id}, session_id: {session_id}")
#         else:
#             # Create new conversation in conversations collection
#             logger.debug(f"Creating new session for user_id: {user_id}")
#             conversation_doc = {
#                 "user_id": user_id,
#                 "session_id": session_id,
#                 "messages": new_messages,
#                 "created_at": timestamp,
#                 "updated_at": timestamp
#             }
#             await db_manager.collection.insert_one(conversation_doc)
#             logger.info(f"New session created for user_id: {user_id}, session_id: {session_id}")
            
#             # Create session metadata in sessions collection
#             # sessions_collection = db_manager.db["sessions"]
#             sessions_collection = db_manager.session_collection
            
#             session_metadata = {
#                 "user_id": user_id,
#                 "session_id": session_id,
#                 "title": "New Chat",
#                 "auto_named": True,
#                 "created_at": timestamp,
#                 "updated_at": timestamp
#             }
#             await sessions_collection.insert_one(session_metadata)
#             logger.info(f"Session metadata created for user_id: {user_id}, session_id: {session_id}")
            
#     except Exception as e:
#         error_msg = f"Failed to save conversation for user_id: {user_id}, session_id: {session_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise Exception(error_msg) from e

# def convert_to_langchain_messages(messages: List[dict]):
#     """Convert message list to LangChain message format"""
#     try:
#         logger.debug(f"Converting {len(messages)} messages to LangChain format")
#         langchain_messages = []
        
#         for msg in messages:
#             if msg["role"] == "user":
#                 langchain_messages.append(HumanMessage(content=msg["content"]))
#             elif msg["role"] == "assistant":
#                 langchain_messages.append(AIMessage(content=msg["content"]))
        
#         logger.debug(f"Successfully converted {len(langchain_messages)} messages")
#         return langchain_messages
#     except Exception as e:
#         error_msg = f"Failed to convert messages to LangChain format: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise Exception(error_msg) from e

# async def process_chat(request: ChatRequest) -> ChatResponse:
#     """Process chat request with conversation history"""
#     try:
#         logger.info(f"Processing chat request for user_id: {request.user_id}, session_id: {request.session_id}")
#         timestamp = datetime.utcnow()
        
#         # Fetch last 10 messages from database
#         logger.debug("Fetching conversation history")
#         last_10_messages = await get_last_n_messages(request.user_id, request.session_id, n=10)
        
#         # Convert to LangChain format
#         history_messages = convert_to_langchain_messages(last_10_messages)
        
#         # Create prompt template with conversation history
#         logger.debug("Creating prompt template with conversation history")
#         prompt = ChatPromptTemplate.from_messages([
#             ("system", HEALTH_SYSTEM_PROMPT),
#             MessagesPlaceholder(variable_name="history"),
#             ("human", "{input}")
#         ])
        
#         # Format the prompt with history and current query
#         formatted_messages = prompt.format_messages(
#             history=history_messages,
#             input=request.query
#         )
        
#         # Get response from Gemini
#         logger.debug("Invoking Gemini model for response")
#         response = await llm.ainvoke(formatted_messages)
#         ai_response = response.content
#         logger.debug("Received response from Gemini model")
        
#         # Save conversation to MongoDB
#         await save_conversation_to_db(
#             user_id=request.user_id,
#             session_id=request.session_id,
#             user_message=request.query,
#             ai_response=ai_response,
#             timestamp=timestamp
#         )
        
#         logger.info(f"Chat request processed successfully for user_id: {request.user_id}")
#         return ChatResponse(
#             user_id=request.user_id,
#             session_id=request.session_id,
#             query=request.query,
#             response=ai_response,
#             timestamp=timestamp
#         )
#     except Exception as e:
#         error_msg = f"Failed to process chat request for user_id: {request.user_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         raise Exception(error_msg) from e
