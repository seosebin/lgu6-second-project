import streamlit as st

# 로그인 여부 확인
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🚫 로그인 후 이용 가능한 페이지입니다.")
    st.stop()

st.title('마이페이지')

st.button("회원정보 수정", key = 'acc-edit_button')