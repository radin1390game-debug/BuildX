from langchain_groq import ChatGroq
from config import get_groq_api_key, get_groq_model

def get_agent_llm(custom_api_key=None):
    api_key = custom_api_key if custom_api_key else get_groq_api_key()
    model_name = get_groq_model()
    
    if not api_key:
        raise ValueError("کلید API یافت نشد. لطفاً کلید Groq خود را تنظیم کنید.")

    return ChatGroq(
        groq_api_key=api_key,
        model_name=model_name,
        temperature=0.2
    )
