from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

class ResourceType(str, Enum):
    """Types of resources"""
    EMERGENCY_CONTACT = "emergency_contact"
    TECHNIQUE = "technique"
    TREATMENT_INFO = "treatment_info"
    SUPPORT_GROUP = "support_group"
    HARM_REDUCTION = "harm_reduction"
    COPING_STRATEGY = "coping_strategy"

@dataclass
class Resource:
    """Individual resource with metadata"""
    content: str
    resource_type: ResourceType
    urgency_level: str  # "emergency", "critical", "general"
    section: str  # Section number from document
    title: str
    source_url: Optional[str] = None
    contact_info: Optional[str] = None

@dataclass
class RetrievalResult:
    """Result from resource retrieval"""
    resources: List[Resource]
    method_used: str  # "function_call", "rag", "hybrid", "none"
    query: str
    relevance_scores: Optional[List[float]] = None