import os
import streamlit as st

def get_groq_api_key():
    if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
        return st.secrets["GROQ_API_KEY"]
    return os.getenv("GROQ_API_KEY", "")

def get_groq_model():
    # تنظیم مستقیم مدل پایدار Gemma 2 9B جهت جلوگیری از ارور مدل‌های قدیمی
    if hasattr(st, "secrets") and "GROQ_MODEL" in st.secrets and st.secrets["GROQ_MODEL"] != "llama-3.3-70b-specdec":
        return st.secrets["GROQ_MODEL"]
    return "gemma2-9b-it"
