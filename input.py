import streamlit as st
import joblib
import pandas as pd
import sqlite3
from db_data import create_user_symptoms_table, create_user_details_table
from db_data import insert_user_details, insert_user_symptoms

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🚫 로그인 후 이용 가능한 페이지입니다.")
    st.stop()

def get_user_info_from_db(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT age, gender FROM users WHERE username = ?"
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        age, gender = row
        return {'age': age, 'gender': gender}
    else:
        return {'age': None, 'gender': None}

if "users_id" not in st.session_state:
    st.session_state["users_id"] = 1  # 기본값으로 세팅

user_id = st.session_state["users_id"]
user_info = get_user_info_from_db(user_id)
    
# 모델과 라벨 인코더, 약 데이터 불러오기
loaded_model = joblib.load('predict_model/best_disease_model.joblib')
label_encoder = joblib.load('predict_model/label_encoder.joblib')
medicine_df = pd.read_csv('data/drug_info.csv')

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

st.title('증상 입력 및 질병 예측')

create_user_symptoms_table()
create_user_details_table()

st.title('증상 입력')
user_id = st.session_state["username"]


option = st.multiselect(
    '증상을 선택해 주세요.',
    ('발열', '기침', '피로', '호흡곤란')
)

st.subheader('해당사항')

bp_options = ["낮음", "정상", "높음"]
selection1 = st.segmented_control(
    label="혈압",
    options=bp_options,
    selection_mode="single",
    key="blood_pressure"
)

if selection1:
    st.markdown(f"🩸 측정된 혈압 수치는 **{selection1}** 입니다.")

chol_options = ["낮음", "정상", "높음"]
selection2 = st.segmented_control(
    label="콜레스테롤",
    options=chol_options,
    selection_mode="single",
    key="cholesterol"
)


if selection2:
    st.markdown(f"📈 측정된 콜레스테롤 수치는 **{selection2}** 입니다.")

if st.button("선택하기"):
    if not option:
        st.warning("증상을 최소 하나 선택해주세요.")
    elif not selection1 or not selection2:
        st.warning("혈압과 콜레스테롤을 모두 선택해주세요.")
    else:
        user_info = get_user_info_from_db(user_id)

        new_patient = {
            '열': 'Yes' if '발열' in option else 'No',
            '기침': 'Yes' if '기침' in option else 'No',
            '피로': 'Yes' if '피로' in option else 'No',
            '호흡곤란': 'Yes' if '호흡곤란' in option else 'No',
            '혈압': selection1,
            '콜레스테롤': selection2,
            'Age': user_info.get('age'),
            'Gender': user_info.get('gender')
        }

    

        user_symptoms = []
        for key, value in new_patient.items():
            if key == '호흡곤란' and value == 'Yes':
                user_symptoms.append('호흡')
            if key in ['열', '기침', '피로'] and value == 'Yes':
                user_symptoms.append(key)
            elif key in ['혈압', '콜레스테롤'] and value == '높음':
                user_symptoms.append(key)



        new_patient_df = pd.DataFrame([new_patient])
        predicted_class = loaded_model.predict(new_patient_df)[0]
        predicted_label = label_encoder.inverse_transform([predicted_class])[0]
        
        predicted_label_kor = disease_translation.get(predicted_label, predicted_label)

    

        st.success(f"예측된 질병: {predicted_label_kor}")

        def symptom_match(efficacy_text):
            if pd.isna(efficacy_text):
                return False
            return any(symptom in efficacy_text for symptom in user_symptoms)

        matched_meds = medicine_df[medicine_df['efcyQesitm'].apply(symptom_match)]

        recommended_meds = matched_meds.head(3)

        if not recommended_meds.empty:
            st.subheader("추천 약 정보 (최대 3개)")
            for idx, row in recommended_meds.iterrows():
                st.markdown(f"**{row['itemName']}**")
                st.markdown(f"- 효능: {row['efcyQesitm']}")
                st.markdown(f"- 복용법: {row['useMethodQesitm']}")
                st.markdown(f"- 부작용: {row['seQesitm']}")
                st.markdown("---")
        else:
            st.info("추천할 약이 없습니다.")
        fever = 1 if '발열' in option else 0
        cough = 1 if '기침' in option else 0
        fatigue = 1 if '피로' in option else 0
        difficulty_breathing = 1 if '호흡곤란' in option else 0
        bp_mapping = {"낮음": "low", "정상": "normal", "높음": "high"}
        blood_pressure = bp_mapping.get(selection1)
        cholesterol = bp_mapping.get(selection2)
        
        insert_user_symptoms(
            user_id=user_id,
            fever=fever,
            cough=cough,
            fatigue=fatigue,
            difficulty_breathing=difficulty_breathing,
            blood_pressure=blood_pressure,
            cholesterol=cholesterol
        )
    
        item_names = recommended_meds['itemName'].tolist()
        item1 = item_names[0] if len(item_names) > 0 else ""
        item2 = item_names[1] if len(item_names) > 1 else ""
        item3 = item_names[2] if len(item_names) > 2 else ""

        insert_user_details(
            user_id=user_id,
            symptoms=", ".join(option),
            disease=predicted_label_kor,
            item1=item1,
            item2=item2,
            item3=item3
        )
