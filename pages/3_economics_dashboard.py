# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 19:34:03 2024

@author: Jake Churchill
"""

import streamlit as st
from streamlit_folium import st_folium, folium_static
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Defining page

APP_TITLE = "Highlight - Solar's Growth and Coal's Decline"
APP_SUBTITLE = "Jake Churchill, Dr. Richard Simmons, Chenghao Duan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout='wide'
)
st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

# Begin App
st.write('## How has a change in energy generation impact jobs throughout Georgia?')
st.write('### First, see the increase in Solar generation, and the accompaning jobs.')

# Get the data
jobsdata = pd.read_csv(r'data/Historical/Energy Jobs/State Level Jobs.csv')
yearsjobs = jobsdata['Year']
solarjobs = jobsdata['Solar']
coaljobs = jobsdata['Coal']

GenerationData = pd.read_csv(r'data/Historical/Generation/SOCO Annual Generation.csv')
yearsGen = GenerationData['Year']
solarGen = GenerationData['Solar'] / 1e6 #Converting from MWh to TWh
coalGen = GenerationData['Coal'] / 1e6

fig1, ax11 = plt.subplots(figsize=(20,10))
ax11.plot(yearsGen, solarGen, color = 'green', marker='o', linewidth= 4)
ax11.set_title('Solar Generation and Jobs', fontsize= 30)
ax11.set_xlabel('Year', fontsize= 20)
ax11.set_ylabel('Solar Generation in SOCO [TWh]', color='green',fontsize= 20)
ax11.tick_params(axis='x', which='major', labelsize= 16)
plt.legend(['Solar Generation'],loc='upper left', fontsize= 20)
plt.yticks(fontsize= 18)

ax12 = ax11.twinx()
ax12.plot(yearsjobs, solarjobs, color='blue', marker= 'o', linewidth= 4)
ax12.set_ylabel('Solar Jobs in the State of Georgia', color='blue',fontsize = 20)
ax12.tick_params(axis='y', which='major', labelsize = 16, color='blue')
plt.yticks(fontsize = 18)
plt.legend(['Solar Jobs'],loc='upper center', fontsize = 20)
st.pyplot(fig1)

# Give brief comment on the significance of the figure
st.write('#### Since 2016 the number of solar jobs in Georgia has increased by 50%. Meanwhile, solar generation has more than doubled in SOCO.')
st.write('### Where are solar jobs being created?')

## Second Figure
# Map of Change in SOLAR JOBS BY COUNTY from 2016 to 2022 
jobs2016 = pd.read_csv(r'data/GIS/Energy Jobs/GA USEER County 2016.csv')
solarjobs2016 = jobs2016[' Solar ']
jobs2022 = pd.read_csv(r'data/GIS/Energy Jobs/GA USEER County 2022.csv')
solarjobs2022 = jobs2022[' Solar '] #Named " Solar " actually
solarjobsdiff = solarjobs2022 - solarjobs2016

#Make it a dataframe 
solarjobschange = pd.DataFrame({'FIPS':jobs2016['FIPS'], 'Solar':solarjobsdiff})
#Turn this into a geojson to plot
geojson = gpd.read_file(r'data/GIS/Geojsons/georgia-with-county-boundaries_1092.geojson') #Counties in GA

# Ensure FIPS codes in both files are in the same format (string with leading zeros)
solarjobschange['FIPS'] = solarjobschange['FIPS'].astype(str).str.zfill(5)
geojson['FIPS'] = geojson['id'].astype(str).str.zfill(5)

# Merge CSV data into the GeoJSON data on the FIPS code
merged_solar = geojson.merge(solarjobschange, on='FIPS')

# MAP solarjobschange
vmin = merged_solar['Solar'].min()  # Minimum value for the color scale
vmax = merged_solar['Solar'].max()  # Maximum value for the color scale

fig2, ax2 = plt.subplots(1, 1, figsize=(10, 6))
merged_solar.plot(column='Solar', cmap='Blues', ax=ax2, vmin=vmin, vmax=vmax)

# Customize legend (optional)
cbar = ax2.get_figure().colorbar(ax2.collections[0], ax=ax2)
cbar.set_label('Number of Jobs')
#cbar.set_ticks([vmin, vmax])  # You can set custom tick positions

# Add titles and labels (optional)
plt.title('Change in Solar Jobs from 2016 to 2022')
plt.xticks(ticks=[],labels=[])
plt.yticks(ticks=[],labels=[])
st.pyplot(fig2)

st.write('#### Solar job growth is much higher in some counties. Highest growth can be seen in Fulton, DeKalb, and Whitfield counties.')
url1 = "https://gov.georgia.gov/press-releases/2022-05-26/gov-kemp-solar-energy-giant-qcells-power-470-new-jobs-whitfield-county"
st.write("##### Read more about Qcells in Whitfield county [here](%s)" % url1)

st.write('### Now, see how coal has changed over the same time period.')
#Same plot but for coal Jobs
fig3, ax31 = plt.subplots(figsize=(20,10))
ax31.plot(yearsGen,coalGen, color = 'red', marker='o', linewidth= 4)
ax31.set_title('Coal Generation and Jobs',fontsize = 28)
ax31.set_xlabel('Year', fontsize = 20)
ax31.set_ylabel('Coal Generation in SOCO [TWh]', color='red',fontsize = 20)
ax31.tick_params(axis='x', which='major', labelsize = 16)
plt.legend(['Coal Generation'],loc='upper center', fontsize=20)
plt.yticks(fontsize = 18)

ax32 = ax31.twinx()
ax32.plot(yearsjobs, coaljobs, color='black', marker= 'o', linewidth= 4)
ax32.set_ylabel('Coal Jobs in Georgia', color='black',fontsize = 20)
ax32.tick_params(axis='y', which='major', labelsize = 16, color='black')
plt.yticks(fontsize = 18)
plt.legend(['Coal Jobs'],loc='upper left', fontsize=20)
st.pyplot(fig3)
st.write('#### Coal generation has seen a decrease of 30% and coal jobs have dropped 25%.')

st.write('### Where has emplyment in coal changed most?')
# COAL MAP
coaljobs2016 = jobs2016[' Coal ']
coaljobs2022 = jobs2022[' Coal ']
coaljobsdiff = coaljobs2022 - coaljobs2016

# Make it a dataframe 
coaljobschange = pd.DataFrame({'FIPS':jobs2016['FIPS'], 'Coal':coaljobsdiff})

# Ensure FIPS codes in both files are in the same format (string with leading zeros)
coaljobschange['FIPS'] = coaljobschange['FIPS'].astype(str).str.zfill(5)
geojson['FIPS'] = geojson['id'].astype(str).str.zfill(5)

# Merge CSV data into the GeoJSON data on the FIPS code
merged_coal = geojson.merge(coaljobschange, on='FIPS')
# MAP coaljobschange
vmin = merged_coal['Coal'].min()  # Minimum value for the color scale
vmax = merged_coal['Coal'].max()  # Maximum value for the color scale

fig4, ax4 = plt.subplots(1, 1, figsize=(10, 6))
merged_coal.plot(column='Coal', cmap='RdGy', ax=ax4, vmin=vmin, vmax=vmax)

# Customize legend (optional)
cbar = ax4.get_figure().colorbar(ax4.collections[0], ax=ax4)
cbar.set_label('Number of Jobs')
#cbar.set_ticks([vmin, vmax])  # You can set custom tick positions

# Add titles and labels (optional)
plt.title('Change of Coal Jobs 2016 to 2022')
plt.xticks(ticks=[],labels=[])
plt.yticks(ticks=[],labels=[])
st.pyplot(fig4)

st.write('### Significant job growth can be seen in DeKalb County, but elsewhere plant shutdowns have seen job decreases.')
url2 = "https://www.northwestgeorgianews.com/rome/business/hammond-is-officially-shut-down/article_b2ee362e-a7da-11e9-8109-33b8c382a50d.html"
st.write("##### Read more about Plant Hammond in Floyd County closing in 2019 [here](%s)" % url2)
# I would love to have an exaplanation of the growth in coal jobs in DeKalb county. But I can't.
st.write('### Using historical trends and maps, we can better understand the relationship between generation and jobs.')
# Show the plots
plt.show()







