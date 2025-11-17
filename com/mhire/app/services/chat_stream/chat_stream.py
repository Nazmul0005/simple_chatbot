# import json
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
# from com.mhire.app.services.chat_stream.chat_stream_schema import ChatStreamRequest
# from com.mhire.app.logger.logger import ChatStreamEndpoint




# logger = ChatStreamEndpoint.setup_chat_stream_logger()

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
#     """Save conversation to MongoDB using upsert pattern"""
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
#             logger.debug(f"Updating existing session for user_id: {user_id}")
#             await db_manager.collection.update_one(
#                 {"user_id": user_id, "session_id": session_id},
#                 {
#                     "$push": {"messages": {"$each": new_messages}},
#                     "$set": {"updated_at": timestamp}
#                 }
#             )
#             logger.info(f"Session updated for user_id: {user_id}, session_id: {session_id}")
#         else:
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

# async def generate_stream(request: ChatStreamRequest):
#     """Generate streaming response"""
#     try:
#         logger.info(f"Starting stream generation for user_id: {request.user_id}, session_id: {request.session_id}")
#         timestamp = datetime.utcnow()
#         full_response = ""
#         chunk_count = 0
        
#         # Fetch last 10 messages from database
#         logger.debug("Fetching conversation history")
#         last_10_messages = await get_last_n_messages(request.user_id, request.session_id, n=10)
        
#         # Convert to LangChain format
#         history_messages = convert_to_langchain_messages(last_10_messages)
        
#         # Create prompt template with conversation history
#         logger.debug("Creating prompt template with conversation history")
#         prompt = ChatPromptTemplate.from_messages([
#             ("system", """You are a helpful AI assistant. 
#             Use the conversation history to provide contextually relevant responses. 
#             Be conversational, friendly, and remember details from previous messages."""),
#             MessagesPlaceholder(variable_name="history"),
#             ("human", "{input}")
#         ])
        
#         # Format the prompt with history and current query
#         formatted_messages = prompt.format_messages(
#             history=history_messages,
#             input=request.query
#         )
        
#         # Stream response from Gemini
#         logger.debug("Starting stream from Gemini model")
#         async for chunk in llm.astream(formatted_messages):
#             if chunk.content:
#                 full_response += chunk.content
#                 chunk_count += 1
#                 logger.debug(f"Streamed chunk {chunk_count}: {len(chunk.content)} characters")
#                 yield f"data: {json.dumps({'chunk': chunk.content, 'done': False})}\n\n"
        
#         logger.info(f"Stream completed with {chunk_count} chunks, total response length: {len(full_response)}")
        
#         # Save complete conversation to MongoDB
#         await save_conversation_to_db(
#             user_id=request.user_id,
#             session_id=request.session_id,
#             user_message=request.query,
#             ai_response=full_response,
#             timestamp=timestamp
#         )
        
#         # Send completion signal
#         logger.debug("Sending stream completion signal")
#         yield f"data: {json.dumps({'chunk': '', 'done': True, 'full_response': full_response})}\n\n"
#         logger.info(f"Stream generation completed successfully for user_id: {request.user_id}")
        
#     except Exception as e:
#         error_msg = f"Error during stream generation for user_id: {request.user_id}: {str(e)}"
#         logger.error(error_msg, exc_info=True)
#         error_data = json.dumps({'error': error_msg, 'done': True})
#         yield f"data: {error_data}\n\n"
