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

st.header('Energy Supply and Demand Scenarios')
st.markdown("""
##### This visualization shows how Atlanta's energy landscape might change under different scenarios. We compare three key situations:
""")

c1,c2,c3 = st.columns(3)
c1.markdown(""" 
###### Baseline Energy Mix (Center):
- Shows how Atlanta currently gets and uses its electricity
- Represents our current mix of power sources (solar, natural gas, nuclear, etc.)
- Serves as a reference point for comparing changes
""")

c2.markdown("""
###### Utility-Led Changes (Left):
- Shows what happens if power companies lead the energy transition
- Focuses on large-scale renewable projects
- Reflects traditional utility planning approaches
""")

c3.markdown("""
###### Customer-Driven Changes (Right):
- Shows what happens when customers adopt new technologies
- Includes impacts of solar panels, energy storage, and smart devices
- Reflects a more distributed energy future
""")

st.divider()

triangle = st.container()
    
# Top of triangle - make it centered
_, center, _ = triangle.columns([1, 2, 1])
with center:
    st.markdown("<div style='text-align: center;'><h3>Baseline Energy Mix</h3></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/rh77Nzv.png" width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

# Bottom of triangle
left, right = triangle.columns(2)
with left:
    st.markdown("<div style='text-align: center;'><h3>Utility Investment in Renewables</h3></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/1wlZaIK.png" width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    st.markdown("<div style='text-align: center;'><h3>DER investment at Grid Edge</h3></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/cxuTk9f.png" width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()
st.header('Impact Metrics')
st.markdown("""
##### We measure the effects of each scenario across several key areas:
""")

c1,c2 = st.columns(2)

c1.markdown("""
###### Infrastructure Focused Studies
- GHG Emissions
- Utility Electricity Cost
- Electrical System Reliability
- Value of Resilience                                    
""")

c2.markdown("""
###### EEEJ Focused Studies
- Consumer Electrical Cost
- Energy Equity for DACs
- Jobs and Workforce Development                                    
""")