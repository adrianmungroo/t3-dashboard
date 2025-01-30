import streamlit as st

APP_TITLE = "Grid Edge Model"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Hyun Woo Kim, Adrian Mungroo, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="⚡",
    layout='wide'
)

st.header('Grid Edge Model Expansion')
st.markdown('##### As seen in the gifs below, we have expanded the reach of our grid energy usage models into Forsyth and DeKalb, with Gwinnett just around the corner!')

st.divider()

st.write("### Baseline")

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown(f"<div style='text-align: center;'><h5> Total Electrical Energy Usage</h5></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/njX0I07.gif width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(f"<div style='text-align: center;'><h5> Total Emissions </h5></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/4zCZQ7j.gif width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(f"<div style='text-align: center;'><h5> Total Natural Gas Used </h5></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/RMJME2O.gif width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("### With Heat Pump")

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown(f"<div style='text-align: center;'><h5> Total Electrical Energy Usage</h5></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/w3FM6Je.gif width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(f"<div style='text-align: center;'><h5> Total Emissions </h5></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/fjqUqR8.gif width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(f"<div style='text-align: center;'><h5> Total Natural Gas Used </h5></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/AzCpztY.gif width="500">
        </div>
        """,
        unsafe_allow_html=True
    )