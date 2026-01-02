import os
from dotenv import load_dotenv
            
load_dotenv()

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        return cls._instance