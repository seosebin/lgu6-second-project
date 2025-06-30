import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import pandas as pd

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

if selected == "증상":
    st.subheader("연령대별 증상 분포 분석")

    conn = sqlite3.connect('users.db')
    df_users = pd.read_sql_query("SELECT username AS user_id, age FROM users", conn)
    df_symp = pd.read_sql_query("""
        SELECT user_id, fever, cough, fatigue, difficulty_breathing FROM user_symptoms                  
    """, conn)
    conn.close()

    df = df_users.merge(df_symp, on='user_id', how='inner')

    bins = [0, 9, 19, 29, 39, 49, 59, 69, 150]
    labels = ['0-9','10-19','20-29','30-39','40-49','50-59','60-69','70+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)

    group = df.groupby('age_group')[['fever','cough','fatigue','difficulty_breathing']].mean()
    group.columns = ['발열', '기침', '피로', '호흡곤란']
    st.bar_chart(group)