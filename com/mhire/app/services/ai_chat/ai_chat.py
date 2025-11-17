from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from com.mhire.app.config.config import Config
from com.mhire.app.services.ai_chat.ai_chat_schema import AIChatRequest, AIChatResponse, MessageHistory
from com.mhire.app.utils.prompt.prompt_short import HEALTH_SYSTEM_PROMPT
from com.mhire.app.logger.logger import ChatEndpoint

logger = ChatEndpoint.setup_chat_logger()

# Initialize Gemini Model
config = Config()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=config.GEMINI_API_KEY,
    temperature=0.7,
    convert_system_message_to_human=True
)

def convert_to_langchain_messages(messages: List[MessageHistory]):
    """Convert message list to LangChain message format"""
    try:
        logger.debug(f"Converting {len(messages)} messages to LangChain format")
        langchain_messages = []
        
        for msg in messages:
            if msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                langchain_messages.append(AIMessage(content=msg.content))
        
        logger.debug(f"Successfully converted {len(langchain_messages)} messages")
        return langchain_messages
    except Exception as e:
        error_msg = f"Failed to convert messages to LangChain format: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise Exception(error_msg) from e

async def process_ai_chat(request: AIChatRequest) -> AIChatResponse:
    """Process AI chat request with conversation history (no DB operations)"""
    try:
        logger.info(f"Processing AI chat request")
        
        # Convert history to LangChain format
        logger.debug(f"Converting {len(request.history)} history messages")
        history_messages = convert_to_langchain_messages(request.history)
        
        # Create prompt template with conversation history
        logger.debug("Creating prompt template with conversation history")
        prompt = ChatPromptTemplate.from_messages([
            ("system", HEALTH_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # Format the prompt with history and current query
        formatted_messages = prompt.format_messages(
            history=history_messages,
            input=request.query
        )
        
        # Get response from Gemini
        logger.debug("Invoking Gemini model for response")
        response = await llm.ainvoke(formatted_messages)
        ai_response = response.content
        logger.debug("Received response from Gemini model")
        
        logger.info(f"AI chat request processed successfully")
        return AIChatResponse(
            query=request.query,
            response=ai_response
        )
    except Exception as e:
        error_msg = f"Failed to process AI chat request: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise Exception(error_msg) from e