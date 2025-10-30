import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM Configuration
    LLM_API_KEY = os.getenv("GROQ_API_KEY") 
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
    LLM_MODEL = "llama-3.3-70b-versatile"
    
    # Application Settings
    MAX_RESERVATION_DAYS = 30
    MAX_PARTY_SIZE = 20
    DEFAULT_TIMEZONE = "UTC"
    
    # Restaurant Data
    SAMPLE_RESTAURANT_COUNT = 75
    
    # UI Settings
    PAGE_TITLE = "GoodFoods AI Reservation System"
    PAGE_ICON = "🍽️"

config = Config()