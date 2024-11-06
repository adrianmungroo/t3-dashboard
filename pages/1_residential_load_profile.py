import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

APP_TITLE = "Fulton County Load Profile Examples"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Adrian Mungroo, Hyun Woo Kim, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout='wide'
)

st.header('Residential Load Profile Examples and Comparison')

st.markdown("""
##### This visualization demonstrates how Winter residential energy consumption patterns vary across Fulton County. We compare two key scenarios:
""")

col1, col2 = st.columns(2)
col1.markdown("""
- ##### Left Map (Baseline / Business as Usual)
    - Homes primarily use natural gas for heating
""")

col2.markdown("""
- ##### Right Map (Heat Pump Scenario)
    - Asks "what if" homes switched to electrical heat pumps
    - Higher electrical usage due to electric heating
    - Demonstrates potential grid impacts of electrification
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

st.header('DAC vs Non DAC')
st.markdown("""
##### The maps above use real data from agent-based models, which simulates individual household energy consumption. To contrast the difference in electrical consumption between DAC and Non-DAC households, two representative households were selected and their respective consumptions were plotted below:
""")

col1, col2 = st.columns(2)


col1.markdown("<div style='text-align: center;'><h6>English Avenue Traditional single-family home</h6></div>", unsafe_allow_html=True)
col1.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/jK4TcXq.png" width="250">
        </div>
        """,
        unsafe_allow_html=True
    )

col2.markdown("<div style='text-align: center;'><h6>Midtown modern condominium unit</h6></div>", unsafe_allow_html=True)
col2.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/DIvcc7u.png" width="250">
        </div>
        """,
        unsafe_allow_html=True
    )

col1, col2 = st.columns(2)
with col1:
    st.markdown("<div style='text-align: center;'><h4>DAC Household Winter Elec Consumption</h4></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/4w56NC5.png" width="500">
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown("<div style='text-align: center;'><h4>Non-DAC Household Winter Elec Consumption</h4></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/xrEaG99.png" width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

st.caption(APP_SUBTITLE)