import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def compute_contribution(dbt, tip_point, industrial_consumption, datacenter_offset, cooling_penalty):
    if dbt > tip_point:
        return industrial_consumption + datacenter_offset + (dbt - tip_point) * cooling_penalty
    else:
        return industrial_consumption + datacenter_offset

st.write("# Datacenter Acquisition Simulator")

data_industrial = pd.read_csv(r'data/Consumed_industrial_kW.csv')

col1, col2 = st.columns(2)

datacenter_offset = col1.slider("Datacenter Base Power MW", 0.0, 350.0, 150.0)
tip_point_F = col2.slider("Tip point (F)", 45, 65, 50)
cooling_penalty = col1.slider("Cooling Penalty %", 0.0, 30.0, 15.0)

data_industrial['Datacenter Contribution (MW)'] = data_industrial.apply(lambda x: compute_contribution(x['DBT'], tip_point_F, x['Consumed Industrial'], datacenter_offset, cooling_penalty), axis=1)

fig, ax = plt.subplots(figsize=(25,6))
ax.plot(data_industrial.index, data_industrial['Consumed Industrial'], label='Industrial')
ax.plot(data_industrial.index, data_industrial['Datacenter Contribution (MW)'], label='Industrial + Datacenters')
ax.legend(loc="upper left")
ax.set_title('Datacenter Power Consumption')
ax.set_xlabel('Time of Year (Hour from 1/1/2022)')
ax.set_ylabel('Industry Power Consumption (MW)')

st.pyplot(fig) # Just plot after. Simple.
