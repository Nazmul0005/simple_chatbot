# from motor.motor_asyncio import AsyncIOMotorClient
# from com.mhire.app.config.config import Config
# from datetime import datetime

# import asyncio
# from typing import Optional
# import logging
# import logging.handlers
# from pathlib import Path
# from com.mhire.app.logger.logger import DatabaseManager

# logger = DatabaseManager.setup_logger()


# class DatabaseManager:
#     _instance = None
#     _client = None
#     _db = None
#     _collection = None
#     _session_collection = None
    
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(DatabaseManager, cls).__new__(cls)
#         return cls._instance
    
#     def initialize(self):
#         """Initialize MongoDB connection"""
#         try:
#             logger.info("Attempting to initialize MongoDB connection...")
#             config = Config()
#             self._client = AsyncIOMotorClient(config.MONGODB_URL)
#             self._db = self._client[config.DATABASE_NAME]
#             self._collection = self._db[config.COLLECTION_NAME]
#             self._session_collection = self._db[config.SESSION_COLLECTION_NAME]

#             logger.info(f"Successfully initialized database: {config.DATABASE_NAME}, collection: {config.COLLECTION_NAME}, session collection: {config.SESSION_COLLECTION_NAME}")
        
#         except Exception as e:
#             error_msg = f"Failed to initialize database connection: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise Exception(error_msg) from e
    
#     @property
#     def client(self):
#         try:
#             if self._client is None:
#                 logger.debug("Client not initialized, initializing now...")
#                 self.initialize()
#             return self._client
#         except Exception as e:
#             error_msg = f"Error accessing MongoDB client: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise
    
#     @property
#     def db(self):
#         try:
#             if self._db is None:
#                 logger.debug("Database not initialized, initializing now...")
#                 self.initialize()
#             return self._db
#         except Exception as e:
#             error_msg = f"Error accessing database: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise
    
#     @property
#     def collection(self):
#         try:
#             if self._collection is None:
#                 logger.debug("Collection not initialized, initializing now...")
#                 self.initialize()
#             return self._collection
#         except Exception as e:
#             error_msg = f"Error accessing collection: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise

#     @property
#     def session_collection(self):
#         try:
#             if self._session_collection is None:
#                 logger.debug("Session collection not initialized, initializing now...")
#                 self.initialize()
#             return self._session_collection
#         except Exception as e:
#             error_msg = f"Error accessing session collection: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise
    
#     async def setup_indexes(self):
#         """Create indexes for efficient querying"""
#         try:
#             logger.info("Setting up database indexes...")
#             await self.collection.create_index([("user_id", 1), ("session_id", 1)], unique=True)
#             await self.collection.create_index([("user_id", 1), ("updated_at", -1)])
#             logger.info("Indexes created successfully")
#         except Exception as e:
#             error_msg = f"Failed to create indexes: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise Exception(error_msg) from e
    
    
    
#     async def test_connection(self):
#         """Test MongoDB connection"""
#         try:
#             logger.info("Testing MongoDB connection...")
#             await self.client.admin.command('ping')
#             logger.info("Successfully connected to MongoDB Atlas")
#         except Exception as e:
#             error_msg = f"Failed to connect to MongoDB Atlas: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise Exception(error_msg) from e
    
#     def close(self):
#         """Close MongoDB connection"""
#         try:
#             if self._client:
#                 self._client.close()
#                 logger.info("MongoDB connection closed successfully")
#             else:
#                 logger.warning("Attempted to close connection but client was not initialized")
#         except Exception as e:
#             error_msg = f"Error closing database connection: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             raise Exception(error_msg) from e

# # Singleton instance
# db_manager = DatabaseManager()
