import streamlit as st
import sqlite3
from db_data import create_user_table


st.markdown("<h2 style='font-size:28px;'>🩺 MediMento - 증상 기반 질병 예측 및 약 추천 서비스</h2>", unsafe_allow_html=True)

def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

create_user_table()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

def login():
    st.subheader("로그인")
    username = st.text_input("사용자 이름")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인", key='login_btn'):
        if authenticate_user(username, password):
            st.session_state["username"] = username
            st.session_state["logged_in"] = True
            st.success(f"{username}님, 환영합니다!")
            st.rerun()
        else:
            st.error("사용자 이름 또는 비밀번호가 잘못되었습니다.")

def main_background():
    username = st.session_state["username"]
    st.subheader(f"{username} 님, 환영합니다!")

if st.session_state["logged_in"]:
    main_background()
    if st.button("로그아웃", key='logout_btn'):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()
else:
    login()