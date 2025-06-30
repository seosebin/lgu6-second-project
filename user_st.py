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

if selected == "질병":
    st.subheader("질병별 나이 분포")

    conn = sqlite3.connect('users.db')
    df_users = pd.read_sql_query("SELECT username AS user_id, age FROM users", conn)
    df_details = pd.read_sql_query("SELECT user_id, disease FROM user_details", conn)
    conn.close()

    df = df_details.merge(df_users, on="user_id", how="inner")

    if df.empty:
        st.info("표시할 질병 데이터가 없습니다.")
    else:
        diseases = df['disease'].unique()
        selected_disease = st.selectbox("질병을 선택하세요", diseases)

        filtered_df = df[df['disease'] == selected_disease]

        bins = [0, 9, 19, 29, 39, 49, 59, 69, 150]
        labels = ['0-9세','10대','20대','30대','40대','50대','60대','70세 이상']
        filtered_df['age_group'] = pd.cut(filtered_df['age'], bins=bins, labels=labels, right=True)

        age_dist = filtered_df['age_group'].value_counts().sort_index()
        chart_data = pd.DataFrame({
            "연령대": age_dist.index,
            "인원수": age_dist.values
        })

        st.write(f"### 🧬 {selected_disease}의 연령대 분포 (Scatter Chart)")
        st.scatter_chart(chart_data.rename(columns={"연령대": "index"}).set_index("index"))

elif selected == "증상":
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

elif selected == "약":
    st.subheader("많이 추천된 약 빈도")
    conn = sqlite3.connect('users.db')
    df = pd.read_sql_query("SELECT item1, item2, item3 FROM user_details", conn)
    conn.close()

    if df.empty:
        st.info("추천된 약 정보가 없습니다")
    else:
        all_meds = pd.concat([
            df['item1'], df['item2'], df['item3']
        ]).dropna()
        freq = all_meds.value_counts().head(10)
        st.bar_chart(freq)

        with st.expander("약별 추천 횟수 보기"):
            st.dataframe(freq.reset_index().rename(columns={"index": "약 이름", "count": "추천 횟수"}))