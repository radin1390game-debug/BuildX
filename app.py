import streamlit as st
import json
from datetime import datetime
from auth import check_password, logout
from agent import run_lead_finder

st.set_page_config(
    page_title="Agentic Lead Finder",
    layout="wide",
    initial_sidebar_state="expanded"
)

if not check_password():
    st.stop()

# اصلاح استایل برای شفافیت و خوانایی ۱۰۰٪ متون
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* کارت‌های متمایز با متن روشن و واضح */
    .glass-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    h1, h2, h3, h4, label, p, span {
        color: #f8fafc !important;
    }
    
    /* اصلاح رنگ لایبل‌ها و اینپوت‌ها */
    .stTextArea label, .stTextInput label {
        color: #cbd5e1 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    
    .stTextArea textarea, .stTextInput input {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }
    
    .hero-title {
        color: #818cf8 !important;
        font-size: 2.5rem;
        font-weight: 800;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #4f46e5;
        color: #ffffff !important;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 12px;
    }
    .stButton>button:hover {
        background-color: #4338ca;
    }
    
    .metric-box {
        background-color: #1e1b4b;
        border-left: 4px solid #6366f1;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

if "selected_analysis" not in st.session_state:
    st.session_state.selected_analysis = None

def reset_to_new_search():
    st.session_state.selected_analysis = None

with st.sidebar:
    st.markdown("### Agentic Lead Finder")
    st.caption("پلتفرم ارزیابی هوشمند فرصت‌های فروش v2.5")
    st.divider()
    
    if st.button("تحلیل جدید", key="new_search_btn", use_container_width=True):
        reset_to_new_search()
        st.rerun()
        
    st.divider()
    st.markdown("#### تاریخچه تحلیل‌ها")
    
    if not st.session_state.history:
        st.info("هنوز تحلیلی ثبت نشده است.")
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            real_index = len(st.session_state.history) - 1 - idx
            label = f"{item['timestamp']} - {item['product_desc'][:20]}..."
            if st.button(label, key=f"hist_{real_index}", use_container_width=True):
                st.session_state.selected_analysis = item

    st.markdown("<div style='height: 150px;'></div>", unsafe_allow_html=True)
    st.divider()
    if st.button("خروج از حساب کاربری", type="secondary", use_container_width=True):
        logout()

st.markdown("<h1 class='hero-title'>Agentic Lead Finder</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8;'>موتور هوش مصنوعی ارزیابی خودکار و استخراج فرصت‌های فروش از جوامع آنلاین</p>", unsafe_allow_html=True)
st.write("")

active_item = st.session_state.selected_analysis

default_product = active_item["product_desc"] if active_item else ""
default_message = active_item["user_msg"] if active_item else ""

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### ورودی داده‌ها")
    
    product_desc = st.text_area(
        "توضیحات محصول / خدمت شما:",
        value=default_product,
        placeholder="مثال: ارائه خدمات طراحی وب‌سایت با پایتون و سئو...",
        height=130
    )
    
    user_msg = st.text_area(
        "پیام دریافتی از جامعه آنلاین:",
        value=default_message,
        placeholder="مثال: سلام، کسی هست پروژه طراحی سایت انجام بده؟",
        height=130
    )
    
    api_key_input = st.text_input("کلید API اختصاصی (اختیاری):", type="password")
    
    submit_btn = st.button("شروع تحلیل هوشمند", type="primary")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### نتایج پردازش Agentic")
    
    if submit_btn:
        if not product_desc or not user_msg:
            st.warning("لطفاً تمامی فیلدهای ورودی را تکمیل کنید.")
        else:
            with st.spinner("در حال پردازش با مدل Gemma 2 9B..."):
                try:
                    result = run_lead_finder(product_desc, user_msg, api_key_input if api_key_input else None)
                    
                    history_entry = {
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "product_desc": product_desc,
                        "user_msg": user_msg,
                        "result": result
                    }
                    st.session_state.history.append(history_entry)
                    st.session_state.selected_analysis = history_entry
                    st.rerun()
                except Exception as e:
                    st.error(f"خطا در ارتباط با مدل: {e}")
                    
    elif active_item:
        result = active_item["result"]
        
        if result.get("is_potential_lead"):
            st.success("این پیام به‌عنوان لید واجد شرایط (Potential Lead) ارزیابی شد.")
        else:
            st.info("این پیام به‌عنوان لید مناسب ارزیابی نشد.")
            
        st.markdown(f"""
        <div class='metric-box'>
            <h4 style='margin:0; color:#a5b4fc !important;'>امتیاز ارتباط (Relevance Score)</h4>
            <h2 style='margin:0; color:#ffffff !important;'>{result.get('relevance_score', 0)} / 100</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.write("تحلیل منطقی هوش مصنوعی:")
        st.info(result.get("reasoning", ""))
        
        if result.get("suggested_reply"):
            st.write("پاسخ پیشنهادی جهت ارسال به خریدار:")
            st.code(result.get("suggested_reply", ""), language="markdown")
            
        with st.expander("خروجی ساختاریافته (Raw JSON)"):
            st.json(result)
    else:
        st.caption("ورودی‌ها را وارد کرده و روی دکمه «شروع تحلیل هوشمند» کلیک کنید تا نتایج هوش مصنوعی ظاهر شوند.")
        
    st.markdown("</div>", unsafe_allow_html=True)
