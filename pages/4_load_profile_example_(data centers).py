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

st.markdown("<div style='text-align: center;'><h2>Winter Datacenter vs Summer Datacenter</h2></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.imgur.com/kGYMj6r.gif" width="1100">
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(APP_SUBTITLE)