import streamlit as st
import json
from agent import run_lead_finder

st.set_page_config(page_title="Agentic Lead Finder", page_icon="🎯", layout="wide")

st.title("🎯 Agentic Lead Finder")
st.subheader("تحلیل پیام‌های جوامع آنلاین جهت شناسایی فرصت‌های فروش")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("ورودی اطلاعات")
    product_desc = st.text_area("توضیحات محصول / خدمت:", height=120)
    user_msg = st.text_area("پیام دریافتی:", height=120)
    api_key_input = st.text_input("کلید API اختیاری:", type="password")
    
    submit_btn = st.button("تحلیل پیام", type="primary")

with col2:
    st.header("خروجی تحلیل")
    if submit_btn:
        if not product_desc or not user_msg:
            st.warning("لطفاً هم توضیحات محصول و هم پیام دریافتی را وارد کنید.")
        else:
            with st.spinner("در حال تحلیل با مدل Gemma 2..."):
                try:
                    result = run_lead_finder(product_desc, user_msg, api_key_input if api_key_input else None)
                    
                    if result.get("is_potential_lead"):
                        st.success("این پیام به‌عنوان لید مناسب ارزیابی شد!")
                    else:
                        st.info("این پیام به‌عنوان لید مناسب ارزیابی نشد.")
                        
                    st.metric("امتیاز ارتباط", f"{result.get('relevance_score', 0)} / 100")
                    st.write("**تحلیل:**", result.get("reasoning", ""))
                    st.write("**پاسخ پیشنهادی:**", result.get("suggested_reply", ""))
                    
                    with st.expander("خروجی JSON"):
                        st.json(result)
                except Exception as e:
                    st.error(f"خطا در پردازش: {e}")
