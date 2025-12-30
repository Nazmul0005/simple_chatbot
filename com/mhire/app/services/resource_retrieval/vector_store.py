"""FAISS vector store for resource retrieval"""

import os
import json
import pickle
from typing import List, Dict, Tuple, Optional
import numpy as np
import faiss
from com.mhire.app.models.resource_models import Resource, ResourceType
from com.mhire.app.services.resource_retrieval.embeddings_service import EmbeddingsService
from com.mhire.app.logger.logger import ChatEndpoint

logger = ChatEndpoint.setup_chat_logger()

class VectorStore:
    """FAISS-based vector store for resource retrieval"""
    
    def __init__(self, index_path: str = "com/mhire/app/data/vector_db"):
        """
        Initialize vector store
        
        Args:
            index_path: Path to store FAISS index and metadata
        """
        self.index_path = index_path
        self.index_file = os.path.join(index_path, "faiss_index.bin")
        self.metadata_file = os.path.join(index_path, "metadata.pkl")
        
        self.embeddings_service = EmbeddingsService()
        self.index: Optional[faiss.Index] = None
        self.metadata: List[Dict] = []
        self.dimension = 3072  # Google embedding-001 dimension
        
        # Create directory if it doesn't exist
        os.makedirs(index_path, exist_ok=True)
        
        logger.info(f"VectorStore initialized at: {index_path}")
    
    def create_index(self, resources: List[Resource], embeddings: List[List[float]]):
        """
        Create FAISS index from resources and embeddings
        
        Args:
            resources: List of Resource objects
            embeddings: List of embedding vectors
        """
        try:
            logger.info(f"Creating FAISS index with {len(resources)} resources...")
            
            # Convert embeddings to numpy array
            embeddings_array = np.array(embeddings, dtype=np.float32)
            
            # Create FAISS index (using L2 distance)
            self.index = faiss.IndexFlatL2(self.dimension)
            self.index.add(embeddings_array)
            
            # Store metadata
            self.metadata = [
                {
                    'content': res.content,
                    'resource_type': res.resource_type.value,
                    'urgency_level': res.urgency_level,
                    'section': res.section,
                    'title': res.title,
                    'source_url': res.source_url,
                    'contact_info': res.contact_info
                }
                for res in resources
            ]
            
            # Save to disk
            self.save()
            
            logger.info(f"✓ FAISS index created successfully with {self.index.ntotal} vectors")
        except Exception as e:
            logger.error(f"Error creating FAISS index: {str(e)}")
            raise
    
    def save(self):
        """Save FAISS index and metadata to disk"""
        try:
            faiss.write_index(self.index, self.index_file)
            with open(self.metadata_file, 'wb') as f:
                pickle.dump(self.metadata, f)
            logger.info(f"✓ Vector store saved to {self.index_path}")
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            raise
    
    def load(self) -> bool:
        """
        Load FAISS index and metadata from disk
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(self.index_file) or not os.path.exists(self.metadata_file):
                logger.warning("Vector store files not found")
                return False
            
            self.index = faiss.read_index(self.index_file)
            with open(self.metadata_file, 'rb') as f:
                self.metadata = pickle.load(f)
            
            logger.info(f"✓ Vector store loaded with {self.index.ntotal} vectors")
            return True
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            return False
    
    def search(
        self, 
        query: str, 
        top_k: int = 3,
        urgency_filter: Optional[str] = None,
        resource_type_filter: Optional[ResourceType] = None
    ) -> Tuple[List[Resource], List[float]]:
        """
        Search for relevant resources
        
        Args:
            query: Search query
            top_k: Number of results to return
            urgency_filter: Filter by urgency level ("emergency", "critical", "general")
            resource_type_filter: Filter by resource type
            
        Returns:
            Tuple of (resources, relevance_scores)
        """
        try:
            if self.index is None:
                logger.error("Vector store not initialized. Call load() first.")
                return [], []
            
            logger.info(f"🔍 Searching vector store for: '{query[:50]}...'")
            logger.info(f"Filters - Urgency: {urgency_filter}, Type: {resource_type_filter}")
            
            # Generate query embedding
            query_embedding = self.embeddings_service.generate_query_embedding(query)
            query_vector = np.array([query_embedding], dtype=np.float32)
            
            # Search FAISS index (get more results for filtering)
            search_k = top_k * 5 if urgency_filter or resource_type_filter else top_k
            distances, indices = self.index.search(query_vector, min(search_k, self.index.ntotal))
            
            # Filter and collect results
            resources = []
            scores = []
            
            for idx, distance in zip(indices[0], distances[0]):
                if idx == -1:  # FAISS returns -1 for empty results
                    continue
                
                meta = self.metadata[idx]
                
                # Apply filters
                if urgency_filter and meta['urgency_level'] != urgency_filter:
                    continue
                if resource_type_filter and meta['resource_type'] != resource_type_filter.value:
                    continue
                
                # Convert distance to similarity score (0-1, higher is better)
                similarity = 1 / (1 + distance)
                
                resource = Resource(
                    content=meta['content'],
                    resource_type=ResourceType(meta['resource_type']),
                    urgency_level=meta['urgency_level'],
                    section=meta['section'],
                    title=meta['title'],
                    source_url=meta.get('source_url'),
                    contact_info=meta.get('contact_info')
                )
                
                resources.append(resource)
                scores.append(float(similarity))
                
                if len(resources) >= top_k:
                    break
            
            logger.info(f"✓ Found {len(resources)} matching resources")
            if resources:
                logger.debug(f"Top result: {resources[0].title} (score: {scores[0]:.3f})")
            
            return resources, scores
            
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            return [], []