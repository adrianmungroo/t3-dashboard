import streamlit as st
from streamlit_folium import st_folium, folium_static
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Defining page

APP_TITLE = "Task 3 Dashboard"
APP_SUBTITLE = "Adrian Mungroo, David Solano, Hyun Woo Kim, Robert Churchill, Chenghao Duan"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout='wide'
)
st.title('Hello World')
st.caption(APP_SUBTITLE)

# Dictionary defining what the types of each dataset

data_dictionary = {'Energy Burden' : ['gis','historical'], 'Jobs' : ['historical'], 'PM25' : ['historical']}

# Define state

if 'gis_filter_1' not in st.session_state:
    st.session_state.gis_filter_1 = False

if 'historical_filter_1' not in st.session_state:
    st.session_state.historical_filter_1 = False

if 'gis_filter_2' not in st.session_state:
    st.session_state.gis_filter_2 = False

if 'historical_filter_2' not in st.session_state:
    st.session_state.historical_filter_2 = False

# Begin app

column1, column2 = st.columns(2)

with column1:
    subcolumn1_1, subcolumn2_1 = st.columns(2) # the underscore 1 is to signify the left main column

    if subcolumn1_1.button('GIS', key = 'gis_button_1'):
        st.session_state.gis_filter_1 = True
        st.session_state.historical_filter_1 = False 
    
    if subcolumn2_1.button('Historical', key = 'hist_button_1'):
        st.session_state.historical_filter_1 = True
        st.session_state.gis_filter_1 = False
    
    if st.session_state.gis_filter_1:
        layer_list = [item for item in data_dictionary.keys() if 'gis' in data_dictionary[item]]
        chosen = st.selectbox('Select a layer', layer_list, key = 'gis_list_1')
        st.write(f"WE WILL PLOT A MAP OF {chosen} HERE")
    
    elif st.session_state.historical_filter_1:
        layer_list = [item for item in data_dictionary.keys() if 'historical' in data_dictionary[item]]
        chosen = st.selectbox('Select a layer', layer_list, key = 'hist_list_1')
        st.write(f"WE WILL PLOT A GRAPH OF {chosen} HERE")




##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################


with column2:
    subcolumn1_2, subcolumn2_2 = st.columns(2) # the underscore 2 is to signify the left main column

    if subcolumn1_2.button('GIS', key = 'gis_button_2'):
        st.session_state.gis_filter_2 = True
        st.session_state.historical_filter_2 = False 
    
    if subcolumn2_2.button('Historical', key = 'hist_button_2'):
        st.session_state.historical_filter_2 = True
        st.session_state.gis_filter_2 = False
    
    if st.session_state.gis_filter_2:
        layer_list = [item for item in data_dictionary.keys() if 'gis' in data_dictionary[item]]
        chosen = st.selectbox('Select a layer', layer_list, key = 'gis_list_2')
        st.write(f"WE WILL PLOT A MAP OF {chosen} HERE")
    
    elif st.session_state.historical_filter_2:
        layer_list = [item for item in data_dictionary.keys() if 'historical' in data_dictionary[item]]
        chosen = st.selectbox('Select a layer', layer_list, key = 'hist_list_2')
        st.write(f"WE WILL PLOT A GRAPH OF {chosen} HERE")