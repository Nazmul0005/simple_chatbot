"""Emergency and crisis detection using keyword matching"""

from typing import List, Optional, Tuple
from com.mhire.app.models.intent_models import IntentCategory, PriorityLevel, IntentResult

# Emergency keywords that trigger immediate response
EMERGENCY_KEYWORDS = {
    'suicide': ['suicide', 'suicidal', 'kill myself', 'end my life', 'want to die', 
                'better off dead', 'no reason to live'],
    'self_harm': ['self harm', 'self-harm', 'cut myself', 'hurt myself', 'harm myself'],
    'overdose': ['overdose', 'overdosed', 'took too much', 'too many pills'],
    'severe_distress': ['can\'t go on', 'can\'t take it', 'give up', 'end it all']
}

# Crisis keywords (high priority but not emergency)
CRISIS_KEYWORDS = {
    'craving': ['craving', 'cravings', 'intense urge', 'strong urge', 'need to use'],
    'relapse_risk': ['going to relapse', 'about to relapse', 'can\'t resist', 
                     'going to use', 'want to use now'],
    'withdrawal': ['withdrawal', 'withdrawing', 'severe symptoms'],
    'high_distress': ['overwhelmed', 'can\'t handle', 'too much', 'breaking down',
                      'losing control', 'panic']
}


def detect_emergency(message: str) -> Optional[IntentResult]:
    """
    Fast emergency detection using keyword matching
    Returns IntentResult if emergency detected, None otherwise
    """
    message_lower = message.lower()
    detected_keywords = []
    
    # Check for emergency keywords
    for category, keywords in EMERGENCY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message_lower:
                detected_keywords.append(keyword)
    
    if detected_keywords:
        return IntentResult(
            category=IntentCategory.EMERGENCY_CRISIS,
            priority=PriorityLevel.CRITICAL,
            confidence=1.0,
            detected_keywords=detected_keywords,
            reasoning=f"Emergency keywords detected: {', '.join(detected_keywords)}"
        )
    
    return None


def detect_crisis(message: str) -> Optional[IntentResult]:
    """
    Detect crisis situations (high priority but not emergency)
    Returns IntentResult if crisis detected, None otherwise
    """
    message_lower = message.lower()
    detected_keywords = []
    
    # Check for crisis keywords
    for category, keywords in CRISIS_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message_lower:
                detected_keywords.append(keyword)
    
    if detected_keywords:
        return IntentResult(
            category=IntentCategory.ACTIVE_CRAVING,
            priority=PriorityLevel.HIGH,
            confidence=0.9,
            detected_keywords=detected_keywords,
            reasoning=f"Crisis keywords detected: {', '.join(detected_keywords)}"
        )
    
    return None


def is_emergency_or_crisis(message: str) -> Tuple[bool, Optional[IntentResult]]:
    """
    Check if message is emergency or crisis
    Returns (is_emergency_or_crisis, IntentResult)
    """
    # Check emergency first (highest priority)
    emergency_result = detect_emergency(message)
    if emergency_result:
        return True, emergency_result
    
    # Check crisis
    crisis_result = detect_crisis(message)
    if crisis_result:
        return True, crisis_result
    
    return False, None