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

st.subheader('해당사항')

options = ["낮음", "정상", "높음"]
selection1 = st.segmented_control(
    "혈압", options, selection_mode="single",
    key="chole_lv"
)

if selection1 is not None:
    st.markdown(f"측정된 혈압 수치는 {selection1}입니다.")

options = ["낮음", "정상", "높음"]
selection2 = st.segmented_control(
    "콜레스테롤", options, selection_mode="single",
    key="blood_prs_lv"
)
if selection2 is not None:
    st.markdown(f"측정된 콜레스테롤 수치는 {selection2}입니다.")


if st.button("선택하기"):
    if not option:
        st.warning("증상을 선택해주세요.")
    else:
        st.success("증상 분석 결과:")