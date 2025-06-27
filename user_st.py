import streamlit as st
from streamlit_option_menu import option_menu

# 로그인 여부 확인
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🚫 로그인 후 이용 가능한 페이지입니다.")
    st.stop() 

st.title('전체 사용자 통계')

if st.session_state.get('switch_button', False):
    st.session_state['menu_option'] = (st.session_state.get('menu_option', 0) + 1) % 4
    manual_select = st.session_state['menu_option']
else:
    manual_select = None
    
selected = option_menu(None, ["질병", "증상", "약"], 
    icons=['activity', 'thermometer', 'capsule'],
    orientation="horizontal", 
    manual_select=manual_select,
    key='menu_4'
)