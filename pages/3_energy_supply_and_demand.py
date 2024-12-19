import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

APP_TITLE = "Power Supply Fuel Mix"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Adrian Mungroo, Hyun Woo Kim, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🔋",
    layout='wide'
)

st.header('Energy Supply and Demand Scenarios')
st.markdown("""
##### This mock outcome shows how the energy landscape can change under different scenarios. We compare three key situations:
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
- Shows what happens if power companies lead the green energy transition
- Focuses on large-scale renewable projects
""")

c3.markdown("""
###### Community-Driven Changes (Right):
- Shows what happens when customers adopt new behind-the-meter (BTM) technologies
- Includes impacts of renewables, energy storage, and smart devices
- Reflects a more distributed energy future
""")

st.markdown("""
##### Please observe the black triangle ▲ which indicates the cost and level of induced pollution of the associated fuel mix.
##### NOTE: None of the following results are empirically accurate, nor are they drawn to scale. They are mockups for conceptual purposes. 
""")

st.divider()
st.write("##### Our tool will allow users to select a pre-ran scenario to observe how it affects the energy spread!")
_,center,_ = st.columns([4,5,1])
with center:
    scenario_choice = st.radio("**Please select a scenario**", ['**Utility Investment in Renewables**','**DER investment at Grid Edge**'])
left, right = st.columns(2)
with left:
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

with right:
    if scenario_choice == "Utility Investment in Renewables":
        st.markdown("<div style='text-align: center;'><h3>Utility Investment in Renewables</h3></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: center;">
                <img src="https://i.imgur.com/1wlZaIK.png" width="530">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown("<div style='text-align: center;'><h3>DER investment at Grid Edge</h3></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align: center;">
                <img src="https://i.imgur.com/cxuTk9f.png" width="550">
            </div>
            """,
            unsafe_allow_html=True
        )

st.divider()
st.markdown("""
##### Our tool aims to capture and measure the following metrics for each scenario:
""")

c1,c2 = st.columns(2)

c1.markdown("""
##### Infrastructure Focused Studies
- GHG Emissions
- Utility Electricity Cost
- Electrical System Reliability
- Value of Resilience                                    
""")

c2.markdown("""
##### EEEJ Focused Studies
- Consumer Electrical Cost
- Energy Equity for Underserved Communities
- Jobs and Workforce Development                                    
""")