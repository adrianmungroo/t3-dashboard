import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from datacenter import DatacenterConsumptionModel, DATACENTER_COOLING_TECH, DATACENTER_TYPE

def compute_datacenter_contribution(datacenter: DatacenterConsumptionModel, dbt: float, hum: float,
                                    industrial_consumption: float):
    dbt = (dbt - 32) * (5/9)
    total_power, _ = datacenter.estimate_power_consumption(dbt, hum)

    return industrial_consumption + total_power

def compute_datacenter_total_power(datacenter: DatacenterConsumptionModel, dbt: float, hum: float):
    dbt = (dbt - 32) * (5/9)
    total_power, _ = datacenter.estimate_power_consumption(dbt, hum)

    return total_power

def compute_datacenter_cooling_power(datacenter: DatacenterConsumptionModel, dbt: float, hum: float):
    dbt = (dbt - 32) * (5/9)
    _, cooling_power = datacenter.estimate_power_consumption(dbt, hum)

    return cooling_power

def compute_datacenter_water_usage(datacenter: DatacenterConsumptionModel, dbt: float, hum: float, water_usage):
    dbt = (dbt - 32) * (5/9)
    total_power, _ = datacenter.estimate_fixed_pue_power_consumption(dbt, hum)

    total_water_usage = water_usage * total_power * 1000

    return total_water_usage

def compute_datacenter_usable_heatload(datacenter: DatacenterConsumptionModel, efficiency: float):
    heating_power = datacenter.estimate_heat_generation(efficiency=efficiency)

    return heating_power

APP_TITLE = "Data Center Simulator"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Adrian Mungroo, Hyun Woo Kim, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🖥️",
    layout='wide'
)

data_industrial = pd.read_csv(r'data/Power_Consumption_KW.csv')

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

datacenter_offset = col1.slider("Individual Datacenter IT (computing) Power MW", 0.0, 50.0, 20.0)
datacenter_number = col1.slider("Number of Upcoming Simulated Datacenters", 0, 83, 40)
datacenter_working_temperature = col2.slider("Datacenter Working Temp (F)", 69, 95, 77)
technology = col2.radio("Datacenter Cooling Technology", [DATACENTER_COOLING_TECH.TRADITIONAL_AIR, 
DATACENTER_COOLING_TECH.ADVANCED_AIR, DATACENTER_COOLING_TECH.LIQUID, DATACENTER_COOLING_TECH.IMMERSION_COOLING],
captions=["Traditional Air", "Advanced Air", "Liquid Cooling", "Immersion Cooling"])
datacenter_heat_eff = col2.slider("Datacenter Heat Recovery Efficiency", 0.2, 0.95, 0.6)
datacenter_water_rate = col1.slider("Datacenter water usage gallons per kWh", 0.132086, 0.5, 0.25)
# Example with units in MW
power_consumption = datacenter_offset
datacenter_name = 'Siemens'
working_temp = (datacenter_working_temperature - 32) * (5/9)
cooling_tech = technology
datacenter_type = DATACENTER_TYPE.AI

siemens_datacenter = DatacenterConsumptionModel(datacenter_name, power_consumption * datacenter_number, working_temp, cooling_tech, datacenter_type, 'Atlanta', 1)

data_industrial['Datacenter Contribution (MW)'] = data_industrial.apply(
    lambda x: compute_datacenter_contribution(siemens_datacenter, x['DBT'], x['Rhum'], x['Total Consumed']), axis=1
)

data_industrial['Datacenter Total (MW)'] = data_industrial.apply(
    lambda x: compute_datacenter_total_power(siemens_datacenter, x['DBT'], x['Rhum']), axis=1
)

data_industrial['Datacenter Cooling (MW)'] = data_industrial.apply(
    lambda x: compute_datacenter_cooling_power(siemens_datacenter, x['DBT'], x['Rhum']), axis=1
)

data_industrial['Datacenter Water Gallons'] = data_industrial.apply(
    lambda x: compute_datacenter_water_usage(siemens_datacenter, x['DBT'], x['Rhum'], datacenter_water_rate), axis=1
)

# data_industrial['Datacenter Usable Heatload (MW)'] = data_industrial.apply(
#     lambda x: compute_datacenter_usable_heatload(siemens_datacenter, datacenter_heat_eff), axis=1
# )

# Computing sample for pie chart:
# Scenario
temperature = 35 #C
humidity = 68 #Percent
total_power, cooling_power = siemens_datacenter.estimate_power_consumption(temperature, humidity)

d = {'Power Type': ['Non-Cooling Power (MW)', 'Cooling Power (MW)'], 'Power MW': [total_power-cooling_power, cooling_power]}
df = pd.DataFrame(data=d)

fig = px.pie(df, values='Power MW', names='Power Type',
                 title=f'Datacenter Composition during Summer',
                 height=300, width=200)
fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
col1.plotly_chart(fig, use_container_width=True)

start_date = pd.Timestamp('2022-01-01') # Making hours into datetime since we know the beginning date
data_industrial['DateTime'] = pd.date_range(start=start_date, periods=len(data_industrial), freq='h')

# Create a Plotly figure
fig = go.Figure()

fig.add_trace(go.Scatter(x=data_industrial['DateTime'], y=data_industrial['Total Consumed'], mode='lines', name='Overal Retail Demand', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=data_industrial['DateTime'], y=data_industrial['Datacenter Contribution (MW)'], mode='lines', name='Overal Retail Demand + Datacenters', line=dict(color='coral')))

fig.update_layout(
    xaxis_title='Time of Year',
    yaxis_title='Industry Power Consumption (MW)',
    legend=dict(x=0, y=1),
    template='plotly_white'  
)
st.plotly_chart(fig)
st.divider()

# Create a Plotly figure
fig2 = go.Figure()

fig2.add_trace(go.Scatter(x=data_industrial['DateTime'], y=data_industrial['Datacenter Total (MW)'], mode='lines', name='Total Datacenter Consumption', line=dict(color='blue')))
fig2.add_trace(go.Scatter(x=data_industrial['DateTime'], y=data_industrial['Datacenter Cooling (MW)'], mode='lines', name='Datacenter Cooling Power Required', line=dict(color='green')))
# fig2.add_trace(go.Scatter(x=data_industrial['DateTime'], y=data_industrial['Datacenter Usable Heatload (MW)']/datacenter_heat_eff, mode='lines', name='Datacenter IT power', line=dict(color='black')))
# fig2.add_trace(go.Scatter(x=data_industrial['DateTime'], y=data_industrial['Datacenter Usable Heatload (MW)'], mode='lines', name='Datacenter useable heatload', line=dict(color='red')))
data_industrial.to_csv('Ind_results.csv', index=False)
fig2.update_layout(
    xaxis_title='Time of Year',
    yaxis_title='Power (MW)',
    legend=dict(x=1, y=1),
    template='plotly_white'
)

st.plotly_chart(fig2)
st.divider()

# Create a Plotly figure
df_monthly_sum = data_industrial.resample('MS', on='DateTime').sum()
df_monthly_sum.to_csv('monthly_results.csv', index=False)

df_daily_sum = data_industrial.resample('D', on='DateTime').sum()
df_daily_sum.to_csv('daily_results.csv', index=False)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=data_industrial['DateTime'], y=data_industrial['Datacenter Water Gallons'], mode='lines', name='Total Datacenter Water Consumption', line=dict(color='blue')))

fig3.update_layout(
    xaxis_title='Time of Year',
    yaxis_title='Hourly Water Usage (Gal)',
    legend=dict(x=1, y=1),
    template='plotly_white'
)



st.plotly_chart(fig3)
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
