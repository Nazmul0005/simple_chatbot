"""RAG (Retrieval Augmented Generation) service"""

from typing import List, Optional, Tuple
from com.mhire.app.models.resource_models import Resource, ResourceType, RetrievalResult
from com.mhire.app.models.intent_models import IntentCategory, PriorityLevel
from com.mhire.app.services.resource_retrieval.vector_store import VectorStore
from com.mhire.app.services.resource_retrieval.function_service import FunctionService
from com.mhire.app.logger.logger import ChatEndpoint

logger = ChatEndpoint.setup_chat_logger()

class RAGService:
    """
    Retrieval Augmented Generation service
    Orchestrates between function calls and vector search
    """
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.function_service = FunctionService()
        
        # Try to load existing vector store
        if not self.vector_store.load():
            logger.warning("⚠️ Vector store not loaded. Run setup_vector_db.py first.")
        
        logger.info("RAGService initialized")
    
    def retrieve_resources(
        self,
        query: str,
        intent_category: IntentCategory,
        priority_level: PriorityLevel,
        top_k: int = 3
    ) -> RetrievalResult:
        """
        Retrieve resources based on query and intent
        
        Args:
            query: User's message
            intent_category: Detected intent category
            priority_level: Priority level of the intent
            top_k: Number of resources to retrieve
            
        Returns:
            RetrievalResult with resources and metadata
        """
        logger.info("=" * 60)
        logger.info("RESOURCE RETRIEVAL STARTED")
        logger.info(f"Query: {query[:50]}...")
        logger.info(f"Intent: {intent_category.value}")
        logger.info(f"Priority: {priority_level.value}")
        
        # Route based on priority and intent
        if priority_level == PriorityLevel.CRITICAL:
            result = self._handle_emergency(query, intent_category)
        elif priority_level == PriorityLevel.HIGH:
            result = self._handle_crisis(query, intent_category, top_k)
        elif priority_level == PriorityLevel.MEDIUM:
            result = self._handle_medium_priority(query, intent_category, top_k)
        else:
            result = self._handle_general(query, intent_category, top_k)
        
        logger.info(f"✓ Resource Retrieval Complete")
        logger.info(f"Method Used: {result.method_used}")
        logger.info(f"Resources Retrieved: {len(result.resources)}")
        logger.info("=" * 60)
        
        return result
    
    def _handle_emergency(self, query: str, intent_category: IntentCategory) -> RetrievalResult:
        """Handle emergency situations - use function calls only"""
        logger.warning("🚨 EMERGENCY - Using function service")
        
        resources = self.function_service.get_emergency_contacts()
        
        return RetrievalResult(
            resources=resources,
            method_used="function_call",
            query=query
        )
    
    def _handle_crisis(
        self, 
        query: str, 
        intent_category: IntentCategory, 
        top_k: int
    ) -> RetrievalResult:
        """Handle crisis situations - hybrid approach"""
        logger.warning("⚡ CRISIS - Using hybrid approach (function + RAG)")
        
        resources = []
        method_used = "hybrid"
        
        # Add crisis helplines via function call
        helplines = self.function_service.get_crisis_helplines()
        resources.extend(helplines[:1])  # Just one helpline
        
        # Search for coping techniques via RAG
        if self.vector_store.index is not None:
            rag_resources, scores = self.vector_store.search(
                query=query,
                top_k=top_k - 1,
                urgency_filter="critical"
            )
            resources.extend(rag_resources)
            
            return RetrievalResult(
                resources=resources,
                method_used=method_used,
                query=query,
                relevance_scores=scores
            )
        else:
            logger.warning("Vector store not available, using function only")
            return RetrievalResult(
                resources=resources,
                method_used="function_call",
                query=query
            )
    
    def _handle_medium_priority(
        self,
        query: str,
        intent_category: IntentCategory,
        top_k: int
    ) -> RetrievalResult:
        """Handle medium priority - function calls for specific categories"""
        logger.info("📋 MEDIUM PRIORITY - Checking category routing")
        
        # Route to specific functions based on intent
        if intent_category == IntentCategory.SEEKING_TREATMENT:
            resources = self.function_service.get_treatment_locator()
            return RetrievalResult(
                resources=resources,
                method_used="function_call",
                query=query
            )
        
        elif intent_category == IntentCategory.HARM_REDUCTION:
            resources = self.function_service.get_harm_reduction_basics()
            return RetrievalResult(
                resources=resources,
                method_used="function_call",
                query=query
            )
        
        else:
            # Use RAG for other medium priority queries
            return self._search_vector_store(query, top_k, urgency_filter=None)
    
    def _handle_general(
        self,
        query: str,
        intent_category: IntentCategory,
        top_k: int
    ) -> RetrievalResult:
        """Handle general queries - optional RAG"""
        logger.info("💬 GENERAL - Optional RAG search")
        
        # Only search if intent is learning techniques or support
        if intent_category in [IntentCategory.LEARNING_TECHNIQUES, IntentCategory.SUPPORT_CONNECTION]:
            return self._search_vector_store(query, top_k)
        else:
            # No resources needed for general conversation
            return RetrievalResult(
                resources=[],
                method_used="none",
                query=query
            )
    
    def _search_vector_store(
        self,
        query: str,
        top_k: int,
        urgency_filter: Optional[str] = None
    ) -> RetrievalResult:
        """Search vector store with RAG"""
        logger.info("🔍 RAG - Searching vector store")
        
        if self.vector_store.index is None:
            logger.warning("Vector store not available")
            return RetrievalResult(
                resources=[],
                method_used="none",
                query=query
            )
        
        resources, scores = self.vector_store.search(
            query=query,
            top_k=top_k,
            urgency_filter=urgency_filter
        )
        
        return RetrievalResult(
            resources=resources,
            method_used="rag",
            query=query,
            relevance_scores=scores
        )