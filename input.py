import streamlit as st
import sqlite3
from db_data import create_user_symptoms_table, create_user_details_table
from db_data import insert_user_details, insert_user_symptoms

# 로그인 여부 확인
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🚫 로그인 후 이용 가능한 페이지입니다.")
    st.stop()

create_user_symptoms_table()
create_user_details_table()

st.title('증상 입력')
user_id = st.session_state["username"]

option = st.multiselect(
    '증상을 선택해 주세요.',
    ('발열', '기침', '피로', '호흡곤란')
)

st.subheader('해당사항')

options = ["낮음", "정상", "높음"]
selection1 = st.segmented_control(
    "혈압", options, selection_mode="single",
    key="blood_pressure"
)

if selection1 is not None:
    st.markdown(f"측정된 혈압 수치는 {selection1}입니다.")

options = ["낮음", "정상", "높음"]
selection2 = st.segmented_control(
    "콜레스테롤", options, selection_mode="single",
    key="cholesterol"
)
if selection2 is not None:
    st.markdown(f"측정된 콜레스테롤 수치는 {selection2}입니다.")

if st.button("선택하기"):
    if not option:
        st.warning("증상을 선택해주세요.")
    else:
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

        # insert_user_details(
        #     user_id=user_id,
        #     symptoms=", ".join(option),
        #     disease="",
        #     item1="",
        #     item2="",
        #     item3=""
        # )