import streamlit as st
from streamlit_folium import st_folium, folium_static
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium import plugins
from streamlit_folium import st_folium
import matplotlib.colors as mcolors
import plotly.express as px
from branca.colormap import LinearColormap

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
 'tracts': ['DAC Boolean','Energy Burden 2022 Tract']},
 'Historical' : ['State Level Jobs', 'GA_AnnualEmissions', 'AQI Scores Fulton']}

# Data category to color mapping
data_colors = {
    'Energy Burden': 'Reds',
    'Solar': 'YlOrBr',
    'Coal': 'Greys',
    'Natural Gas': 'Blues',
    'Median AQI': 'RdYlGn_r',  # Reversed so red=bad air quality
    'DAC Boolean': 'Set1'
}

# Session state for synced colorbars
if 'sync_colorbars' not in st.session_state:
    st.session_state.sync_colorbars = False

if 'global_min_max' not in st.session_state:
    st.session_state.global_min_max = {}

# Helper Functions

def get_appropriate_colormap(column_name):
    for key in data_colors.keys():
        if key in column_name:
            return data_colors[key]
    return 'Reds'  # Default

def get_data_category(column_name):
    for key in data_colors.keys():
        if key in column_name:
            return key
    return None

def get_color(value, min_value, max_value, color_scale):
    if value is None or pd.isna(value):
        return '#CCCCCC'  # Gray for missing data
    normalized = (value - min_value) / (max_value - min_value) if max_value > min_value else 0.5
    cmap = plt.get_cmap(color_scale)
    color = mcolors.to_hex(cmap(normalized))
    return color

def plotGISGraph(chosen, subgroup, key_suffix):
    data = gpd.read_file(f'data/GIS/{subgroup}.geojson')
    data_json = data.to_json()
    column_choice = chosen
    
    # Store data info for potential sync
    data_category = get_data_category(column_choice)
    if data_category:
        if data_category not in st.session_state.global_min_max:
            st.session_state.global_min_max[data_category] = {'min': float('inf'), 'max': float('-inf')}
        
        current_min = data[column_choice].min()
        current_max = data[column_choice].max()
        
        # Update global min/max for this data category
        st.session_state.global_min_max[data_category]['min'] = min(st.session_state.global_min_max[data_category]['min'], current_min)
        st.session_state.global_min_max[data_category]['max'] = max(st.session_state.global_min_max[data_category]['max'], current_max)
    
    # Create tile layers
    tiles = {
        'OpenStreetMap': folium.TileLayer(
            tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            name='OpenStreetMap'
        ),
        'ESRI Satellite': folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='ESRI Satellite'
        ),
        'CartoDB Positron': folium.TileLayer(
            tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            name='CartoDB Positron'
        ),
    }
    
    # Create map
    m = folium.Map(
        location=[32.9, -82], 
        zoom_start=7,
        tiles=None
    )
    
    # Add all tile layers to the map
    for tile in tiles.values():
        tile.add_to(m)
    
    if column_choice:
        # Handle boolean columns differently
        if column_choice == 'DAC Boolean':
            colormap = get_appropriate_colormap(column_choice)
            
            def style_function(feature):
                value = feature['properties'][column_choice]
                color = '#FF0000' if value else '#00FF00'  # Red for True, Green for False
                return {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                }
            
            legend_colors = {'Yes': '#FF0000', 'No': '#00FF00'}
            
        else:
            # For numeric columns
            colormap = get_appropriate_colormap(column_choice)
            
            # Determine if we should use synced min/max values
            if st.session_state.sync_colorbars and data_category and data_category in st.session_state.global_min_max:
                min_value = st.session_state.global_min_max[data_category]['min']
                max_value = st.session_state.global_min_max[data_category]['max']
            else:
                min_value = data[column_choice].min()
                max_value = data[column_choice].max()
            
            def style_function(feature):
                value = feature['properties'][column_choice]
                color = get_color(value, min_value, max_value, colormap)
                return {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                }
            
            # Convert matplotlib colormap to hex colors that branca can use
            colormap_instance = plt.get_cmap(colormap)
            color_values = np.linspace(0, 1, 10)
            hex_colors = [mcolors.to_hex(colormap_instance(i)) for i in color_values]
            
            # Create a colormap for the legend
            colormap_obj = LinearColormap(
                colors=hex_colors,
                index=np.linspace(min_value, max_value, 10),
                vmin=min_value,
                vmax=max_value,
                caption=column_choice
            )
            
            # Add the colormap to the map
            colormap_obj.add_to(m)
        
        # Create GeoJson layer with tooltips
        tooltip_fields = ['name'] if subgroup == 'counties' else ['AFFGEOID']
        tooltip_aliases = ['County'] if subgroup == 'counties' else ['Tract ID']
        
        # Add column choice to tooltip
        tooltip_fields.append(column_choice)
        tooltip_aliases.append(column_choice)
        
        folium.GeoJson(
            data_json,
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(
                fields=tooltip_fields,
                aliases=tooltip_aliases,
                sticky=True,
                localize=True,
                style='''
                    background-color: #F0EFEF;
                    border: 2px solid black;
                    border-radius: 3px;
                    box-shadow: 3px 3px 3px rgba(0,0,0,0.2);
                    padding: 10px;
                    font-size: 14px;
                '''
            ),
            name=f'{column_choice}'
        ).add_to(m)
        
        # Add special legend for boolean data
        if column_choice == 'DAC Boolean':
            legend_html = '''
            <div style="
                position: fixed; 
                bottom: 50px; right: 50px; 
                background-color: white; 
                padding: 10px; 
                border: 2px solid grey;
                border-radius: 5px;
                z-index: 9999;
                ">
                <p><b>{title}</b></p>
                <p><span style="color:{color1};">■</span> Yes</p>
                <p><span style="color:{color2};">■</span> No</p>
            </div>
            '''.format(title=column_choice, color1='#FF0000', color2='#00FF00')
            
            m.get_root().html.add_child(folium.Element(legend_html))
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add scale bar
    folium.plugins.MeasureControl(position='bottomleft').add_to(m)
    
    # Display the map
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

# Sync Colorbars button - only show when both panels have maps
sync_needed = st.session_state.gis_filter_1 and st.session_state.gis_filter_2

if sync_needed:
    sync_col1, sync_col2, sync_col3 = st.columns([4, 1, 4])
    with sync_col2:
        if st.button('🔄 Sync Colorbars', key='sync_colorbars_button'):
            st.session_state.sync_colorbars = not st.session_state.sync_colorbars
            st.rerun()
    
    sync_status = "ON ✅" if st.session_state.sync_colorbars else "OFF ❌"
    sync_col2.write(f"Sync: {sync_status}")

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
        chosen = st.selectbox('Click to select a dataset below', sorted(layer_list), key = 'gis_list_1', index=5)

        if chosen in column_dictionary['GIS']['counties']:
            subgroup = 'counties'
        elif chosen in column_dictionary['GIS']['tracts']:
            subgroup = 'tracts'

        plotGISGraph(chosen, subgroup, 1)

    elif st.session_state.historical_filter_1:
        layer_list = column_dictionary['Historical']
        chosen = st.selectbox('Click to select a dataset below', sorted(layer_list), key = 'hist_list_1')

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
        chosen = st.selectbox('Click to select a dataset below', sorted(layer_list), key = 'gis_list_2')

        if chosen in column_dictionary['GIS']['counties']:
            subgroup = 'counties'
        elif chosen in column_dictionary['GIS']['tracts']:
            subgroup = 'tracts'

        plotGISGraph(chosen, subgroup, 2)
    
    elif st.session_state.historical_filter_2:
        layer_list = column_dictionary['Historical']
        chosen = st.selectbox('Click to select a dataset below', sorted(layer_list), key = 'hist_list_2', index=2)

        plotHistoricalGraph(chosen, 2)

st.divider()
st.caption(APP_SUBTITLE)