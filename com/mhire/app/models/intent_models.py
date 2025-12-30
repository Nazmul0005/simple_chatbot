from enum import Enum
from dataclasses import dataclass
from typing import Optional, List

class IntentCategory(str, Enum):
    """Intent categories for user messages"""
    EMERGENCY_CRISIS = "emergency_crisis"
    ACTIVE_CRAVING = "active_craving"
    SEEKING_TREATMENT = "seeking_treatment"
    HARM_REDUCTION = "harm_reduction"
    LEARNING_TECHNIQUES = "learning_techniques"
    SUPPORT_CONNECTION = "support_connection"
    GENERAL_CONVERSATION = "general_conversation"

class PriorityLevel(str, Enum):
    """Priority levels for intent handling"""
    CRITICAL = "critical"  # Emergency - immediate response
    HIGH = "high"          # Crisis - needs resources now
    MEDIUM = "medium"      # Seeking help/info
    LOW = "low"            # General conversation

@dataclass
class IntentResult:
    """Result of intent classification"""
    category: IntentCategory
    priority: PriorityLevel
    confidence: float
    detected_keywords: Optional[List[str]] = None
    reasoning: Optional[str] = None