"""Embedding generation service using Google Generative AI"""

from typing import List
from google import genai
from com.mhire.app.config.config import Config
from com.mhire.app.logger.logger import ChatEndpoint

logger = ChatEndpoint.setup_chat_logger()

class EmbeddingsService:
    """Service for generating embeddings using Google's embedding model"""
    
    def __init__(self):
        config = Config()
        # Create client with API key using new google.genai API
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.model_name = "gemini-embedding-001"
        logger.info(f"EmbeddingsService initialized with model: {self.model_name}")
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            result = self.client.models.embed_content(
                model=self.model_name,
                contents=text
            )
            # New API returns embeddings in a different structure
            return result.embeddings[0].values
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            logger.info(f"Generating embeddings for {len(texts)} texts...")
            embeddings = []
            
            # Process in batches to avoid rate limits
            batch_size = 100
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i+batch_size]
                for text in batch:
                    embedding = self.generate_embedding(text)
                    embeddings.append(embedding)
                    
                logger.debug(f"Processed {min(i+batch_size, len(texts))}/{len(texts)} embeddings")
            
            logger.info(f"✓ Successfully generated {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            raise
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a search query
        
        Args:
            query: Search query text
            
        Returns:
            Embedding vector for the query
        """
        try:
            result = self.client.models.embed_content(
                model=self.model_name,
                contents=query
            )
            # New API returns embeddings in a different structure
            return result.embeddings[0].values
        except Exception as e:
            logger.error(f"Error generating query embedding: {str(e)}")
            raise