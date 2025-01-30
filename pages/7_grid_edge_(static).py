import streamlit as st

APP_TITLE = "Grid Edge Model"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Hyun Woo Kim, Adrian Mungroo, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="⚡",
    layout='wide'
)

st.header('Grid Edge Model Expansion')
st.markdown('##### The gifs from the [dynamic panel](http://localhost:8501/grid_edge_(dynamic)) are frozen to show the peak hours, emphasizing the differences between the two scenarios.')

st.divider()

c1,c2,c3,c4 = st.columns([1,1,1,0.2])

with c1:
    st.markdown(f"<div style='text-align: center;'><h5>Electrical Energy Usage</h5></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/ZggzLwX.png width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(f"<div style='text-align: center;'><h5>Emissions</h5></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/BCJe8MO.png width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(f"<div style='text-align: center;'><h5>Natural Gas Used (heating)</h5></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/kCYP1JL.png width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        """
        <div style="writing-mode: vertical-rl; transform: rotate(180deg); height: 30%; margin-top: 50px;">
            <h3>Baseline</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

c1,c2,c3,c4 = st.columns([1,1,1,0.2])

with c1:
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/5CTvYmW.png width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/ojLbjjz.png width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/B7mTIzT.png width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        """
        <div style="writing-mode: vertical-rl; transform: rotate(180deg); height: 30%; margin-top: 50px;">
            <h3>Heat Pump</h3>
        </div>
        """,
        unsafe_allow_html=True
    )