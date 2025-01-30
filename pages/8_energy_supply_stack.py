import streamlit as st
import pandas as pd
import plotly.graph_objects as go

APP_TITLE = "Supply Stack"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Hyun Woo Kim, Adrian Mungroo, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout='wide'
)

total_baseline_energy = pd.read_csv(r'data/total_baseline_energy.csv')
total_heatpump_energy = pd.read_csv(r'data/total_heatpump_energy.csv')

fig = go.Figure()

# Add Baseline Energy Trace
fig.add_trace(go.Scatter(
    x=total_baseline_energy['timestamp'],
    y=total_baseline_energy['total_energy_kWh'],
    mode='lines',
    name='Baseline Energy',
    line=dict(width=1)
))

fig.add_trace(go.Scatter(
    x=total_heatpump_energy['timestamp'],
    y=total_heatpump_energy['total_energy_kWh'],
    mode='lines',
    name='Heat Pump Energy',
    line=dict(width=1, color = 'orange')
))

fig.update_layout(
    title="Baseline vs. Heat Pump Energy Consumption",
    xaxis_title="Time",
    yaxis_title="Total Energy (kWh)",
    xaxis=dict(showgrid=True, tickformat="%b %Y"),
    yaxis=dict(showgrid=True),
    hovermode="x unified",
)

# Show in Streamlit

st.header('Supply Stack')

st.divider()

c1,c2,c3 = st.columns([3,1,3])
with c1:
    st.plotly_chart(fig, use_container_width=True)
    st.write("The sum of emissions for baseline is 6.729e+09 kg")
    st.write("The sum of emissions for heatpump is 5.436e+09 kg")