"""Text processing utilities for chunking and cleaning"""

import re
from typing import List, Dict

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text.strip()


def chunk_by_section(text: str, max_chunk_size: int = 500) -> List[Dict[str, str]]:
    """
    Chunk resource document by sections
    Returns list of dicts with 'content', 'section', 'title'
    """
    chunks = []
    
    # Split by main sections (numbered sections like "1.", "2.", etc.)
    sections = re.split(r'\n(\d+\.\s+[A-Z\s]+)\n', text)
    
    current_section = "0"
    current_title = "Introduction"
    
    for i, part in enumerate(sections):
        # Check if this is a section header
        if re.match(r'^\d+\.\s+[A-Z\s]+$', part.strip()):
            match = re.match(r'^(\d+)\.\s+(.+)$', part.strip())
            if match:
                current_section = match.group(1)
                current_title = match.group(2).strip()
        elif part.strip():
            # This is content
            # Further split by subsections
            subsections = re.split(r'\n(\d+\.\d+(?:\.\d+)?)\s+(.+)\n', part)
            
            for j in range(0, len(subsections), 3):
                content = subsections[j].strip()
                if not content:
                    continue
                    
                subsection_num = subsections[j+1] if j+1 < len(subsections) else ""
                subsection_title = subsections[j+2] if j+2 < len(subsections) else current_title
                
                # Clean content
                content = clean_text(content)
                
                # Split large content into smaller chunks
                if len(content) > max_chunk_size:
                    words = content.split()
                    for k in range(0, len(words), max_chunk_size//5):
                        chunk_content = ' '.join(words[k:k+max_chunk_size//5])
                        chunks.append({
                            'content': chunk_content,
                            'section': f"{current_section}.{subsection_num}" if subsection_num else current_section,
                            'title': subsection_title
                        })
                else:
                    chunks.append({
                        'content': content,
                        'section': f"{current_section}.{subsection_num}" if subsection_num else current_section,
                        'title': subsection_title
                    })
    
    return chunks


def extract_keywords(text: str, top_n: int = 10) -> List[str]:
    """Extract important keywords from text"""
    # Simple keyword extraction based on frequency
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    
    # Common words to ignore
    stop_words = {'that', 'this', 'with', 'from', 'have', 'will', 'your', 'their', 
                  'about', 'would', 'there', 'which', 'when', 'them', 'been', 'than'}
    
    # Filter and count
    word_freq = {}
    for word in words:
        if word not in stop_words:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort and return top N
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:top_n]]