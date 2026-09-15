import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="서울 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울의 연평균 기온 변화")
st.write("서울의 일별 기온 데이터를 이용해 연평균 기온의 변화를 살펴봅니다.")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜와 평균기온을 숫자/날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    # 필요한 데이터가 없는 행 제거
    df = df.dropna(subset=["날짜", "평균기온"])

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    return df


try:
    df = load_data()

    # 연도별 평균기온 계산
    yearly_temp = (
        df.groupby("연도")["평균기온"]
        .mean()
        .reset_index()
        .sort_values("연도")
    )

    st.subheader("📈 연도별 평균기온")

    # Streamlit 그래프용 데이터
    chart_data = yearly_temp.set_index("연도")

    st.line_chart(
        chart_data["평균기온"],
        height=500
    )

    # 요약 정보
    first_year = int(yearly_temp["연도"].min())
    last_year = int(yearly_temp["연도"].max())

    first_temp = yearly_temp.iloc[0]["평균기온"]
    last_temp = yearly_temp.iloc[-1]["평균기온"]

    st.subheader("📊 주요 정보")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "자료 기간",
            f"{first_year} ~ {last_year}"
        )

    with col2:
        st.metric(
            f"{first_year}년 연평균",
            f"{first_temp:.1f} ℃"
        )

    with col3:
        st.metric(
            f"{last_year}년 연평균",
            f"{last_temp:.1f} ℃"
        )

    st.caption(
        "※ 연평균 기온은 각 연도의 일별 평균기온을 평균하여 계산했습니다."
    )

except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.exception(e)
