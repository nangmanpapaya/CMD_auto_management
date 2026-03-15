import streamlit as st
import pandas as pd

data = {
    "이름": ["김철수", "이영희", "박민준"],
    "포지션": ["QB", "WR", "OL"],
    "연락처": ["010-1234-5678", "010-2345-6789", "010-3456-7890"]
}

df = pd.DataFrame(data)

st.title("🏈 미식축구부 관리 시스템")
st.subheader("부원 명단")
st.dataframe(df)