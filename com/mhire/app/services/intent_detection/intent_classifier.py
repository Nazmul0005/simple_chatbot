"""Main intent classification orchestrator"""

from com.mhire.app.models.intent_models import IntentResult, IntentCategory, PriorityLevel
from .emergency_detector import is_emergency_or_crisis
from .semantic_classifier import classify_intent
from com.mhire.app.logger.logger import ChatEndpoint

logger = ChatEndpoint.setup_chat_logger()


class IntentClassifier:
    """
    Main orchestrator for intent classification
    Routes through emergency detection first, then semantic classification
    """
    
    @staticmethod
    def classify(message: str) -> IntentResult:
        """
        Classify user message intent
        Priority: Emergency > Crisis > Semantic Classification > General
        """
        logger.info("=" * 60)
        logger.info("INTENT CLASSIFICATION STARTED")
        logger.info(f"Message: {message[:100]}...")
        
        # Step 1: Check for emergency/crisis (highest priority)
        is_critical, critical_result = is_emergency_or_crisis(message)
        
        if is_critical:
            logger.warning(f"🚨 CRITICAL SITUATION DETECTED")
            logger.warning(f"Category: {critical_result.category.value}")
            logger.warning(f"Priority: {critical_result.priority.value}")
            logger.warning(f"Keywords: {critical_result.detected_keywords}")
            logger.info("=" * 60)
            return critical_result
        
        # Step 2: Semantic classification for non-critical messages
        logger.info("No critical situation detected, performing semantic classification...")
        result = classify_intent(message)
        
        logger.info(f"✓ Intent Classification Complete")
        logger.info(f"Category: {result.category.value}")
        logger.info(f"Priority: {result.priority.value}")
        logger.info(f"Confidence: {result.confidence:.2f}")
        if result.detected_keywords:
            logger.info(f"Keywords: {result.detected_keywords}")
        logger.info("=" * 60)
        
        return result