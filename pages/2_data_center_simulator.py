import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
from enum import Enum
import os
from scipy import interpolate

class DATACENTER_COOLING_TECH(Enum): # Facility Power / IT Power; different categories for different types of energy
    TRADITIONAL_AIR = 1.8
    ADVANCED_AIR = 1.35
    LIQUID = 1.1
    IMMERSION_COOLING = 1.025

class DATACENTER_TYPE(Enum): # Power per rack (in kW)
    AI = 60
    NETWORK = 5
    TRADITIONAL = 7.5
    ULTRA_HIGH_DENSITY = 85

class DATACENTER_MIX_TYPE(Enum):
    WORST = (1,0,0,0)
    BASELINE = (0,1,0,0) #(0.25,0.5,0.22,0.3)
    BEST = (0,0,0,1)

def compute_BW(DB_temperature, Humidity):
    return DB_temperature * np.arctan(
			0.151977 * np.sqrt(Humidity + 8.313659)) + 0.00391838 * np.sqrt(
			Humidity ** 3) * np.arctan(0.023101 * Humidity) - np.arctan(
			Humidity - 1.676331) + np.arctan(
			DB_temperature + Humidity) - 4.686035

class DatacenterConsumptionModel:
    """
    A virtual data center generator that estimates power consumption and heat generation
    based on cooling technology, datacenter type, and external weather conditions.
    """
    def __init__(self, datacenter_name, datacenter_size, working_temperature=23.33, cooling_technology=None, datacenter_type=None, location='Atlanta', num_datacenters=1):
        self.name = datacenter_name
        self.datacenter_size = datacenter_size # Size of each individual datacenter in KW envelope
        self.num_datacenters = num_datacenters # Number of datacenters of this type
        self.location = location               # City or location where this datacenter operate
        self.working_temperature = working_temperature

        # Fixed but Modifiable:
        self.yearly_mean_temperature = 21.777524 # Modulating the PUE contribution on cooling is a yearly system.
        self.yearly_mean_humidity = 66.44765
        # Enumerators for datacenter type and cooling technology
        if isinstance(cooling_technology, DATACENTER_COOLING_TECH):
            self.cooling_technology = cooling_technology
            self.pue = cooling_technology.value    
        else:
            self.cooling_technology = None
            self.pue = None     
        if isinstance(datacenter_type, DATACENTER_TYPE):
            self.datacenter_type = datacenter_type.value
        else:
            self.datacenter_type = None

        # Load COP regressions
        base_folder = "./data"
        file_list = ["Datacenter_20_Eq.csv", "Datacenter_30_Eq.csv", "Datacenter_45_Eq.csv"]
        get_curve_interpolator = True

        self.COP_tables = self.load_COP_data(base_folder, file_list, get_curve_interpolator)


    def set_cooling_technology(self, cooling_tech):
        """
        Set the cooling technology for the datacenter.
        This will impact the estimated PUE (Power Usage Effectiveness).
        """
        if isinstance(cooling_tech, DATACENTER_COOLING_TECH):
            self.cooling_technology = cooling_tech
            self.pue = cooling_tech.value    
        else:
            self.cooling_technology = None
            self.pue = None     

    def set_datacenter_type(self, datacenter_type):
        """
        Set the type of datacenter.
        This, along with the cooling technology, will determine power consumption.
        """
        self.datacenter_type = datacenter_type

    def estimate_power_consumption(self, DB_temperature, Humidity):
        """
        Estimate the hourly power consumption of the datacenters
        based on the datacenter type, cooling technology, and external weather conditions.
        """
        # Compute Real WB Temperature using Stull formula:
        wetbulb_temperature = compute_BW(DB_temperature=DB_temperature, Humidity=Humidity)
        yearly_wetbulb_temperature = compute_BW(DB_temperature=self.yearly_mean_temperature, Humidity=self.yearly_mean_humidity)

        COP_multiplier = self.estimate_COP(yearly_wetbulb_temperature) / self.estimate_COP(wetbulb_temperature) # How much "worse" a warmer weather is compared to a cooler weather

        # print('COP_scenario: '+str(self.estimate_COP(wetbulb_temperature)))
        # print('COP_average: ' + str(self.estimate_COP(yearly_wetbulb_temperature)))
        # print('COP_ratio: '+str(COP_multiplier))
        # IT_equipment_power = (self.datacenter_size * self.num_datacenters) / self.pue # Share of the power that is IT only
        #
        # non_IT_power = (self.datacenter_size * self.num_datacenters) - IT_equipment_power

        IT_equipment_power = (self.datacenter_size * self.num_datacenters)  # Share of the power that is IT only by design

        non_IT_power = IT_equipment_power * (self.pue - 1)

        non_IT_cooling_power = 0.74 * non_IT_power # Other uses for non_IT_power, such as lighting and electricity transformed should not be counted

        non_IT_misc_power = 0.26 * non_IT_power # Lighting and electricity generation

        fixed_power = IT_equipment_power + non_IT_misc_power  # Power in the datacenter that will not fluctuate due to weather

        weather_induced_cooling_power = non_IT_cooling_power * (COP_multiplier)

        total_power = fixed_power + weather_induced_cooling_power

        cooling_power = weather_induced_cooling_power

        return total_power, cooling_power
    
    def estimate_fixed_pue_power_consumption(self, DB_temperature, Humidity, pue_mix):
        """
        Estimate the hourly power consumption of the datacenters
        based on the datacenter type, cooling technology, and external weather conditions.
        """
        # Compute Real WB Temperature using Stull formula:
        wetbulb_temperature = compute_BW(DB_temperature=DB_temperature, Humidity=Humidity)
        yearly_wetbulb_temperature = compute_BW(DB_temperature=self.yearly_mean_temperature, Humidity=self.yearly_mean_humidity)

        COP_multiplier = self.estimate_COP(yearly_wetbulb_temperature) / self.estimate_COP(wetbulb_temperature) # How much "worse" a warmer weather is compared to a cooler weather

        # print('COP_scenario: '+str(self.estimate_COP(wetbulb_temperature)))
        # print('COP_average: ' + str(self.estimate_COP(yearly_wetbulb_temperature)))
        # print('COP_ratio: '+str(COP_multiplier))
        # IT_equipment_power = (self.datacenter_size * self.num_datacenters) / self.pue # Share of the power that is IT only
        #
        # non_IT_power = (self.datacenter_size * self.num_datacenters) - IT_equipment_power

        IT_equipment_power = (self.datacenter_size * self.num_datacenters)  # Share of the power that is IT only by design
        estimated_pue = pue_mix.value[0]*1.5 + pue_mix.value[1] * 1.35 + pue_mix.value[2] * 1.1 + pue_mix.value[3] * 1.025 
        non_IT_power = IT_equipment_power * (estimated_pue- 1)

        non_IT_cooling_power = 0.74 * non_IT_power # Other uses for non_IT_power, such as lighting and electricity transformed should not be counted

        non_IT_misc_power = 0.26 * non_IT_power # Lighting and electricity generation

        fixed_power = IT_equipment_power + non_IT_misc_power  # Power in the datacenter that will not fluctuate due to weather

        weather_induced_cooling_power = non_IT_cooling_power * (COP_multiplier)

        total_power = fixed_power + weather_induced_cooling_power

        cooling_power = weather_induced_cooling_power

        return total_power, cooling_power

    def estimate_heat_generation(self, efficiency=0.6):
        """
        Estimate the heat generation of the datacenters
        to enable potential use of excess heat for other purposes.
        """
        heat_conduction_efficiency = efficiency # Lower bound taken, could be up to 95%

        # IT_equipment_power = (self.datacenter_size * self.num_datacenters) / self.pue # Share of the power that is IT only
        IT_equipment_power = (self.datacenter_size * self.num_datacenters)  # Share of the power that is IT only by design
        
        return IT_equipment_power * heat_conduction_efficiency
    
    def load_COP_data(self, base_folder, list_files, make_spline=True):
        file_tables = {}
        for a_file in list_files:
            file_location = os.path.join(base_folder, a_file)
            my_data = np.genfromtxt(file_location, delimiter=',', skip_header=1)
            number_on_file = [int(s) for s in a_file.split('_') if s.isdigit()]
            temperature_focus = number_on_file[0]
            if make_spline:
                f_COP = interpolate.interp1d(np.squeeze(my_data[:,0]), np.squeeze(my_data[:,1]))
                file_tables[temperature_focus] = f_COP
            else:
                file_tables[temperature_focus] = my_data
        return file_tables

    def estimate_COP(self, wetbulb_temperature):
        temperature_list = list(self.COP_tables.keys())
        for i in range(1,len(temperature_list)):
            if self.working_temperature == temperature_list[i-1]:
                min_index = i-1
                max_index = i-1
            elif self.working_temperature > temperature_list[i-1] and self.working_temperature < temperature_list[i]:
                min_index = i-1
                max_index = i
            elif self.working_temperature == temperature_list[i]:
                min_index = i
                max_index = i
            elif self.working_temperature > temperature_list[-1]:
                min_index = len(temperature_list) - 1
                max_index = len(temperature_list) - 1
        COP_low_table = self.COP_tables[temperature_list[min_index]]
        COP_high_table = self.COP_tables[temperature_list[max_index]]

        COP_low = COP_low_table(wetbulb_temperature)
        COP_high = COP_high_table(wetbulb_temperature)

        COP_estimated = (self.working_temperature - temperature_list[min_index])/(temperature_list[max_index] - temperature_list[min_index])* (COP_high - COP_low) + COP_low

        return COP_estimated


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

def compute_datacenter_water_usage(datacenter: DatacenterConsumptionModel, dbt: float, hum: float, water_usage, pue_mix: tuple):
    dbt = (dbt - 32) * (5/9)
    total_power, _ = datacenter.estimate_fixed_pue_power_consumption(dbt, hum, pue_mix)

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
- Datacenter Cooling Technology - Changes the Power Usage Effectivenes (PUE) for the simulated datacenters.
- Datacenter Heat Recovery Efficiency - Changes the sensitivity of the datacenter cooling system to changes in temperature
- Datacenter water usage in gallons per kWh - Changes the relative water usage per kWh of power consumed (varies depending on datacenter technology and construction)
- Datacenter PUE makeup - For water usage estimation, it changes the distribution of technologies across Atlanta (worst is all air, baseline reflects better the distribution in Atlanta, and best is all immersion cooling).           
""")

st.markdown("""
##### The graph uses data for the entire year of 2022 quantified at the hourly level. Afterwards, please scroll down to see a map of datacenter demand. 
""")
st.divider()

st.markdown("<div style='text-align: center;'><h2>Current Datacenters in Atlanta</h2></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.imgur.com/NECuOYk.png" width="30%">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.85em;'>"
    "Credit: Science for Georgia. Includes completed, planned data centers and crypto mines"
    "</div>",
    unsafe_allow_html=True
)

st.divider()
st.header('Simulation Control')
col1, col2 = st.columns(2)

datacenter_offset = col1.slider("Individual Datacenter IT (computing) Power MW", 0.0, 50.0, 20.0)
datacenter_number = col1.slider("Number of Upcoming Simulated Datacenters", 0, 83, 40)
datacenter_working_temperature = col2.slider("Datacenter Working Temp (F)", 69, 95, 77)
technology = col2.radio("Datacenter Cooling Technology", [DATACENTER_COOLING_TECH.TRADITIONAL_AIR, 
DATACENTER_COOLING_TECH.ADVANCED_AIR, DATACENTER_COOLING_TECH.LIQUID, DATACENTER_COOLING_TECH.IMMERSION_COOLING],
captions=["Traditional Air", "Advanced Air", "Liquid Cooling", "Immersion Cooling"])
datacenter_water_rate = col2.slider("Datacenter water usage gallons per kWh", 0.132086, 0.5, 0.25)

pue_mix = col2.radio("Datacenter PUE Makup", [DATACENTER_MIX_TYPE.WORST, 
DATACENTER_MIX_TYPE.BASELINE, DATACENTER_MIX_TYPE.BEST],
captions=["Air Only", "Georgia Average", "Latest Technology"])
datacenter_heat_eff = col1.slider("Datacenter Heat Recovery Efficiency", 0.2, 0.95, 0.6)
st.header('Simulation Results')

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
    lambda x: compute_datacenter_water_usage(siemens_datacenter, x['DBT'], x['Rhum'], datacenter_water_rate, pue_mix), axis=1
)

# data_industrial['Datacenter Usable Heatload (MW)'] = data_industrial.apply(
#     lambda x: compute_datacenter_usable_heatload(siemens_datacenter, datacenter_heat_eff), axis=1
# )
col1, col2 = st.columns(2)
# Computing sample for pie chart:
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
with col1:
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
    # st.divider()

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
    # st.divider()

with col2:
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
    # st.divider()

st.markdown("<div style='text-align: center;'><h2>Datacenter Scenario Breakdown</h2></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.imgur.com/9Svlpv2.png" width="45%">
        <img src="https://i.imgur.com/U9M6cNF.png" width="45%">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.imgur.com/MmIBOQw.png" width="45%">
        <img src="https://i.imgur.com/BqGBpkf.png" width="45%">
    </div>
    """,
    unsafe_allow_html=True
)

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
