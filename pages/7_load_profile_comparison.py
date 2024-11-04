import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

APP_TITLE = "Load Profile Comparison"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Adrian Mungroo, Hyun Woo Kim, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout='wide'
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div style='text-align: center;'><h3>Winter No Heatpump</h3></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/TnE4QQC.png" width="620">
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown("<div style='text-align: center;'><h3>Winter Income Based Heatpump</h3></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/sMmusZQ.png" width="620">
        </div>
        """,
        unsafe_allow_html=True
    )
with col3:
    st.markdown("<div style='text-align: center;'><h3>Winter Full Heatpump</h3></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/3UGSZLd.png" width="620">
        </div>
        """,
        unsafe_allow_html=True
    )

st.write('')
st.write("Combining heat pump models with Distributed Energy Resource (DER) adoption models provides a more realistic scenario for understanding technology adoption patterns. This approach enables more accurate projections of energy usage and emissions reductions based on varying levels of heat pump penetration and income-based adoption incentives.")