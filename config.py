import os
import streamlit as st
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env در صورت وجود
load_dotenv()

def get_groq_api_key():
    # 1. اولویت اول: خواندن از Streamlit Secrets
    if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
        return st.secrets["GROQ_API_KEY"]
    # 2. اولویت دوم: خواندن از فایل .env یا متغیرهای سیستم
    return os.getenv("GROQ_API_KEY", "")

def get_groq_model():
    if hasattr(st, "secrets") and "GROQ_MODEL" in st.secrets:
        return st.secrets["GROQ_MODEL"]
    return os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
