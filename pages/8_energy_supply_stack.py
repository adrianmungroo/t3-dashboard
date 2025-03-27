import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

APP_TITLE = "Supply Stack"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Hyun Woo Kim, Adrian Mungroo, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout='wide'
)

# Combined data structure
charts_data = {
    'generation': {
        'title': "Total Power Generation by Fuel Type",
        'labels': ['Nuclear', 'Gas', 'Hydro', 'Coal', 'Solar'],
        'values': [56939998, 97380973, 8322000, 41732190, 9344000],
        'unit': 'MWh',
        'format': ',.0f'
    },
    'cost': {
        'title': "Total Power Generation Cost by Fuel Type",
        'labels': ['Nuclear Cost', 'Gas Cost', 'Hydro Cost', 'Coal Cost', 'Solar Cost'],
        'values': [1252679939, 3700476909, 122416624, 3171646515, 0],
        'unit': 'USD',
        'format': '$,.0f'
    },
    'co2': {
        'title': "Total CO2 Equivalence Generation by Fuel Type",
        'labels': ['Nuclear CO2 Emission', 'Gas CO2 Emission', 'Hydro CO2 Emission', 'Coal CO2 Emission', 'Solar CO2 Emission'],
        'values': [6715, 42404, 1963, 43727, 3433],
        'unit': 'metric tons',
        'format': ',.0f'
    }
}

# Create subplot figure
fig = make_subplots(
    rows=1, cols=3,
    specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]],
    subplot_titles=tuple(data['title'] for data in charts_data.values()),
    vertical_spacing=0.15
)

# Adjust the y position of subplot titles
for i, annotation in enumerate(fig.layout.annotations):
    annotation.update(y=1.1)

# Color scheme
colors = ['#90EE90', '#E8F8F5', '#87CEEB', '#ADD8E6', '#FFB6C1']

# Add traces using a loop
for i, (chart_type, data) in enumerate(charts_data.items(), 1):
    fig.add_trace(
        go.Pie(
            labels=data['labels'],
            values=data['values'],
            name=chart_type,
            marker_colors=colors,
            texttemplate=(
                "%{label}<br>"
                f"%{{value:{data['format']}}}<br>"
                "(%{percent})"
            ),
            textinfo='text',
            hovertemplate=(
                "<b>%{label}</b><br>"
                f"Value: %{{value:{data['format']}}} {data['unit']}<br>"
                "Percentage: %{percent}%"
                "<extra></extra>"
            )
        ),
        row=1, col=i
    )

# Update layout
fig.update_layout(
    showlegend=False,
    height=600,
    width=1200,
    # title={
    #     'text': "Energy Supply Stack Analysis",
    #     'y':0.95,
    #     'x':0.5,
    #     'xanchor': 'center',
    #     'yanchor': 'top'
    # }
)

# Show in Streamlit
st.header('Supply Stack (Balancing authority: SOCO)')

# Display the pie charts
st.plotly_chart(fig, use_container_width=True)

# make 3 columns and put the totals in the columns. Center them 
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div style='text-align: center;'>Total Power Generation: {sum(charts_data['generation']['values']):,.2f} MWh</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div style='text-align: center;'>Total Generation Cost: {sum(charts_data['cost']['values']):,.2f} USD</div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div style='text-align: center;'>Total CO2 Emissions: {sum(charts_data['co2']['values']):,.2f} metric tons</div>", unsafe_allow_html=True)

# Load and process time series data
@st.cache_data
def load_time_series_data():
    df = pd.read_csv('data/stack model output v0.csv')
    df['Time'] = pd.to_datetime(df['Time'])
    return df

# Load the data
ts_data = load_time_series_data()

# Create time series plots
st.divider()

# Create the cost time series plot
cost_fig = go.Figure()
cost_fig.add_trace(
    go.Scatter(
        x=ts_data['Time'], 
        y=ts_data['Total Cost Model'],
        mode='markers',
        name='Total Cost',
        line=dict(color='#FF5733', width=2)
    )
)

cost_fig.update_layout(
    title="Cost Over Time",
    xaxis_title="Date",
    yaxis_title="Cost (USD)",
    height=450,
    hovermode="x unified",
    margin=dict(l=50, r=50, t=50, b=50),
    xaxis=dict(
        dtick="M1",
        tickformat="%b"
    ),
    yaxis=dict(
        range=[0, max(ts_data['Total Cost Model']) * 1.1]  # Start at 0, end at 110% of max value
    )
)

# Create the generation and emissions plot with dual y-axes
gen_emissions_fig = make_subplots(specs=[[{"secondary_y": True}]])

gen_emissions_fig.add_trace(
    go.Scatter(
        x=ts_data['Time'], 
        y=ts_data['Net Generation Model'],
        mode='markers',
        name='Power Generation',
        line=dict(color='#3366FF', width=3)
    ),
    secondary_y=False
)

gen_emissions_fig.add_trace(
    go.Scatter(
        x=ts_data['Time'], 
        y=ts_data['CO2 Emission Model'],
        mode='markers',
        name='CO2 Emissions',
        line=dict(color='#33CC33', width=3)
    ),
    secondary_y=True
)

gen_emissions_fig.update_layout(
    title="Power Generation and CO2 Emissions Over Time",
    xaxis_title="Date",
    hovermode="x unified",
    height=450,
    margin=dict(l=50, r=50, t=50, b=50),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(
        dtick="M1",
        tickformat="%b"
    )
)

gen_emissions_fig.update_yaxes(
    title_text="Power Generation (MWh)", 
    secondary_y=False,
    range=[0, max(ts_data['Net Generation Model']) * 1.1],  # Start at 0, end at 110% of max value
    title_font=dict(color='#3366FF'),  # Match Power Generation blue color
    tickfont=dict(color='#3366FF')     # Match color for tick labels
)
gen_emissions_fig.update_yaxes(
    title_text="CO2 Emissions (metric tons)", 
    secondary_y=True,
    range=[0, max(ts_data['CO2 Emission Model']) * 1.1],  # Start at 0, end at 110% of max value
    title_font=dict(color='#33CC33'),  # Match CO2 Emissions green color
    tickfont=dict(color='#33CC33')     # Match color for tick labels
)

# Display the time series plots
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(cost_fig, use_container_width=True)

with col2:
    st.plotly_chart(gen_emissions_fig, use_container_width=True)

# Add summary statistics for time series data
col1, col2, col3 = st.columns(3)

# Define metrics data
metrics_data = [
    {
        "column": col1,
        "title": "Average Hourly Cost",
        "value_column": "Total Cost Model",
        "format": "{:,.1f}",
        "prefix": "$"
        
    },
    {
        "column": col2,
        "title": "Average Hourly Generation",
        "value_column": "Net Generation Model",
        "format": "{:,.1f} MWh",
        "prefix": ""
    },
    {
        "column": col3,
        "title": "Average Hourly CO2 Emissions",
        "value_column": "CO2 Emission Model",
        "format": "{:,.1f} metric tons",
        "prefix": ""
    }
]

# Display metrics in a loop
for metric in metrics_data:
    with metric["column"]:
        column_name = metric["value_column"]
        st.metric(
            metric["title"],
            f"{metric['prefix']}{metric['format'].format(ts_data[column_name].mean())}",
            delta=f"{(ts_data[column_name].iloc[-1] - ts_data[column_name].iloc[0]) / ts_data[column_name].iloc[0]:.1%}"
        )