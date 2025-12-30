"""Semantic intent classification for non-emergency messages"""

from typing import Optional
from com.mhire.app.models.intent_models import IntentCategory, PriorityLevel, IntentResult

# Intent patterns for semantic matching
INTENT_PATTERNS = {
    IntentCategory.SEEKING_TREATMENT: {
        'keywords': ['treatment', 'help', 'therapy', 'counseling', 'rehab', 'program', 
                     'find help', 'get help', 'medication', 'doctor', 'professional','opioid','acamprosate','buprenorphine', 'naltrexone', 'disulfiram', 'alcohol','bupropion', 'varenicline', 'tobacco','nicotine', 'nrt', 'cocaine', 'methamphetamine', 'stimulants'],
        'priority': PriorityLevel.MEDIUM,
        'confidence_threshold': 0.1
    },
    IntentCategory.HARM_REDUCTION: {
        'keywords': ['safer', 'harm','reduce harm', 'naloxone', 'narcan', 'Naloxone','Narcan', 'test strips','needle exchange', 'overdose prevention', 'safe use', 'opioid overdose', 'opioid', 'safer injection techniques', 'safer injection', 'mixing substances', 'overdose sign', 'test strip', 'fentanyl', 'fentanyl test', 'needle exchange', 'Syringe', 'disposal', 'harm reduction', 'samartian law', 'infectious diseases', 'HIV', 'hepatitis', 'infectious', 'hepatitis'],
        'priority': PriorityLevel.MEDIUM,
        'confidence_threshold': 0.1  # Low threshold since these keywords are very specific
    },
    IntentCategory.LEARNING_TECHNIQUES: {
        'keywords': ['technique', 'strategy', 'strategies','coping', 'manage', 'deal with','cognitive',
                     'handle', 'breathing', 'meditation', 'mindfulness', 'exercise'],
        'priority': PriorityLevel.LOW,
        'confidence_threshold': 0.5
    },
    IntentCategory.SUPPORT_CONNECTION: {
        'keywords': ['support group', 'meeting', 'community', 'alone', 'isolated',
                     'connect', 'talk to someone', 'share', 'contact,''support', ' alcoholics', 'smartwellness', 'drug abuse'],
        'priority': PriorityLevel.LOW,
        'confidence_threshold': 0.6
    }
}


def classify_intent(message: str) -> IntentResult:
    """
    Classify intent using keyword matching and scoring
    Returns IntentResult with best matching category
    """
    message_lower = message.lower()
    best_match = None
    best_score = 0.0
    best_keywords = []
    
    for intent_category, pattern_config in INTENT_PATTERNS.items():
        keywords = pattern_config['keywords']
        matched_keywords = []
        
        # Count keyword matches
        for keyword in keywords:
            if keyword in message_lower:
                matched_keywords.append(keyword)
        
        # Calculate confidence score
        if matched_keywords:
            score = len(matched_keywords) / len(keywords)
            
            if score > best_score and score >= pattern_config['confidence_threshold']:
                best_score = score
                best_match = intent_category
                best_keywords = matched_keywords
    
    # If no match found, default to general conversation
    if not best_match:
        return IntentResult(
            category=IntentCategory.GENERAL_CONVERSATION,
            priority=PriorityLevel.LOW,
            confidence=1.0,
            reasoning="No specific intent pattern matched, treating as general conversation"
        )
    
    return IntentResult(
        category=best_match,
        priority=INTENT_PATTERNS[best_match]['priority'],
        confidence=best_score,
        detected_keywords=best_keywords,
        reasoning=f"Matched keywords: {', '.join(best_keywords)}"
    )