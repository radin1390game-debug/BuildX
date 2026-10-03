import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatil")
    TEMPERATURE = 0.1
    
    @staticmethod
    def get_api_key(override_key: Optional[str] = None) -> str:
        api_key = override_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found")
        return api_key.strip()
