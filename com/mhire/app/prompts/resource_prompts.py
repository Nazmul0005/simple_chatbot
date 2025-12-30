"""Prompts for resource formatting"""

def format_emergency_resources(resources: list) -> str:
    """Format emergency resources for prompt"""
    formatted = []
    for resource in resources:
        formatted.append(f"- {resource.title}: {resource.contact_info or resource.content}")
    return "\n".join(formatted)


def format_technique_resources(resources: list) -> str:
    """Format technique resources for prompt"""
    formatted = []
    for resource in resources:
        formatted.append(f"**{resource.title}**\n{resource.content}\n")
    return "\n".join(formatted)


def format_general_resources(resources: list) -> str:
    """Format general resources for prompt"""
    formatted = []
    for resource in resources:
        parts = [f"**{resource.title}**", resource.content]
        
        # Add URL if available
        if resource.source_url:
            parts.append(f"URL: {resource.source_url}")
        
        # Add contact info if available
        if resource.contact_info:
            parts.append(f"Contact: {resource.contact_info}")
        
        formatted.append("\n".join(parts))
    
    return "\n\n".join(formatted)