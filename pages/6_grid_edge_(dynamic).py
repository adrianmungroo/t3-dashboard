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

st.markdown("""
            Two scenarios are presented below: \n
            1) 0% Heat Pump utilization
            2) 100% Heat Pump Adoption \n
            ###### We observe the effects that while heat pumps lead to an increase of electricity usage, they ultimately lead to lower total emissions and a reduced reliance on local natural gas. 
""")

st.divider()

c1,c2,c3,c4 = st.columns([1,1,1,0.2])

with c1:
    st.markdown(f"<div style='text-align: center;'><h5>Electrical Energy Usage</h5></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/rcD4WcH.gif width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(f"<div style='text-align: center;'><h5>Emissions</h5></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/CgrlPTO.gif width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(f"<div style='text-align: center;'><h5>Natural Gas Used (heating)</h5></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/rbkGo7Y.gif width="500">
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
            <img src=https://i.imgur.com/Ak9YrOb.gif width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/ru9IoVJ.gif width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src=https://i.imgur.com/hL5QT4D.gif width="500">
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