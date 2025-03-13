import streamlit as st

APP_TITLE = "Grid Edge Model"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Hyun Woo Kim, Adrian Mungroo, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="⚡",
    layout='wide'
)

st.header('Grid Edge Model Expansion')
st.markdown('##### The gifs from the [dynamic panel](https://energyshed-dashboard.streamlit.app/grid_edge_(dynamic)) are frozen to show the peak hours, emphasizing the differences between the two scenarios.')

st.divider()

c1,c2,c3,c4 = st.columns([1,1,1,0.2])

with c1:
    st.markdown(f"<div style='text-align: center;'><h5>Electrical Energy Usage</h5></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/ukI2zHa.png width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(f"<div style='text-align: center;'><h5>Emissions</h5></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/8jlemVV.png width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(f"<div style='text-align: center;'><h5>Natural Gas Used (heating)</h5></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/aQoS7yz.png width="500">
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
            <img src=https://i.imgur.com/ziy4vmt.png width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/1zJjurF.png width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/v2EF5YS.png width="500">
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