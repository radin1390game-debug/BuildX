import streamlit as st
import sqlite3
import hashlib

# ساخت و اتصال به دیتابیس کاربران
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# هش کردن رمز عبور برای امنیت بالا
def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# ثبت نام کاربر جدید
def register_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, make_hash(password)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# بررسی نام کاربری و رمز عبور برای ورود
def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, make_hash(password)))
    data = c.fetchall()
    conn.close()
    return data

def check_password():
    init_db()
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.markdown("### ورود / ثبت نام در Agentic Lead Finder")
    
    # تب‌های ورود و ثبت‌نام
    tab_login, tab_register = st.tabs(["ورود به حساب", "ایجاد حساب جدید"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("نام کاربری:")
            password = st.text_input("رمز عبور:", type="password")
            submit_login = st.form_submit_button("ورود")

            if submit_login:
                if username and password:
                    if login_user(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("ورود موفقیت‌آمیز بود.")
                        st.rerun()
                    else:
                        st.error("نام کاربری یا رمز عبور اشتباه است.")
                else:
                    st.warning("لطفاً تمامی فیلدها را پر کنید.")

    with tab_register:
        with st.form("register_form"):
            new_user = st.text_input("نام کاربری جدید:")
            new_pass = st.text_input("رمز عبور جدید:", type="password")
            confirm_pass = st.text_input("تکرار رمز عبور:", type="password")
            submit_reg = st.form_submit_button("ثبت نام")

            if submit_reg:
                if not new_user or not new_pass:
                    st.warning("لطفاً نام کاربری و رمز عبور را وارد کنید.")
                elif new_pass != confirm_pass:
                    st.error("رمز عبور و تکرار آن یکسان نیستند.")
                else:
                    if register_user(new_user, new_pass):
                        st.success("حساب کاربری با موفقیت ساخته شد! حالا می‌توانید از تب 'ورود' وارد شوید.")
                    else:
                        st.error("این نام کاربری قبلاً ثبت شده است. نام دیگری انتخاب کنید.")

    return False

def logout():
    st.session_state.authenticated = False
    if "username" in st.session_state:
        del st.session_state.username
    st.rerun()
