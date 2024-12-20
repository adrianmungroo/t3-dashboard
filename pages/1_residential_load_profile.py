import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

APP_TITLE = "Fulton County Load Profiles"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Adrian Mungroo, Hyun Woo Kim, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏡",
    layout='wide'
)

st.header('Residential Load Profile Examples and Comparison')

st.markdown("""
##### This visualization demonstrates how Winter residential energy consumption patterns vary across Fulton County (with other Metro ATL counties coming soon!). We compare two key scenarios:
""")

col1, col2 = st.columns(2)
col1.markdown("""
- ##### Left Map (Baseline / Business as Usual)
    - Homes primarily use natural gas for heating
""")

col2.markdown("""
- ##### Right Map (Heat Pump Conversion Scenario)
    - Asks "what if" homes switched to heat pumps
    - Demonstrates potential grid impacts of electrification
    - On-site combustion is significantly reduced or removed entirely
""")

st.markdown("""
##### Pay attention to the following gif that changes over time, incorporating dynamic weather data into its simulation. 

##### Afterwards, please scroll down to observe how socioeconomic differences affect energy usage.
""")

st.divider()

st.markdown("<div style='text-align: center;'><h2>Baseline vs Heatpump</h2></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.imgur.com/Jpng561.gif" width="1000">
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

st.header('How does energy burden affect usage?')
st.markdown("""
##### The maps above use real data from agent-based models, which simulates individual household energy consumption. Two representative households were selected based on their energy burdens. Their respective consumptions were plotted below:
""")

col1, col2 = st.columns(2)


col1.markdown("<div style='text-align: center;'><h6>High Energy Burden English Avenue SFH</h6></div>", unsafe_allow_html=True)
col1.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/jK4TcXq.png" width="250">
        </div>
        """,
        unsafe_allow_html=True
    )

col2.markdown("<div style='text-align: center;'><h6>Low Energy Burden Johns Creek SFH</h6></div>", unsafe_allow_html=True)
col2.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/GxMoeCY.png" width="250">
        </div>
        """,
        unsafe_allow_html=True
    )

col1, col2 = st.columns(2)
with col1:
    st.markdown("<div style='text-align: center;'><h4>High Energy Burden Consumption</h4></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/n2lKQME.png" width="500">
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown("<div style='text-align: center;'><h4>Low Energy Burden Consumption</h4></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/7c2buib.png" width="500">
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div style='text-align: center;'><p>Note: This household used washer/dryer at 9pm</p></div>", unsafe_allow_html=True)

st.divider()
st.caption(APP_SUBTITLE)