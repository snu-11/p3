import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Streamlit 앱 제목 및 설명 설정
st.title("엑셀 데이터 시각화")
st.write("엑셀 파일을 업로드하고 선택한 행과 열을 기반으로 막대 그래프를 생성합니다.")

# 엑셀 파일 업로드
uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx"])

if uploaded_file is not None:
    # 엑셀 파일을 DataFrame으로 읽기
    df = pd.read_excel(uploaded_file)

    # 첫 번째 행을 인덱스로 설정
    df = df.set_index(df.columns[0])

    # 선택 위젯에 표시할 행과 열의 이름
    row_names = df.index.tolist()
    column_names = df.columns.tolist()

    # 행 선택 위젯
    selected_rows = st.multiselect("행 선택", row_names)

    # 열 선택 위젯
    selected_columns = st.multiselect("열 선택", column_names)

    if selected_rows and selected_columns:
        # 선택한 데이터로 DataFrame 생성
        selected_data = df.loc[selected_rows, selected_columns]

        # 한글 폰트 설정
        plt.rcParams['font.family'] = 'NanumGothic'

        # 그래프 크기 조정
        plt.figure(figsize=(12, len(selected_rows) + len(selected_columns)))

        # 동적 막대 너비 및 간격 설정
        total_bars = len(selected_columns) * len(selected_rows)
        bar_width = 0.8 / total_bars  # 전체 막대 개수에 따라 막대 너비 조정
        gap = bar_width * 0.05  # 막대 너비에 비례하여 간격 조정
        indices = np.arange(len(selected_rows))  # 행 인덱스

        # 다양한 색상 생성
        colors = plt.cm.get_cmap('nipy_spectral', total_bars)

        for i, column in enumerate(selected_columns):
            for j, row in enumerate(selected_rows):
                idx = i * len(selected_rows) + j
                plt.barh(indices[j] + (bar_width + gap) * i, selected_data.loc[row, column], height=bar_width, label=f'{column}-{row}', color=colors(idx))

        # y 축에 행 이름 설정 및 글자 크기 조정
        plt.yticks(indices + (bar_width + gap) * len(selected_columns) / 2, selected_rows, fontsize=12)  # 글자 크기를 12로 조정

        # x축, y축 라벨 및 범례 설정

        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=min(3, total_bars))  # 범례 위치 및 열 개수 조정

        # 그래프를 Streamlit에 표시
        st.pyplot(plt.gcf())
