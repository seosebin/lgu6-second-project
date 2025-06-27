import streamlit as st

# 로그인 여부 확인
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🚫 로그인 후 이용 가능한 페이지입니다.")
    st.stop()

st.title('증상 입력')

option = st.multiselect(
    '증상을 선택해 주세요.',
    ('발열', '기침', '피로', '호흡곤란')
)

if st.button("선택하기"):
    if not option:
        st.warning("증상을 선택해주세요.")
    else:
        st.success("증상 분석 결과:")