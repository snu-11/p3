import streamlit as st

# 24개의 직업과 그에 대한 AI 노출지수 정답 데이터
job_data = {
    '직업': ['의사', '교사', '개발자', '경찰', '간호사', '회계사', '변호사', '연구원', '영화배우', '가수', '작가', '요리사',
            '디자이너', '엔지니어', '프로게이머', '운동선수', '프로그래머', '판매원', '기자', '농부', '예술가', '과학자', '의료기사'],
    'AI 노출지수': [85, 60, 95, 70, 75, 65, 80, 90, 60, 70, 75, 50, 70, 85, 95, 80, 90, 55, 60, 70, 65, 75, 85]
}

# Streamlit 앱 제목 설정
st.title('직업별 AI 노출지수 추측 게임')

# Initialize session state variables
if 'guesses' not in st.session_state:
    st.session_state['guesses'] = [None] * len(job_data['직업'])
    st.session_state['submitted'] = False

# Input fields for each job, three per row
for i in range(0, len(job_data['직업']), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(job_data['직업']):
            with cols[j]:
                st.session_state['guesses'][i + j] = st.number_input(f"{job_data['직업'][i + j]}의 AI 노출지수 추측", 
                                                                    min_value=0, max_value=100, step=1, key=i + j)

# Submit button
if st.button("모든 답 제출"):
    st.session_state['submitted'] = True

# Display results after submission
if st.session_state['submitted']:
    correct_count = 0
    st.subheader("결과:")
    for i, job in enumerate(job_data['직업']):
        guess = st.session_state['guesses'][i]
        correct_answer = job_data['AI 노출지수'][i]
        if abs(guess - correct_answer) <= 5:
            st.success(f"{job}: 정답입니다! AI 노출지수는 {correct_answer}입니다. 당신의 추측: {guess}")
            correct_count += 1
        else:
            st.error(f"{job}: 틀렸습니다. 정답은 {correct_answer}입니다. 당신의 추측: {guess}")

    # Display the count of correct answers
    st.subheader(f"총 {correct_count}개의 직업을 맞췄습니다.")
