import streamlit as st

'''
# 로그인 여부 확인
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🚫 로그인 후 이용 가능한 페이지입니다.")
    st.stop()
'''

st.title('👩‍💻마이페이지')

col1, col2, col3 = st.columns(3)

with col1:

    if "medic_records" not in st.session_state:
        st.session_state["medic_records"] = False

    if st.button("나의 진단 내역", key = 'medic_records_btn'):
        st.session_state["medic_records"] = True

    def medic_rcds_background():
        st.subheader("나의 진단 내역")
        st.markdown("🏣 증상: ")
    
    
    
    if st.session_state["medic_records"]:
        medic_rcds_background()


# 증상 : 발열, 기침, 피로, 호흡 곤란
# 예상되는 질병
# 예측된 질병과 관련된 일반 의약품

with col2:
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