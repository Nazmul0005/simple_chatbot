from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from com.mhire.app.config.config import Config
from com.mhire.app.services.ai_chat.ai_chat_schema import AIChatRequest, AIChatResponse, MessageHistory
from com.mhire.app.logger.logger import ChatEndpoint

# NEW IMPORTS
from com.mhire.app.services.intent_detection.intent_classifier import IntentClassifier
from com.mhire.app.services.resource_retrieval.rag_service import RAGService
from com.mhire.app.models.intent_models import PriorityLevel
from com.mhire.app.prompts.system_prompts import (
    BASE_SORA_PROMPT,
    EMERGENCY_PROMPT,
    CRISIS_WITH_RESOURCES_PROMPT,
    MEDIUM_WITH_RESOURCES_PROMPT,
    GENERAL_WITH_CONTEXT_PROMPT
)
from com.mhire.app.prompts.resource_prompts import (
    format_emergency_resources,
    format_technique_resources,
    format_general_resources
)

logger = ChatEndpoint.setup_chat_logger()

# Initialize services
config = Config()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=config.GEMINI_API_KEY,
    temperature=0.7,
    convert_system_message_to_human=True
)

# Initialize RAG service
rag_service = RAGService()

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


def select_system_prompt(priority_level: PriorityLevel, resources: list) -> str:
    """
    Select appropriate system prompt based on priority and resources
    
    Args:
        priority_level: Priority level from intent classification
        resources: Retrieved resources
        
    Returns:
        Formatted system prompt
    """
    if priority_level == PriorityLevel.CRITICAL:
        # Emergency situation
        formatted_resources = format_emergency_resources(resources)
        return EMERGENCY_PROMPT.format(emergency_resources=formatted_resources)
    
    elif priority_level == PriorityLevel.HIGH:
        # Crisis situation with techniques
        formatted_resources = format_technique_resources(resources)
        return CRISIS_WITH_RESOURCES_PROMPT.format(retrieved_resources=formatted_resources)
    
    elif priority_level == PriorityLevel.MEDIUM and resources:
        # Medium priority with structured resources (treatment, harm reduction)
        formatted_resources = format_general_resources(resources)
        return MEDIUM_WITH_RESOURCES_PROMPT.format(retrieved_resources=formatted_resources)
    
    elif resources:
        # General with optional context
        formatted_resources = format_general_resources(resources)
        return GENERAL_WITH_CONTEXT_PROMPT.format(retrieved_resources=formatted_resources)
    
    else:
        # Default Sora prompt
        return BASE_SORA_PROMPT


async def process_ai_chat(request: AIChatRequest) -> AIChatResponse:
    """Process AI chat request with intent detection and resource retrieval"""
    try:
        logger.info(f"Processing AI chat request")
        
        # STEP 1: Classify intent
        intent_result = IntentClassifier.classify(request.query)
        
        # STEP 2: Retrieve resources based on intent
        retrieval_result = rag_service.retrieve_resources(
            query=request.query,
            intent_category=intent_result.category,
            priority_level=intent_result.priority,
            top_k=3
        )
        
        # STEP 3: Select appropriate system prompt
        system_prompt = select_system_prompt(
            priority_level=intent_result.priority,
            resources=retrieval_result.resources
        )
        
        # STEP 4: Convert history to LangChain format
        logger.debug(f"Converting {len(request.history)} history messages")
        history_messages = convert_to_langchain_messages(request.history)
        
        # STEP 5: Create prompt template with selected system prompt
        logger.debug("Creating prompt template with conversation history")
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # STEP 6: Format the prompt
        formatted_messages = prompt.format_messages(
            history=history_messages,
            input=request.query
        )
        
        # STEP 7: Get response from Gemini
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