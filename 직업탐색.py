import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Streamlit 페이지 설정
st.set_page_config(
    page_title="직업탐색",
    page_icon="./image/job.png",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None
)

# Streamlit 앱의 제목 설정
st.title("진로 강의")

# 오늘 배울 내용
st.subheader("오늘 배울 내용")
st.markdown("**오늘** 배울 내용")

st.divider()

# 엑셀 파일 업로드
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요.", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, header=0, index_col=0)
    df.index = pd.to_numeric(df.index, errors='coerce')
    
    st.success('파일 업로드 성공!')
    
    occupations = df.columns.tolist()

    selected_occupation = st.selectbox("직업 선택:", occupations)

    # 연도 범위 설정 시 정수 변환 적용
    start_year = st.slider("시작 연도:", min_value=int(df.index.min()), max_value=int(df.index.max()) - 1, value=int(df.index.min()))
    end_year = st.slider("끝 연도:", min_value=start_year + 1, max_value=int(df.index.max()), value=int(df.index.max()))

    filtered_df = df.loc[start_year:end_year, [selected_occupation]]

    st.subheader(f"{selected_occupation}의 {start_year}에서 {end_year}까지의 변화")
    fig, ax = plt.subplots()
    filtered_df.plot(ax=ax, marker='o')
    plt.xlabel("연도")
    plt.ylabel(selected_occupation)
    st.pyplot(fig)

    st.subheader("전체 연도와 선택한 직업에 대한 데이터 시각화")
    selected_occupations = st.multiselect("직업 선택:", occupations, default=[selected_occupation])

    if selected_occupations:
        selected_df = df.loc[start_year:end_year, selected_occupations]
        fig, ax = plt.subplots()
        selected_df.plot(ax=ax, marker='o')
        plt.xlabel("연도")
        plt.ylabel("값")
        st.pyplot(fig)

st.divider()

st.subheader("당신의 생각을 공유하세요")
student_thought = st.text_area("당신의 생각을 입력하세요")

if st.button("제출"):
    if 'student_thoughts.csv' not in os.listdir():
        student_thoughts_df = pd.DataFrame({'학생 생각': [student_thought]})
    else:
        student_thoughts_df = pd.read_csv('student_thoughts.csv', encoding='utf-8')
        student_thoughts_df = student_thoughts_df.append({'학생 생각': student_thought}, ignore_index=True)

    student_thoughts_df.to_csv('student_thoughts.csv', index=False, encoding='utf-8')

    st.subheader("당신의 생각:")
    st.write(student_thought)
