import streamlit as st
import sqlite3
from db_data import update_user_info

# 로그인 여부 확인
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("🚫 로그인 후 이용 가능한 페이지입니다.")
    st.stop()

st.title('👩‍💻마이페이지')

tab1, tab2 = st.tabs(["나의 진단 내역", "회원정보 수정"])


def get_user_diagnosis(user_id):
     conn = sqlite3.connect('users.db')
     cursor = conn.cursor()
     cursor.execute('''
        SELECT symptoms, disease, item1, item2, item3
        FROM user_details
        WHERE user_id = ? 
        ORDER BY id DESC
        LIMIT 3
    ''', (user_id,))
     row = cursor.fetchall()
     conn.close()
     return row
     
user_id = st.session_state.get('username')


diagnoses = get_user_diagnosis(user_id)

with tab1:
    st.header("🩺 나의 최근 진단 내역")

    if not diagnoses:
        st.info("아직 저장된 진단 내역이 없습니다.")
    else:
        for idx, (symptoms, disease, item1, item2, item3) in enumerate(diagnoses, start=1):
       
            with st.container():
                st.markdown(
                    """
                    <div style="
                        background-color: #f0f4f8; 
                        padding: 20px; 
                        border-radius: 10px; 
                        box-shadow: 0 2px 4px lightgray;
                        max-width: 600px;
                        margin-bottom: 20px;
                    ">
                        <p><strong>🏣 증상:</strong> {symptoms}</p>
                        <p><strong>🧬 질병:</strong> {disease}</p>
                        <p><strong>💊 추천 약:</strong> {item1}, {item2}, {item3}</p>
                    </div>
                    """.format(symptoms=symptoms, disease=disease, item1=item1, item2=item2, item3=item3),
                    unsafe_allow_html=True
                )



# 증상 : 발열, 기침, 피로, 호흡 곤란
# 예상되는 질병
# 예측된 질병과 관련된 일반 의약품

with tab2:
    st.subheader("회원정보수정")
    chg_username = st.text_input("아이디", placeholder="변경할 아이디를 작성해주세요.")
    chg_password = st.text_input("비밀번호", placeholder="변경할 비밀번호를 입력해주세요", type = "password")
    chg_gender = st.selectbox("성별",("선택", "남성", "여성"))
    chg_age = st.slider("나이", 0, 110, 25)
    if st.button("수정 완료", key="submit_edit"):
        if chg_username and chg_password and chg_gender != "선택":
            update_user_info(
                current_username=st.session_state["username"],
                new_username=chg_username,
                new_password=chg_password,
                gender=chg_gender,
                age=chg_age
            )
            st.session_state["username"] = chg_username 
            st.success("회원정보가 수정되었습니다")
        else:
            st.warning("모든 항목을 입력해주세요")