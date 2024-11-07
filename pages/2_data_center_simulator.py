import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go

def compute_contribution(dbt, tip_point, industrial_consumption, datacenter_offset, cooling_penalty):
    if dbt > tip_point:
        return industrial_consumption + datacenter_offset + (dbt - tip_point) * cooling_penalty
    else:
        return industrial_consumption + datacenter_offset

APP_TITLE = "Datacenter Acquisition Simulator"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Adrian Mungroo, Hyun Woo Kim, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout='wide'
)

data_industrial = pd.read_csv(r'data/Consumed_industrial_kW.csv')

st.markdown(
        """<style>
    div[class*="stSlider"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 20px;
    }
        </style>
        """, unsafe_allow_html=True)

st.header('Data Center Simulator')
st.markdown('##### This tool allows you to simulate the electrical demand impacts of datacenters.')
st.markdown('##### Please adjust the sliders below to change parameters such as:')
st.markdown("""
- Datacenter Base Power - This is the minimum amount of power that a datacenter consistently needs to operate.
- Tip Point - The temperature threshold at which additional cooling starts to kick in.
- Cooling Penalty - Quantifies the extra energy needed to cool the datacenter when it gets hotter than the Tip Point.  
""")

st.markdown("""
##### The graph uses data for the entire year of 2022 quantified at the hourly level. Afterwards, please scroll down to see a map of datacenter demand. 
""")
st.divider()

col1, col2 = st.columns(2)

datacenter_offset = col1.slider("Datacenter Base Power MW", 0.0, 350.0, 150.0)
tip_point_F = col2.slider("Tip Point (F)", 45, 65, 50)
cooling_penalty = col1.slider("Cooling Penalty %", 0.0, 100.0, 15.0)

data_industrial['Datacenter Contribution (MW)'] = data_industrial.apply(
    lambda x: compute_contribution(x['DBT'], tip_point_F, x['Consumed Industrial'], datacenter_offset, cooling_penalty), axis=1
)

start_date = pd.Timestamp('2022-01-01') # Making hours into datetime since we know the beginning date
data_industrial['DateTime'] = pd.date_range(start=start_date, periods=len(data_industrial), freq='h')

# Create a Plotly figure
fig = go.Figure()

fig.add_trace(go.Scatter(x=data_industrial['DateTime'], y=data_industrial['Consumed Industrial'], mode='lines', name='Industrial', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=data_industrial['DateTime'], y=data_industrial['Datacenter Contribution (MW)'], mode='lines', name='Industrial + Datacenters', line=dict(color='coral')))

fig.update_layout(
    xaxis_title='Time of Year',
    yaxis_title='Industry Power Consumption (MW)',
    legend=dict(x=0, y=1),
    template='plotly_white'  
)

st.plotly_chart(fig)

st.divider()

st.header("Spatio-temporal Forecast of Fulton Datacenter Energy Usage")
st.markdown('##### This analysis assumed datacenter locations from [Drawdown Georgia](https://drawdownga.gatech.edu/datacenters/) but this count is obsolete in comparison to [Data Center Map](https://www.datacentermap.com/usa/georgia/).')


st.markdown("<div style='text-align: center;'><h4>Winter Datacenter vs Summer Datacenter</h2></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.imgur.com/kGYMj6r.gif" width="1100">
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()
st.caption(APP_SUBTITLE)
