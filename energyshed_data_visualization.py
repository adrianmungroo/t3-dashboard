import streamlit as st
from streamlit_folium import st_folium, folium_static
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import matplotlib.colors as mcolors
import plotly.express as px

# Defining page

APP_TITLE = "Energyshed Dashboard"
APP_SUBTITLE = "Dr. Jung-Ho Lewe, Dr. David Solano, Dr. Scott Duncan, Adrian Mungroo, Hyun Woo Kim, Meiwen Bi, Imran Aziz and Yunmei Guan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout='wide'
)

# Column dictionary for all the selectable datasets

# column_dictionary = {'GIS' : {'counties': ['Energy Burden 2016', 'Energy Burden 2021', 'Energy Burden 2022', 'Solar 2016', 'Coal 2016', 'Natural Gas 2016',
#               'Solar 2020', 'Coal 2020', 'Natural Gas 2020', 'Solar 2021','Coal 2021', 'Natural Gas 2021', 'Solar 2022', 'Coal 2022',
#               'Natural Gas 2022', 'Median AQI 2016', 'Median AQI 2017', 'Median AQI 2018', 'Median AQI 2019', 'Median AQI 2020',
#               'Median AQI 2021', 'Median AQI 2022'],
#  'tracts': ['DAC Boolean', 'Energy Burden 2016', 'Energy Burden 2021','Energy Burden 2022']},
#  'Historical' : ['SOCO Consumer Cost', 'SOCO Sold MWh', 'State Level Jobs', 'SOCO Annual Generation', 'GA_AnnualEmissions', 'AQI Scores Fulton']}

column_dictionary = {'GIS' : {'counties': ['Energy Burden 2016', 'Energy Burden 2021', 'Energy Burden 2022', 'Solar 2016', 'Coal 2016', 'Natural Gas 2016',
              'Solar 2020', 'Coal 2020', 'Natural Gas 2020', 'Solar 2021','Coal 2021', 'Natural Gas 2021', 'Solar 2022', 'Coal 2022',
              'Natural Gas 2022', 'Median AQI 2016', 'Median AQI 2017', 'Median AQI 2018', 'Median AQI 2019', 'Median AQI 2020',
              'Median AQI 2021', 'Median AQI 2022'],
 'tracts': ['DAC Boolean', 'Energy Burden 2016', 'Energy Burden 2021','Energy Burden 2022']},
 'Historical' : ['State Level Jobs', 'GA_AnnualEmissions', 'AQI Scores Fulton']}

# Helper Functions

def get_color(value, min_value, max_value, color_scale):
    if value is None:
        return '#000000'
    normalized = (value - min_value) / (max_value - min_value)
    cmap = plt.get_cmap(color_scale)
    color = mcolors.to_hex(cmap(normalized))
    return color

def plotGISGraph(chosen, subgroup, key_suffix):
    data = gpd.read_file(f'data/GIS/{subgroup}.geojson')
    data_json = data.to_json()
    column_choice = chosen  # Just a reassignment

    m = folium.Map(prefer_canvas=True, zoom_control=False, 
                   tiles='http://tile.openstreetmap.org/{z}/{x}/{y}.png', 
                   attr='basemap-choice',
                   location=[32.9, -82.91], zoom_start=7)
    
    if column_choice:
        min_value = data[column_choice].min()
        max_value = data[column_choice].max()  

        def style_function(feature):
            value = feature['properties'][column_choice]
            color = get_color(value, min_value, max_value, 'Reds')
            return {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 1
            }  
        
        folium.GeoJson(
            data_json,
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(
                fields=[column_choice],  # 'name' or any other property in your GeoJSON, and column_choice for data values
                aliases=[column_choice],  # Optional: aliases for the fields
                localize=True,
                sticky=True
            ),
            name=f'{column_choice}'
        ).add_to(m)
    
    st_folium(m, width=750, height=500, key=f'map_{key_suffix}')

def plotHistoricalGraph(name, key_suffix):

    df = pd.read_csv(f'data/Historical/{name}.csv')

    fig = px.line(df, x='Year', y=df.columns[1:], markers=True, title=f"{name}")

    if name == "State Level Jobs":
        visible_columns = ["Solar", "Electric power generation total"]
    else:
        visible_columns = [df.columns[1]]  # Keep the first column visible by default in other cases

    # Update traces to show only specified columns, hide the rest
    for i, trace in enumerate(fig.data):
        if df.columns[i + 1] in visible_columns:  # Check if the column is in the visible list
            trace.visible = True
        else:
            trace.visible = 'legendonly'

    # Customize the layout for better readability
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Values',
        legend_title='Series',
        hovermode='x unified',  # Show all values when hovering over a point
    )
    st.plotly_chart(fig, use_container_width=True, key=f'graph_{key_suffix}')

# Define state

if 'gis_filter_1' not in st.session_state:
    st.session_state.gis_filter_1 = True # initialize it as true
    # st.session_state.historical_filter_1 = False

if 'historical_filter_1' not in st.session_state:
    st.session_state.historical_filter_1 = False

if 'gis_filter_2' not in st.session_state:
    st.session_state.gis_filter_2 = False

if 'historical_filter_2' not in st.session_state:
    st.session_state.historical_filter_2 = True

# Begin app

st.write("""
# Welcome to the Energyshed Dashboard!

##### This interactive tool is designed to help you explore and visualize important data and forecasts related to energy and environmental metrics.          
         
##### Click the tabs on the left navigational panel to explore the different features this tool provides. 
""")

st.divider()

st.markdown("""
##### Please interact with the visualization tool below by clicking the buttons to switch between maps and graphs.

#####  Please click the dropdown menus to visualize different datasets.            
""")

column1, column2 = st.columns(2)

with column1:
    subcolumn1_1, subcolumn2_1 = st.columns(2) # the underscore 1 is to signify the left main column

    if subcolumn1_1.button('MAP', key = 'gis_button_1'):
        st.session_state.gis_filter_1 = True
        st.session_state.historical_filter_1 = False 
    
    if subcolumn2_1.button('GRAPH', key = 'hist_button_1'):
        st.session_state.historical_filter_1 = True
        st.session_state.gis_filter_1 = False
    
    if st.session_state.gis_filter_1:
        layer_list = column_dictionary['GIS']['counties'] + column_dictionary['GIS']['tracts']
        chosen = st.selectbox('Click to select a dataset below', layer_list, key = 'gis_list_1')

        if chosen in column_dictionary['GIS']['counties']:
            subgroup = 'counties'
        elif chosen in column_dictionary['GIS']['tracts']:
            subgroup = 'tracts'

        plotGISGraph(chosen, subgroup, 1)

    elif st.session_state.historical_filter_1:
        layer_list = column_dictionary['Historical']
        chosen = st.selectbox('Click to select a dataset below', layer_list, key = 'hist_list_1')

        plotHistoricalGraph(chosen, 1)


##########################################
##########################################
#########      ############       ########
##########################################
##########################################
##########################################
##########################################
##################       #################
##########################################


with column2:
    subcolumn1_2, subcolumn2_2 = st.columns(2) # the underscore 2 is to signify the left main column

    if subcolumn1_2.button('MAP', key = 'gis_button_2'):
        st.session_state.gis_filter_2 = True
        st.session_state.historical_filter_2 = False 
    
    if subcolumn2_2.button('GRAPH', key = 'hist_button_2'):
        st.session_state.historical_filter_2 = True
        st.session_state.gis_filter_2 = False
    
    if st.session_state.gis_filter_2:
        layer_list = column_dictionary['GIS']['counties'] + column_dictionary['GIS']['tracts']
        chosen = st.selectbox('Click to select a dataset below', layer_list, key = 'gis_list_2')

        if chosen in column_dictionary['GIS']['counties']:
            subgroup = 'counties'
        elif chosen in column_dictionary['GIS']['tracts']:
            subgroup = 'tracts'

        plotGISGraph(chosen, subgroup, 2)
    
    elif st.session_state.historical_filter_2:
        layer_list = column_dictionary['Historical']
        chosen = st.selectbox('Click to select a dataset below', layer_list, key = 'hist_list_2')

        plotHistoricalGraph(chosen, 2)

st.divider()
st.caption(APP_SUBTITLE)