import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
st.header('Supply Stack')

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