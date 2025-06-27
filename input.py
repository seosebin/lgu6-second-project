import streamlit as st

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
