"""
One-time setup script to create vector database from resources
Run this script once after adding your resource document

Usage:
    python scripts/setup_vector_db.py
"""

import os
import sys
import re

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from com.mhire.app.utils.text_processor import chunk_by_section
from com.mhire.app.models.resource_models import Resource, ResourceType
from com.mhire.app.services.resource_retrieval.vector_store import VectorStore
from com.mhire.app.services.resource_retrieval.embeddings_service import EmbeddingsService


def determine_resource_type(section: str, title: str) -> ResourceType:
    """
    Determine resource type based on section number and title
    
    Args:
        section: Section number (e.g., "1.1", "2.3")
        title: Section title
        
    Returns:
        ResourceType enum value
    """
    section_lower = section.lower()
    title_lower = title.lower()
    
    # Section-based classification
    if section.startswith("1."):
        return ResourceType.EMERGENCY_CONTACT
    elif section.startswith("2."):
        return ResourceType.HARM_REDUCTION
    elif section.startswith("3."):
        return ResourceType.TREATMENT_INFO
    elif section.startswith("4."):
        return ResourceType.SUPPORT_GROUP
    
    # Title-based classification for sections 5-7
    if any(keyword in title_lower for keyword in ["technique", "strategy", "method", "approach"]):
        return ResourceType.TECHNIQUE
    else:
        return ResourceType.COPING_STRATEGY


def determine_urgency_level(section: str, title: str) -> str:
    """
    Determine urgency level based on section
    
    Args:
        section: Section number
        title: Section title
        
    Returns:
        Urgency level: "emergency", "critical", or "general"
    """
    # Emergency resources (Section 1)
    if section.startswith("1."):
        return "emergency"
    
    # Critical resources (Sections 2, 5, 6, 7 - immediate coping needs)
    elif section.startswith("2.") or section.startswith("5.") or \
         section.startswith("6.") or section.startswith("7."):
        return "critical"
    
    # General resources (Sections 3, 4 - treatment info, support)
    else:
        return "general"


def extract_contact_info(content: str, title: str) -> str:
    """
    Extract contact information from content
    
    Args:
        content: Resource content text
        title: Resource title
        
    Returns:
        Contact info string or None
    """
    # Look for specific known numbers
    if "988" in content:
        return "Call or text 988"
    
    if "741741" in content:
        return "Text HOME to 741741"
    
    if "911" in content and "emergency" in content.lower():
        return "Call 911"
    
    # Look for phone number patterns
    phone_pattern = r'(\d{1}-\d{3}-\d{3}-\d{4}|\d{3}-\d{4}|1-800-\d{3}-\d{4})'
    phone_match = re.search(phone_pattern, content)
    if phone_match:
        return phone_match.group(0)
    
    # Look for "Call" or "Text" instructions
    call_pattern = r'(?:Call|Text|Contact)[\s:]+([^.]+?)(?:\.|,|$)'
    call_match = re.search(call_pattern, content, re.IGNORECASE)
    if call_match:
        contact = call_match.group(1).strip()
        # Clean up if it's too long
        if len(contact) < 50:
            return contact
    
    # Look for "press" instructions (like Veterans Crisis Line)
    press_pattern = r'(Call \d+ and press \d+)'
    press_match = re.search(press_pattern, content, re.IGNORECASE)
    if press_match:
        return press_match.group(1)
    
    return None


def extract_source_url(content: str) -> str:
    """
    Extract URL from content
    
    Args:
        content: Resource content text
        
    Returns:
        URL string or None
    """
    # URL pattern
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    url_match = re.search(url_pattern, content)
    
    return url_match.group(0) if url_match else None


def print_statistics(resources: list):
    """Print statistics about processed resources"""
    print("\n" + "=" * 60)
    print("📊 RESOURCE STATISTICS")
    print("=" * 60)
    
    # Count by resource type
    type_counts = {}
    for resource in resources:
        type_name = resource.resource_type.value
        type_counts[type_name] = type_counts.get(type_name, 0) + 1
    
    print("\nBy Resource Type:")
    for res_type, count in sorted(type_counts.items()):
        print(f"  {res_type}: {count}")
    
    # Count by urgency level
    urgency_counts = {}
    for resource in resources:
        urgency = resource.urgency_level
        urgency_counts[urgency] = urgency_counts.get(urgency, 0) + 1
    
    print("\nBy Urgency Level:")
    for urgency, count in sorted(urgency_counts.items()):
        print(f"  {urgency}: {count}")
    
    # Count resources with URLs
    url_count = sum(1 for r in resources if r.source_url)
    print(f"\nResources with URLs: {url_count}")
    
    # Count resources with contact info
    contact_count = sum(1 for r in resources if r.contact_info)
    print(f"Resources with Contact Info: {contact_count}")


def main():
    """Main setup function"""
    print("\n" + "=" * 60)
    print("VECTOR DATABASE SETUP")
    print("=" * 60)
    print("\nThis script will:")
    print("1. Read your resource document")
    print("2. Chunk it into manageable pieces")
    print("3. Generate embeddings using Google's API")
    print("4. Create a FAISS vector database")
    print("5. Save everything for use by the chatbot")
    
    # Path to resource document
    resource_file = "com/mhire/app/data/resources/raw/substance_use_resource.txt"
    
    # Check if file exists
    if not os.path.exists(resource_file):
        print(f"\n❌ ERROR: Resource file not found!")
        print(f"Expected location: {resource_file}")
        print("\nPlease:")
        print("1. Create the directory: com/mhire/app/data/resources/raw/")
        print("2. Add your resource document as: substance_use_resource.txt")
        return
    
    # Step 1: Read resource document
    print(f"\n{'='*60}")
    print("STEP 1: Reading Resource Document")
    print(f"{'='*60}")
    print(f"📄 Loading: {resource_file}")
    
    try:
        with open(resource_file, 'r', encoding='utf-8') as f:
            resource_text = f.read()
        
        print(f"✓ Document loaded successfully")
        print(f"  Characters: {len(resource_text):,}")
        print(f"  Lines: {resource_text.count(chr(10)):,}")
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")
        return
    
    # Step 2: Chunk the document
    print(f"\n{'='*60}")
    print("STEP 2: Chunking Document")
    print(f"{'='*60}")
    print("✂️ Splitting document into sections...")
    
    try:
        chunks = chunk_by_section(resource_text, max_chunk_size=500)
        print(f"✓ Created {len(chunks)} chunks")
        
        # Show sample chunk
        if chunks:
            print(f"\n📝 Sample chunk:")
            print(f"  Section: {chunks[0]['section']}")
            print(f"  Title: {chunks[0]['title']}")
            print(f"  Content: {chunks[0]['content'][:100]}...")
    except Exception as e:
        print(f"❌ Error chunking document: {str(e)}")
        return
    
    # Step 3: Create Resource objects
    print(f"\n{'='*60}")
    print("STEP 3: Creating Resource Objects")
    print(f"{'='*60}")
    print("🏗️ Processing chunks into structured resources...")
    
    resources = []
    for i, chunk in enumerate(chunks):
        try:
            resource_type = determine_resource_type(chunk['section'], chunk['title'])
            urgency_level = determine_urgency_level(chunk['section'], chunk['title'])
            contact_info = extract_contact_info(chunk['content'], chunk['title'])
            source_url = extract_source_url(chunk['content'])
            
            resource = Resource(
                content=chunk['content'],
                resource_type=resource_type,
                urgency_level=urgency_level,
                section=chunk['section'],
                title=chunk['title'],
                source_url=source_url,
                contact_info=contact_info
            )
            resources.append(resource)
            
            if (i + 1) % 10 == 0:
                print(f"  Processed {i + 1}/{len(chunks)} chunks...")
                
        except Exception as e:
            print(f"⚠️ Warning: Error processing chunk {i+1}: {str(e)}")
            continue
    
    print(f"✓ Created {len(resources)} Resource objects")
    
    # Print statistics
    print_statistics(resources)
    
    # Step 4: Generate embeddings
    print(f"\n{'='*60}")
    print("STEP 4: Generating Embeddings")
    print(f"{'='*60}")
    print("🧮 This may take a few minutes depending on the number of resources...")
    print("⚠️ Note: This uses the Google Generative AI API")
    
    try:
        embeddings_service = EmbeddingsService()
        texts = [r.content for r in resources]
        
        embeddings = embeddings_service.generate_embeddings_batch(texts)
        
        print(f"✓ Generated {len(embeddings)} embeddings")
        print(f"  Embedding dimension: {len(embeddings[0])}")
    except Exception as e:
        print(f"❌ Error generating embeddings: {str(e)}")
        print("\nPossible issues:")
        print("- Check your GEMINI_API_KEY in config")
        print("- Verify API quota/rate limits")
        return
    
    # Step 5: Create vector store
    print(f"\n{'='*60}")
    print("STEP 5: Creating FAISS Vector Store")
    print(f"{'='*60}")
    print("💾 Building FAISS index...")
    
    try:
        vector_store = VectorStore()
        vector_store.create_index(resources, embeddings)
        
        print(f"✓ Vector store created successfully")
        print(f"  Index size: {vector_store.index.ntotal} vectors")
        print(f"  Saved to: {vector_store.index_path}")
    except Exception as e:
        print(f"❌ Error creating vector store: {str(e)}")
        return
    
    # Step 6: Test the vector store
    print(f"\n{'='*60}")
    print("STEP 6: Testing Vector Store")
    print(f"{'='*60}")
    
    test_queries = [
        "I'm having intense cravings right now",
        "Where can I find treatment?",
        "I need emergency help"
    ]
    
    print("🧪 Running test searches...\n")
    
    for query in test_queries:
        print(f"Query: \"{query}\"")
        test_resources, test_scores = vector_store.search(query, top_k=2)
        
        if test_resources:
            for i, (resource, score) in enumerate(zip(test_resources, test_scores), 1):
                print(f"  {i}. {resource.title} (score: {score:.3f})")
        else:
            print("  No results found")
        print()
    
    # Final summary
    print("=" * 60)
    print("✅ SETUP COMPLETE!")
    print("=" * 60)
    print("\n🎉 Your vector database is ready to use!")
    print("\nNext steps:")
    print("1. Start your chatbot: python com/mhire/app/main.py")
    print("2. Test with example queries")
    print("3. Monitor logs to see RAG in action")
    print("\nThe system will automatically:")
    print("- Detect user intent")
    print("- Retrieve relevant resources")
    print("- Integrate them into responses")
    print("\nAll without changing your input/output format! 🚀")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)