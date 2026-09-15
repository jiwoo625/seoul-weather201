```python
import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="서울 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

# 제목
st.title("🌡️ 서울의 연평균 기온 변화")
st.write("서울의 일별 기온 데이터를 연도별 평균으로 계산해 장기간의 변화를 살펴봅니다.")

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    # 평균기온을 숫자로 변환
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    # 날짜 또는 평균기온이 없는 행 제거
    df = df.dropna(subset=["날짜", "평균기온"])

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    return df


try:
    df = load_data()

    # 연도별 평균기온 계산
    yearly_temp = (
        df.groupby("연도", as_index=False)["평균기온"]
        .mean()
        .sort_values("연도")
    )

    # 그래프
    st.subheader("📈 연도별 평균기온")

    chart_data = yearly_temp.set_index("연도")

    st.line_chart(
        chart_data,
        y="평균기온",
        x_label="연도",
        y_label="평균기온 (℃)",
        height=500
    )

    # 간단한 요약 정보
    first_year = int(yearly_temp["연도"].min())
    last_year = int(yearly_temp["연도"].max())

    first_temp = yearly_temp.iloc[0]["평균기온"]
    last_temp = yearly_temp.iloc[-1]["평균기온"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "자료 기간",
            f"{first_year} ~ {last_year}"
        )

    with col2:
        st.metric(
            "가장 오래된 연평균",
            f"{first_temp:.1f} ℃"
        )

    with col3:
        st.metric(
            "최근 연평균",
            f"{last_temp:.1f} ℃"
        )

    st.caption(
        "※ 연평균 기온은 해당 연도의 일별 평균기온을 평균하여 계산했습니다."
    )

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.write(f"오류 내용: {e}")
```
