import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

APP_TITLE = "Fulton County Load Profile Examples"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Adrian Mungroo, Hyun Woo Kim, Meiwen Bi + Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout='wide'
)

st.write('## Winter Datacenter vs Summer Datacenter')

st.image('https://s6.ezgif.com/tmp/ezgif-6-9abfc313f8.gif', use_column_width=True)

st.caption(APP_SUBTITLE)