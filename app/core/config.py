from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Savory Haven Restaurant Chatbot"
    
    # MongoDB Settings
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "restaurant_chatbot")
    
    # LLM Settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    MODEL_NAME: str = "gemini-2.0-flash"
    TEMPERATURE: float = 0.5
    MAX_TOKENS: int = 512
    
    # Vector Store Settings
    VECTOR_STORE_PATH: str = "vectorstore/db_faiss"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Restaurant Settings
    RESTAURANT_NAME: str = "Savory Haven"
    RESTAURANT_DATA_PATH: str = "data/restaurant_data.json"
    
    class Config:
        case_sensitive = True

settings = Settings() 