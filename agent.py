import json
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

def run_lead_finder(product_description, received_message, custom_api_key=None):
    """
    تحلیل پیام دریافت شده جهت شناسایی فرصت فروش (Lead)
    """
    llm = get_agent_llm(custom_api_key)
    
    prompt = f"""
    تو یک دستیار هوشمند ارزیابی فرصت‌های فروش (Lead Generation Agent) هستی.
    
    توضیحات محصول/خدمت ما:
    {product_description}
    
    پیام دریافت شده از کاربر/جامعه آنلاین:
    {received_message}
    
    وظیفه تو تحلیل پیام و پاسخ با یک فرمت JSON دقیق شامل موارد زیر است:
    1. is_potential_lead: (bool) آیا این پیام نشان‌دهنده نیازمندی به خدمت/محصول ماست؟ (True/False)
    2. relevance_score: (int) امتیاز مرتبط بودن از 0 تا 100
    3. reasoning: (str) تحلیل کوتاه و دلیل امتیاز داده شده
    4. suggested_reply: (str) پاسخ پیشنهادی کوتاه و حرفه‌ای به خریدار (اگر لید نیست خالی بگذار)
    
    خروجی را فقط و فقط به صورت یک ساختار JSON معتبر تحویل بده و هیچ متن اضافه‌ای قبل یا بعد آن ننویس.
    """
    
    response = llm.invoke(prompt)
    content = response.content.strip()
    
    # تمیزکاری خروجی جهت اطمینان از صحت JSON
    if content.startswith("```json"):
        content = content.replace("```json", "", 1)
    if content.startswith("```"):
        content = content.replace("```", "", 1)
    if content.endswith("```"):
        content = content[:-3]
        
    return json.loads(content.strip())
