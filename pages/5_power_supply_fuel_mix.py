import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

APP_TITLE = "Power Supply Fuel Mix"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Adrian Mungroo, Hyun Woo Kim, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout='wide'
)

col1, col2 = st.columns(2)
with col1:
    st.markdown("<div style='text-align: center;'><h3>Baseline Energy Mix</h3></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/rh77Nzv.png" width="600">
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown("<div style='text-align: center;'><h3>Utility Investment in Renewables</h3></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/1wlZaIK.png" width="635">
        </div>
        """,
        unsafe_allow_html=True
    )