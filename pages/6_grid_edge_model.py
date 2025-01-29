import streamlit as st

APP_TITLE = "Grid Edge Model"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Hyun Woo Kim, Adrian Mungroo, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="⚡",
    layout='wide'
)

st.header('Grid Edge Model Expansion')
st.markdown('##### As seen in the gif below, we have expanded the reach of our grid energy usage models into Forsyth and DeKalb, with Gwinnett just around the corner!')

st.divider()

st.markdown(f"<div style='text-align: center;'><h5> Total Electrical Energy Usage (Fulton, Forsyth, DeKalb) </h5></div>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="text-align: center;">
        <img src=https://i.imgur.com/zUrv2rx.gif width="500">
    </div>
    """,
    unsafe_allow_html=True
)