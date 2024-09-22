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
APP_SUBTITLE = "David Solano, Adrian Mungroo, Hyun Woo Kim"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout='wide'
)

# st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

data_industrial = pd.read_csv(r'data/Consumed_industrial_kW.csv')

col1, col2 = st.columns(2)

datacenter_offset = col1.slider("Datacenter Base Power MW", 0.0, 350.0, 150.0)
tip_point_F = col2.slider("Tip point (F)", 45, 65, 50)
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
    title='Datacenter Power Consumption',
    xaxis_title='Time of Year',
    yaxis_title='Industry Power Consumption (MW)',
    legend=dict(x=0, y=1),
    template='plotly_white'  
)

st.plotly_chart(fig)
