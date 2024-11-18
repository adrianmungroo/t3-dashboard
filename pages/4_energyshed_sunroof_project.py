import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

# 'Schools' : ["https://i.imgur.com/UuVIZE3.gif", "https://i.imgur.com/KjnreM5.png", "https://i.imgur.com/KySERIe.png"]

link_dict = {'Apartments (Class X)': ["https://i.imgur.com/tg5AmQh.gif", "https://i.imgur.com/k6UmhER.png", "https://i.imgur.com/0l67XAg.png"],
             'Churches' : ["https://i.imgur.com/i9YAmH6.gif", "https://i.imgur.com/htlTzNI.png", "https://i.imgur.com/2QZg9bt.png"],
             'Warehouses' : ["https://i.imgur.com/Ou1rFvB.gif", "https://i.imgur.com/NBayTpO.png", "https://i.imgur.com/t020zuK.png"],
             }

APP_TITLE = "Energyshed Sunroof Project"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Adrian Mungroo, Hyun Woo Kim, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="☀️",
    layout='wide'
)

st.header('Energyshed Sunroof Project ☀️')
st.markdown("""
##### Hourly solar irradiation data and Fulton Parcel Land Use data as well as Microsoft Buildings Footprint data to develop estimated Solar kWh
""")

landuse = st.selectbox('**Select a Land Use below**', ['Apartments (Class X)', 'Schools', 'Churches', 'Warehouses'])

c1,c2 = st.columns(2)


with c1:
    st.markdown(f"<div style='text-align: center;'><h3>{landuse} Monthly kWh</h3></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src={link_dict[landuse][0]} width="500">
        </div>
        """,
        unsafe_allow_html=True
    )
with c2:
    st.markdown(f"<div style='text-align: center;'><h3>{landuse} Yearly kWh</h3></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src={link_dict[landuse][1]} width="470">
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(f"<div style='text-align: center;'><h3>{landuse} Monthly Trend</h3></div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src={link_dict[landuse][2]} width="1000">
    </div>
    """,
    unsafe_allow_html=True
)


