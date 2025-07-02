import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import pandas as pd
import altair as alt

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
        disease_translation = {
            'Influenza': '독감',
            'Asthma': '천식',
            'Eczema': '습진',
            'Depression': '우울증',
            'Liver Cancer': '간암',
            'Stroke': '뇌졸중',
            'Urinary Tract Infection': '요로감염',
            'Bipolar Disorder': '조울증',
            'Bronchitis': '기관지염',
            'Cerebral Palsy': '뇌성마비',
            'Colorectal Cancer': '대장암',
            'Hypertensive Heart Disease': '고혈압성 심장병',
            'Multiple Sclerosis': '다발성 경화증',
            'Myocardial Infarction (Heart...': '심근경색증',
            'Urinary Tract Infection (UTI)': '요로감염(UTI)',
            'Common Cold': '감기',
            'Migraine': '편두통',
            'Pneumonia': '폐렴',
            'Cirrhosis': '간경변증',
            'Conjunctivitis (Pink Eye)': '결막염',
            'Gastroenteritis': '위장염',
            'Hyperthyroidism': '갑상선기능항진증',
            'Kidney Cancer': '신장암',
            'Liver Disease': '간질환',
            'Malaria': '말라리아',
            'Pancreatitis': '췌장염',
            'Rheumatoid Arthritis': '류마티스 관절염',
            'Spina Bifida': '척추 이분증',
            'Ulcerative Colitis': '궤양성 대장염',
            'Anxiety Disorders': '불안장애',
            'Diabetes': '당뇨병',
            'Osteoarthritis': '골관절염',
            'Klinefelter Syndrome': '클라인펠터 증후군',
            'Chickenpox': '수두',
            'Coronary Artery Disease': '관상동맥질환',
            'Eating Disorders (Anorexia,...': '섭식장애(거식증 등)',
            'Fibromyalgia': '섬유근육통',
            'Hemophilia': '혈우병',
            'Hypoglycemia': '저혈당증',
            'Lymphoma': '림프종',
            'Psoriasis': '건선',
            'Tuberculosis': '결핵',
            'Hypothyroidism': '갑상선기능저하증',
            'Kidney Disease': '신장질환',
            'Allergic Rhinitis': '알레르기 비염',
            'Cataracts': '백내장',
            "Crohn's Disease": '크론병',
            'Hypertension': '고혈압',
            'Osteoporosis': '골다공증',
            'Pneumocystis Pneumonia (PCP)': '폐포자충 폐렴',
            'Scoliosis': '척추측만증',
            'Sickle Cell Anemia': '겸상 적혈구 빈혈',
            'Tetanus': '파상풍',
            'Down Syndrome': '다운 증후군',
            'Ebola Virus': '에볼라 바이러스',
            'Lyme Disease': '라임병',
            'Pancreatic Cancer': '췌장암',
            'Pneumothorax': '기흉',
            'Hemorrhoids': '치질',
            'Polycystic Ovary Syndrome (PCOS)': '다낭성 난소 증후군',
            'Systemic Lupus Erythematosus...': '전신홍반루푸스',
            'Typhoid Fever': '장티푸스',
            'Chronic Kidney Disease': '만성 신장질환',
            'Hepatitis B': 'B형 간염',
            "Parkinson's Disease": '파킨슨병',
            'Prader-Willi Syndrome': '프래더-윌리 증후군',
            'Thyroid Cancer': '갑상선암',
            "Alzheimer's Disease": '알츠하이머병',
            'Chronic Obstructive Pulmonary Disease (COPD)': '만성폐쇄성폐질환(COPD)',
            'Dementia': '치매',
            'Diverticulitis': '게실염',
            'Lung Cancer': '폐암',
            'Mumps': '유행성이하선염(볼거리)',
            'Gout': '통풍',
            'Testicular Cancer': '고환암',
            'Tonsillitis': '편도염',
            'Williams Syndrome': '윌리엄스 증후군'
        }

        diseases = df['disease'].unique()
        disease_kor_list = [disease_translation.get(d, d) for d in diseases]
        selected_kor = st.selectbox("질병을 선택하세요", disease_kor_list)

        kor_to_eng = {v: k for k, v in disease_translation.items()}
        selected_eng = kor_to_eng.get(selected_kor, selected_kor)

        filtered_df = df[df['disease'] == selected_eng]

        bins = [0, 9, 19, 29, 39, 49, 59, 69, 150]
        labels = ['0-9세','10대','20대','30대','40대','50대','60대','70세 이상']
        filtered_df['age_group'] = pd.cut(filtered_df['age'], bins=bins, labels=labels, right=True)

        age_dist = filtered_df['age_group'].value_counts().sort_index()
        chart_data = pd.DataFrame({
            "연령대": age_dist.index,
            "인원수": age_dist.values
        })

        import altair as alt

        chart = alt.Chart(chart_data).mark_circle(size=100).encode(
            x=alt.X('연령대:N', title='연령대'),
            y=alt.Y('인원수:Q', title='인원수',
                    scale=alt.Scale(zero=True),
                    axis=alt.Axis(format='d')),
            tooltip=['연령대', '인원수']
        ).properties(
            width=600,
            height=400,
            title=f"🧬 {selected_kor}의 연령대 분포 (Scatter)"
        )

        st.altair_chart(chart, use_container_width=True)

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
        # 빈 문자열, 공백 제거도 같이 하기
        all_meds = pd.concat([
            df['item1'], df['item2'], df['item3']
        ]).dropna()
        
        # 공백이나 빈 문자열 제거
        all_meds = all_meds[all_meds.str.strip() != ""]

        freq = all_meds.value_counts().head(10)
        
        st.bar_chart(freq)

        with st.expander("약별 추천 횟수 보기"):
            freq_df = freq.reset_index()
            freq_df.columns = ["약 이름", "추천 횟수"]
            st.dataframe(freq_df)