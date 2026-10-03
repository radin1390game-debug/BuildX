import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_groq_api_key():
    if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
        return st.secrets["GROQ_API_KEY"]
    return os.getenv("GROQ_API_KEY", "")

def get_groq_model():
    # چک کردن Secrets یا فایل env
    if hasattr(st, "secrets") and "GROQ_MODEL" in st.secrets:
        return st.secrets["GROQ_MODEL"]
    
    # حتماً این نام مدل جدید باشد:
    return os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
