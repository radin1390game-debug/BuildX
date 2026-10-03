import sys
import streamlit as st
from auth import add_user, login_user
from agent import run_lead_finder

st.set_page_config(
    page_title="BuildX - Agentic Lead Finder",
    layout="wide"
)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.authenticated:
    st.title("BuildX Lead Finder")
    st.subheader("لطفاً وارد شوید یا ثبت‌نام کنید.")

    tab_login, tab_signup = st.tabs(["ورود", "ثبت‌نام"])

    with tab_login:
        login_user_input = st.text_input("نام کاربری", key="login_user")
        login_pass_input = st.text_input("رمز عبور", type="password", key="login_pass")
        if st.button("ورود", type="primary"):
            if login_user(login_user_input, login_pass_input):
                st.session_state.authenticated = True
                st.session_state.username = login_user_input
                st.success("ورود با موفقیت انجام شد.")
                st.rerun()
            else:
                st.error("نام کاربری یا رمز عبور اشتباه است.")

    with tab_signup:
        signup_user_input = st.text_input("نام کاربری جدید", key="signup_user")
        signup_pass_input = st.text_input("رمز عبور جدید", type="password", key="signup_pass")
        if st.button("ثبت‌نام"):
            if signup_user_input and signup_pass_input:
                if add_user(signup_user_input, signup_pass_input):
                    st.success("حساب کاربری ساخته شد.")
                else:
                    st.warning("این نام کاربری قبلاً ثبت شده است.")
            else:
                st.error("لطفاً تمام فیلدها را پر کنید.")

else:
    st.sidebar.title(f"کاربر: {st.session_state.username}")
    if st.sidebar.button("خروج"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()

    st.title("Agentic Lead Finder")
    st.markdown("تحلیل پیام‌های جوامع آنلاین جهت شناسایی فرصت‌های فروش")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("ورودی اطلاعات")
        product_context = st.text_area(
            "توضیحات محصول / خدمت:",
            height=150,
            placeholder="مثال: ارائه بسته‌های آموزش جامع پایتون..."
        )
        raw_message = st.text_area(
            "پیام دریافتی:",
            height=150,
            placeholder="مثال: سلام دوستان، کسی دوره خوب پایتون سراغ داره؟"
        )
        api_key_override = st.text_input("کلید API اختیاری:", type="password")

        submit_btn = st.button("تحلیل پیام", type="primary", use_container_width=True)

    with col2:
        st.subheader("خروجی تحلیل")
        if submit_btn:
            if not product_context or not raw_message:
                st.warning("لطفاً هم توضیحات محصول و هم پیام را وارد کنید.")
            else:
                with st.spinner("در حال تحلیل..."):
                    result = run_lead_finder(
                        raw_message=raw_message,
                        product_context=product_context,
                        api_key=api_key_override if api_key_override else None
                    )

                    if result.get("is_potential_lead"):
                        st.success("این پیام یک لید بالقوه تشخیص داده شد.")
                    else:
                        st.info("این پیام به‌عنوان لید مناسب ارزیابی نشد.")

                    st.metric("امتیاز ارتباط", f"{result.get('relevance_score', 0)} / 100")
                    st.write("**تحلیل:**", result.get("reasoning", ""))
                    st.write("**پاسخ پیشنهادی:**")
                    st.info(result.get("suggested_reply", "پاسخی تولید نشد."))

                    with st.expander("خروجی JSON"):
                        st.json(result)

if __name__ == "__main__":
    if not st.runtime.exists():
        from streamlit.web import cli as stcli
        sys.argv = ["streamlit", "run", __file__]
        sys.exit(stcli.main())