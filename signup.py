import streamlit as st

def signup_page():
    st.title("회원가입")
    with st.form("signup_form"):
        new_username = st.text_input("아이디", placeholder="아이디를 입력해주세요.")
        new_password = st.text_input("비밀번호", type="password", placeholder= "비밀번호를 입력해주세요.")
        gender = st.selectbox(
                "성별",
                ("선택", "남성", "여성")
            )

        age = st.slider("나이", 0, 110, 25)

        agree_required = st.checkbox(
                "[필수] 수집되는 건강정보(사용자가 직접 입력한 증상, 예측된 질병, 추천 약 정보 등)는\n"
                "익명화된 형태로 통계 분석, 질병 시각화, 서비스 개선 등의 목적으로 활용될 수 있습니다.\n"
                "해당 정보는 사용자 식별이 불가능한 방식으로 처리되며, 동의하신 경우에만 수집 및 분석에 사용됩니다."
            )

        agree_optional = st.checkbox(
                "[선택] 건강정보(증상, 질병, 약 관련 입력 데이터)를\n"
                "익명 통계 및 시각화 목적으로 수집·활용하는 데 동의합니다."
            )

        submitted = st.form_submit_button("회원가입")

    if submitted:
              st.success("회원가입이 완료되었습니다!")

if __name__ == "__main__":
    signup_page()

