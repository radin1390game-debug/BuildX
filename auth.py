import streamlit as st

def check_password():
    """
    بررسی احراز هویت کاربر جهت ورود به پلتفرم
    """
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.markdown("### ورود به پلتفرم Agentic Lead Finder")
    
    with st.form("login_form"):
        username = st.text_input("نام کاربری:")
        password = st.text_input("رمز عبور:", type="password")
        submit = st.form_submit_button("ورود")

        if submit:
            # نام کاربری و رمز عبور پیش‌فرض (قابل تغییر در Secrets)
            correct_user = st.secrets.get("ADMIN_USER", "admin") if hasattr(st, "secrets") else "admin"
            correct_pass = st.secrets.get("ADMIN_PASS", "123456") if hasattr(st, "secrets") else "123456"

            if username == correct_user and password == correct_pass:
                st.session_state.authenticated = True
                st.success("ورود موفقیت‌آمیز بود.")
                st.rerun()
            else:
                st.error("نام کاربری یا رمز عبور اشتباه است.")
                
    return False

def logout():
    """
    خروج از حساب کاربری
    """
    st.session_state.authenticated = False
    st.rerun()import streamlit as st

def check_password():
    """
    بررسی احراز هویت کاربر جهت ورود به پلتفرم
    """
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.markdown("### ورود به پلتفرم Agentic Lead Finder")
    
    with st.form("login_form"):
        username = st.text_input("نام کاربری:")
        password = st.text_input("رمز عبور:", type="password")
        submit = st.form_submit_button("ورود")

        if submit:
            # نام کاربری و رمز عبور پیش‌فرض (قابل تغییر در Secrets)
            correct_user = st.secrets.get("ADMIN_USER", "admin") if hasattr(st, "secrets") else "admin"
            correct_pass = st.secrets.get("ADMIN_PASS", "123456") if hasattr(st, "secrets") else "123456"

            if username == correct_user and password == correct_pass:
                st.session_state.authenticated = True
                st.success("ورود موفقیت‌آمیز بود.")
                st.rerun()
            else:
                st.error("نام کاربری یا رمز عبور اشتباه است.")
                
    return False

def logout():
    """
    خروج از حساب کاربری
    """
    st.session_state.authenticated = False
    st.rerun()
