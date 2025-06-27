import streamlit as st
# st.markdown("<h2 style='font-size:28px;'>🩺 MediMento - 증상 기반 질병 예측 및 약 추천 서비스</h2>", unsafe_allow_html=True)

accounts = {
    "user1": "1234"
}

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

def login():
    st.title("로그인")
    username = st.text_input("사용자 이름")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        if username in accounts and accounts[username] == password:
            st.session_state["username"] = username
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("사용자 이름 또는 비밀번호가 잘못되었습니다.")
    return False

def main_background():
    username = st.session_state["username"]

    st.title(f"🩺 MediMento")
    st.subheader(f"{username} 님, 환영합니다!")
    st.header('st.selectbox')
    option = st.selectbox(
        '증상을 선택해주세요.',
        ('발열', '기침', '피로', '호흡 곤란')
    )

    if option == '발열':
        st.write('???')
    elif option == '기침':
        st.write

if st.session_state["logged_in"]:
    main_background()
else:
    login()

