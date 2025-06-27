import streamlit as st
from streamlit_option_menu import option_menu

st.title("사용자 증상을 분석해 질병을 예측하고 약을 추천하는 서비스")

signup_page = st.Page("signup.py", title="회원가입", icon=":material/add_circle:")
input_page = st.Page("input.py", title="질병 입력", icon=":material/edit:")
 
pg = st.navigation([signup_page, input_page])
pg.run()