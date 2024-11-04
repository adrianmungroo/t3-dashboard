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

st.markdown("<div style='text-align: center;'><h2>Baseline vs Heatpump</h2></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.imgur.com/Jpng561.gif" width="1000">
    </div>
    """,
    unsafe_allow_html=True
)

st.write('## DAC vs Non DAC')

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