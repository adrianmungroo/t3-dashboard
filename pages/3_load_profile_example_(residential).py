import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

APP_TITLE = "Fulton County Load Profile Examples"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Adrian Mungroo, Hyun Woo Kim, Meiwen Bi"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout='wide'
)

st.write('## Baseline vs Heatpump')

st.image('https://i.imgur.com/Jpng561.gif', use_column_width=True)

st.write('## DAC vs Non DAC household Winter')

col1, col2 = st.columns(2)
with col1:
    st.image('https://i.imgur.com/4w56NC5.png', use_column_width=True)
with col2:
    st.image('https://i.imgur.com/xrEaG99.png', use_column_width=True)

st.caption(APP_SUBTITLE)