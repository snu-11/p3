import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os  # Import the os module

st.title("진로 도감")

st.subheader("미래에 인기있을 직업, 새로 나타날 직업")

skill_emoji_dict = {
    "창의": "💡",
    "수리논리": "➕",
    "사회정서": "💗",
    "언어": "🗣️",
    "땅": "🌋",
    "바위": "🪨",
    "벌레": "🐛",
    "고스트": "👻",
    "강철": "🤖",
    "불꽃": "🔥",
    "물": "💧",
    "풀": "🍃",
    "전기": "⚡",
    "에스퍼": "🔮",
    "얼음": "❄️",
    "드래곤": "🐲",
    "악": "😈",
    "페어리": "🧚"
}

initial_jobs = [
    {
        "name": "사물 인터넷 전문가",
        "skill": ["창의", "수리논리"],
        "image_url": "https://cdn-icons-png.flaticon.com/128/6537/6537379.png"
    },
    {
        "name":"프롬프트 개발자",
        "skill":["창의", "수리논리"],
        "image_url":"https://cdn-icons-png.flaticon.com/128/6009/6009939.png"
    },
    {
        "name": "감정인식기술전문가",
        "skill": ["언어", "사회정서"],
        "image_url": "https://cdn-icons-png.flaticon.com/128/5230/5230777.png",
    },
]

if "직업" not in st.session_state:
    st.session_state.jobs = initial_jobs

with st.form(key="form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(label="직업 이름")
    with col2:
        skill = st.multiselect(
            label="직업에 필요한 능력",
            options=list(skill_emoji_dict.keys()),
            max_selections=2
        )
    image_url = st.text_input(label="직업 이미지 URL")
    submit = st.form_submit_button(label="Submit")
    if submit:
        if not name:
            st.error("직업의 이름을 입력해주세요.")
        elif len(skill) == 0:
            st.error("직업에 필요한 능력을 적어도 한개 선택해주세요.")
        else:
            st.success("직업을 추가할 수 있습니다.")
            st.session_state.jobs.append({
                "name": name,
                "skill": skill,
                "image_url": image_url if image_url else "./images/default.png"
            })

for i in range(0, len(st.session_state.jobs), 3):
    row_jobs = st.session_state.jobs[i:i+3]
    cols = st.columns(3)
    for j in range(len(row_jobs)):
        with cols[j]:
            job = row_jobs[j]
            with st.expander(label=f"**{i+j+1}. {job['name']}**", expanded=True):
                st.image(job["image_url"])
                emoji_skill = [f"{skill_emoji_dict[x]} {x}" for x in job["skill"]]
                st.text(" / ".join(emoji_skill))
                delete_button = st.button(label="삭제", key=i+j, use_container_width=True)
                if delete_button:
                    del st.session_state.jobs[i+j]
                    st.rerun()
