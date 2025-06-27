import streamlit as st

'''
# 로그인 여부 확인
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🚫 로그인 후 이용 가능한 페이지입니다.")
    st.stop()
'''
st.title('👩‍💻마이페이지')

if "edit_mode" not in st.session_state:
    st.session_state["edit_mode"] = False

if st.button("회원정보 수정", key = 'acc_edit_btn'):
    st.session_state["edit_mode"] = True

def acc_edit_background():
    st.subheader("회원정보수정")
    chg_username = st.text_input("아이디", placeholder="변경할 아이디를 작성해주세요.")
    chg_password = st.text_input("비밀번호", placeholder="변경할 비밀번호를 입력해주세요", type = "password")
    chg_gender = st.selectbox(
                "성별",
                ("선택", "남성", "여성")
            )
    chg_age = st.slider("나이", 0, 110, 25)
    if st.button("수정 완료", key = "submit_edit"):
        st.success("회원정보가 수정되었습니다!")

if st.session_state["edit_mode"]:
    acc_edit_background()