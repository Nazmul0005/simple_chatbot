"""Structured function service for emergency and critical resources"""

from typing import List
from com.mhire.app.models.resource_models import Resource, ResourceType
from com.mhire.app.logger.logger import ChatEndpoint

logger = ChatEndpoint.setup_chat_logger()

class FunctionService:
    """
    Provides structured, predefined resources for critical situations
    No vector search needed - direct function calls
    """
    
    @staticmethod
    def get_emergency_contacts() -> List[Resource]:
        """
        Get emergency contact resources
        Returns immediately without search
        """
        logger.info("📞 FUNCTION CALL: get_emergency_contacts()")
        
        resources = [
            Resource(
                content="For life-threatening emergencies, call 911 immediately.",
                resource_type=ResourceType.EMERGENCY_CONTACT,
                urgency_level="emergency",
                section="1.1",
                title="911 Emergency",
                contact_info="Call 911"
            ),
            Resource(
                content="If you're having thoughts of suicide or need mental health support, help is available 24/7.",
                resource_type=ResourceType.EMERGENCY_CONTACT,
                urgency_level="emergency",
                section="1.2",
                title="988 Suicide & Crisis Lifeline",
                contact_info="Call or text 988"
            ),
            Resource(
                content="Connect with a trained crisis counselor anytime, day or night.",
                resource_type=ResourceType.EMERGENCY_CONTACT,
                urgency_level="emergency",
                section="1.3",
                title="Crisis Text Line",
                contact_info="Text HOME to 741741"
            ),
            Resource(
                content="Veterans can get immediate crisis support from counselors who understand military experience.",
                resource_type=ResourceType.EMERGENCY_CONTACT,
                urgency_level="emergency",
                section="1.4",
                title="Veterans Crisis Line",
                contact_info="Call 988 and press 1, or text 838255"
            )
        ]
        
        logger.info(f"✓ Returned {len(resources)} emergency contacts")
        return resources
    
    @staticmethod
    def get_crisis_helplines() -> List[Resource]:
        """Get crisis helplines for high-priority situations"""
        logger.info("📞 FUNCTION CALL: get_crisis_helplines()")
        
        resources = [
            Resource(
                content="SAMHSA's National Helpline provides free, confidential, 24/7 treatment referral and information for individuals and families facing mental health and/or substance use disorders.",
                resource_type=ResourceType.SUPPORT_GROUP,
                urgency_level="critical",
                section="4.1.1",
                title="SAMHSA's National Helpline",
                contact_info="1-800-662-HELP (4357)"
            ),
            Resource(
                content="If you're having thoughts of suicide or need mental health support, help is available 24/7.",
                resource_type=ResourceType.EMERGENCY_CONTACT,
                urgency_level="critical",
                section="1.2",
                title="988 Suicide & Crisis Lifeline",
                contact_info="Call or text 988"
            )
        ]
        
        logger.info(f"✓ Returned {len(resources)} crisis helplines")
        return resources
    
    @staticmethod
    def get_treatment_locator() -> List[Resource]:
        """Get treatment facility locator information"""
        logger.info("📞 FUNCTION CALL: get_treatment_locator()")
        
        resources = [
            Resource(
                content="Find local treatment facilities for substance use and mental health issues using SAMHSA's Treatment Locator.",
                resource_type=ResourceType.TREATMENT_INFO,
                urgency_level="general",
                section="3.6.1",
                title="SAMHSA's Treatment Locator",
                source_url="https://findtreatment.gov/"
            ),
            Resource(
                content="Call SAMHSA's National Helpline for treatment referral and information service. Free, confidential, 24/7.",
                resource_type=ResourceType.TREATMENT_INFO,
                urgency_level="general",
                section="3.6.2",
                title="SAMHSA's National Helpline",
                contact_info="1-800-662-HELP (4357)"
            )
        ]
        
        logger.info(f"✓ Returned {len(resources)} treatment locator resources")
        return resources
    
    @staticmethod
    def get_harm_reduction_basics() -> List[Resource]:
        """Get basic harm reduction information"""
        logger.info("📞 FUNCTION CALL: get_harm_reduction_basics()")
        
        resources = [
            Resource(
                content="Naloxone (Narcan) is a life-saving medication that can reverse an opioid overdose. It's available without a prescription in many states.",
                resource_type=ResourceType.HARM_REDUCTION,
                urgency_level="critical",
                section="2.1",
                title="Naloxone (Narcan)",
                source_url="https://www.samhsa.gov/medication-assisted-treatment/medications-counseling-related-conditions/opioid-overdose"
            ),
            Resource(
                content="Fentanyl test strips can detect the presence of fentanyl in substances before use, helping prevent accidental fentanyl exposure.",
                resource_type=ResourceType.HARM_REDUCTION,
                urgency_level="critical",
                section="2.3",
                title="Fentanyl Test Strips",
                source_url="https://www.samhsa.gov/find-help/harm-reduction"
            ),
            Resource(
                content="Good Samaritan Laws provide legal protections for calling 911 during an overdose emergency, protecting people even if substances are present.",
                resource_type=ResourceType.HARM_REDUCTION,
                urgency_level="general",
                section="2.5",
                title="Good Samaritan Laws",
                source_url="https://oasas.ny.gov/good-samaritan-law"
            )
        ]
        
        logger.info(f"✓ Returned {len(resources)} harm reduction resources")
        return resources