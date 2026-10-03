import os
import streamlit as st

def get_groq_api_key():
    # خواندن امن کلید از Streamlit Secrets یا .env
    if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
        return st.secrets["GROQ_API_KEY"]
    return os.getenv("GROQ_API_KEY", "")

def get_groq_model():
    # مدل استاندارد، پایدار و رسمی Gemma 2 9B
    if hasattr(st, "secrets") and "GROQ_MODEL" in st.secrets:
        return st.secrets["GROQ_MODEL"]
    return os.getenv("GROQ_MODEL", "gemma2-9b-it")
