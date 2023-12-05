import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os  # Import the os module


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
    # 엑셀 파일을 데이터프레임으로 읽기
    df = pd.read_excel(uploaded_file, header=0, index_col=0)
    
    # 파일 업로드에 성공했다는 메시지 표시
    st.success('파일 업로드 성공!')
    
    # 데이터프레임의 열 목록 가져오기
    occupations = df.columns.tolist()

    # 직업 선택 위젯 생성
    selected_occupation = st.selectbox("직업 선택:", occupations)

    # 연도 범위 설정
    start_year = st.slider("시작 연도:", min_value=df.index.min(), max_value=df.index.max() - 1, value=df.index.min())
    end_year = st.slider("끝 연도:", min_value=start_year + 1, max_value=df.index.max(), value=df.index.max())

    # 선택한 연도 범위로 데이터 필터링
    filtered_df = df.loc[start_year:end_year, [selected_occupation]]

    # 직업별 선형 그래프 그리기
    st.subheader(f"{selected_occupation}의 {start_year}에서 {end_year}까지의 변화")
    fig, ax = plt.subplots()
    filtered_df.plot(ax=ax, marker='o')
    plt.xlabel("연도")
    plt.ylabel(selected_occupation)
    st.pyplot(fig)

    # 전체 연도와 선택한 직업에 대한 데이터를 한 번에 선형 그래프로 그리기
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
        # 학생의 생각 입력
st.subheader("당신의 생각을 공유하세요")
student_thought = st.text_area("당신의 생각을 입력하세요")




# 생각 제출 버튼
if st.button("제출"):
    # 입력된 생각을 저장하는 코드
    if 'student_thoughts.csv' not in os.listdir():
        # student_thoughts.csv 파일이 없으면 새로 생성
        student_thoughts_df = pd.DataFrame({'학생 생각': [student_thought]})
    else:
        # student_thoughts.csv 파일이 이미 존재하면 기존 데이터에 추가
        student_thoughts_df = pd.read_csv('student_thoughts.csv', encoding='utf-8')
        student_thoughts_df = student_thoughts_df.append({'학생 생각': student_thought}, ignore_index=True)

    # 데이터프레임을 파일에 저장 (UTF-8 인코딩 지정)
    student_thoughts_df.to_csv('student_thoughts.csv', index=False, encoding='utf-8')

    # 입력된 생각을 출력
    st.subheader("당신의 생각:")
    st.write(student_thought)