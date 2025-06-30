import streamlit as st
import joblib
import pandas as pd
import sqlite3


def get_user_info_from_db(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT age, gender FROM users WHERE id = ?"
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

st.title('증상 입력 및 질병 예측')

option = st.multiselect(
    '증상을 선택해 주세요.',
    ('발열', '기침', '피로', '호흡곤란')
)

st.subheader('해당사항')

bp_options = ["낮음", "정상", "높음"]
selection1 = st.segmented_control(
    "혈압", bp_options, selection_mode="single", key="chole_lv"
)

if selection1:
    st.markdown(f"🩸 측정된 혈압 수치는 **{selection1}** 입니다.")

chol_options = ["낮음", "정상", "높음"]
selection2 = st.segmented_control(
    "콜레스테롤", chol_options, selection_mode="single", key="blood_prs_lv"
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
        }

        st.write("사용자 증상 데이터:")
        st.json(new_patient)

        user_symptoms = []
        for key, value in new_patient.items():
            if key in ['열', '기침', '피로', '호흡곤란'] and value == 'Yes':
                user_symptoms.append(key)
            elif key in ['혈압', '콜레스테롤'] and value == '높음':
                user_symptoms.append(key)

        new_patient_df = pd.DataFrame([new_patient])
        predicted_class = loaded_model.predict(new_patient_df)[0]
        predicted_label = label_encoder.inverse_transform([predicted_class])[0]

        st.success(f"예측된 질병: {predicted_label}")

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
