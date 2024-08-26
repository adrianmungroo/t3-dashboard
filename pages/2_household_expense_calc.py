import streamlit as st
import pandas as pd

st.write("# Household Energy Expenditure Simulator")

st.write("### Input Parameters")
col1, col2 = st.columns(2)
house_size = col1.slider("House Size", 0.0, 1.0, 0.5)
electricity_price = col2.slider("Electricity Price $usd", 0.05, 0.25, 0.09)
gas_price = col2.slider("Gas Price $usd", 0.25, 1.25, 0.55)
outside_temp = col2.slider("Outside Temperature F", 20, 38, 25)
set_temp = col2.slider("Set Temp F", 65, 78, 72)
heating_type = col1.radio(
    "Heating Technology Type",
    [":rainbow[Heat Pumps]", "***Boiler***", "Electric Heating"],
    captions=[
        "More efficient with better insulation",
        "Gas-based",
        "Most inefficient, no gas needed",
    ],
)

# Setting up computations:

heating_gas_consumption = 0
heating_elec_consumption = 0
bad_insulation_penalty = 1

heating_temp = set_temp - outside_temp

if heating_type == "***Boiler***":
    heating_gas_consumption += 3.0 * heating_temp * house_size
    bad_insulation_penalty = 1.1

if heating_type == ":rainbow[Heat Pumps]":
    heating_elec_consumption += 1.0 * heating_temp * house_size * 250
    bad_insulation_penalty = 2

if heating_type == "Electric Heating":
    heating_elec_consumption += 3.0 * heating_temp * house_size * 250
    bad_insulation_penalty = 1.25

base_elec_non_DAC = house_size * 2500
base_elec_DAC = house_size * 1800

heating_elec_non_DAC = heating_elec_consumption
heating_elec_DAC = bad_insulation_penalty * heating_elec_consumption

total_elec_non_DAC = base_elec_non_DAC + heating_elec_non_DAC
total_elec_DAC = base_elec_DAC + heating_elec_DAC

cost_heating_non_DAC = gas_price * heating_gas_consumption * 0.1 + electricity_price * (heating_elec_non_DAC) / 1000
cost_heating_DAC = gas_price * heating_gas_consumption * 0.1 + electricity_price * (heating_elec_DAC) / 1000

cost_total_non_DAC = electricity_price * base_elec_non_DAC / 1000 + cost_heating_non_DAC
cost_total_DAC = electricity_price * base_elec_DAC / 1000 + cost_heating_DAC

df = pd.DataFrame({"Household Type": ["Non-DAC","Non-DAC","DAC","DAC"],
                   "Type": ["Misc Cost", "Heating Cost","Misc Cost", "Heating Cost"],
                   "Price $ per hour": [cost_total_non_DAC, cost_heating_non_DAC, cost_total_DAC, cost_heating_DAC]})

st.bar_chart(df, x="Household Type", y="Price $ per hour", color="Type", stack=False)