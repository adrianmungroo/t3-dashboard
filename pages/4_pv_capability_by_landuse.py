import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

link_dict = {'Apartments (Class X)': ["https://i.imgur.com/tg5AmQh.gif", "https://i.imgur.com/a4Kd2Q2.png"],
             'Schools' : ["https://i.imgur.com/UuVIZE3.gif", "https://i.imgur.com/ZGJvqFL.png"],
             'Churches' : ["https://i.imgur.com/i9YAmH6.gif", "https://i.imgur.com/3fiFoB5.png"],
             'Warehouses' : ["https://i.imgur.com/Ou1rFvB.gif", "https://i.imgur.com/qOb6zRG.png"],
             }

APP_TITLE = "PV Capability"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Adrian Mungroo, Hyun Woo Kim, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout='wide'
)

st.header('PV Capability')
st.markdown("""
##### We used temporal data from GT campus PV panels as well as Fulton Parcel Land Use Data as well as Microsoft Buildings Footprint data to develop estimated PV kWh contributions by landuse codes:
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


