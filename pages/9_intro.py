import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from streamlit.components.v1 import html

APP_TITLE = "Atlanta Energy Transition"
APP_SUBTITLE = "Energy Transformation Initiatives"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏙️",
    layout='wide'
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .tab-container {
        display: flex;
        width: 100%;
        margin-bottom: 20px;
    }
    .tab-section {
        background-color: #B8E2FA;
        padding: 15px 10px;
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        color: #0A3E5A;
        flex: 1;
        border-right: 1px solid white;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .tab-section:last-child {
        border-right: none;
    }
    .tab-section.active {
        background-color: #0A3E5A;
        color: white;
    }
    .heading-section {
        color: #0A3E5A;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 20px;
        font-family: sans-serif;
    }
    .sub-heading-section {
        color: #0A3E5A;
        font-size: 42px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 20px;
        font-family: sans-serif;
    }
    .content-text {
        font-size: 16px;
        color: #333333;
        font-style: italic;
        line-height: 1.5;
    }
    .content-text a {
        color: #0A3E5A;
        text-decoration: underline;
    }
    .main-container {
        padding: 0 20px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'intro'

# Function to navigate between pages without full reload
def navigate_to(page):
    # Set the page in session state
    st.session_state.page = page
    # Use st.query_params to update URL without reload
    st.query_params.page = page
    # Rerun the app to reflect the change
    st.rerun()

# Check URL parameters for direct navigation
if 'page' in st.query_params:
    if st.query_params.page != st.session_state.page:
        st.session_state.page = st.query_params.page

# Create navigation with buttons
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("Defining\nAtlanta", key="tab_intro", use_container_width=True, 
                 help="Navigate to Defining Atlanta", 
                 type="primary" if st.session_state.page == 'intro' else "secondary"):
        navigate_to('intro')

with col2:
    if st.button("Energy\nEfficiency", key="tab_energy", use_container_width=True, 
                 help="Navigate to Energy Efficiency",
                 type="primary" if st.session_state.page == 'energy_efficiency' else "secondary"):
        navigate_to('energy_efficiency')

with col3:
    if st.button("Data Centers\n& EVs", key="tab_data", use_container_width=True, 
                 help="Navigate to Data Centers & EVs",
                 type="primary" if st.session_state.page == 'data_centers' else "secondary"):
        navigate_to('data_centers')

with col4:
    if st.button("Our Energy\nGrid", key="tab_grid", use_container_width=True, 
                 help="Navigate to Our Energy Grid",
                 type="primary" if st.session_state.page == 'energy_grid' else "secondary"):
        navigate_to('energy_grid')

with col5:
    if st.button("Looking to\nour Future", key="tab_future", use_container_width=True, 
                 help="Navigate to Looking to our Future",
                 type="primary" if st.session_state.page == 'future' else "secondary"):
        navigate_to('future')

# Handle navigation based on session state
if st.session_state.page != 'intro':
    # Map page names to their file paths
    page_mapping = {
        'energy_efficiency': '10_energy_efficiency.py',
        'data_centers': '11_data_centers.py',  # Assuming this is the correct filename
        'energy_grid': '12_energy_grid.py',    # Assuming this is the correct filename
        'future': '13_future.py'              # Assuming this is the correct filename
    }
    
    # Navigate to the selected page
    if st.session_state.page in page_mapping:
        st.switch_page(f"pages/{page_mapping[st.session_state.page]}")


# Main content section with two columns
st.markdown('<div class="main-container">', unsafe_allow_html=True)
col_left, col_right = st.columns([1, 2])

with col_left:
    # Left column with DEFINING ATLANTA
    st.markdown('<div class="heading-section">DEFINING<br>ATLANTA</div>', unsafe_allow_html=True)

    st.markdown(
        '''
        <div class="content-text">
            The capital of Georgia and centerpiece of a metropolitan area exceeding 6 million residents, Atlanta represents a critical energy ecosystem with distinctive characteristics shaped by its climate, geography, and economic profile. With hot, humid summers driving substantial cooling demands and a dispersed urban footprint requiring extensive transportation networks, Atlanta's energy consumption patterns present unique challenges and opportunities for innovation.
        </div>
        ''',
        unsafe_allow_html=True
    )

with col_right:
    # Right column with How it's changing and Looking Forward
    st.markdown('<div class="sub-heading-section">How it\'s changing</div>', unsafe_allow_html=True)
    
    st.markdown(
        '''
        <div class="content-text">
            Our city stands at a pivotal moment in its energy evolution. The traditional reliance on fossil fuel generation is giving way to a more diverse and sustainable mix of energy sources. Local policies supporting clean energy adoption, growing corporate sustainability commitments from Atlanta's major businesses, and increasing consumer interest in energy-efficient technologies are collectively driving this transition. From solar installations on commercial properties to community solar programs in historically underserved neighborhoods, energy innovation is spreading across the metro area.
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="sub-heading-section">Looking Forward</div>', unsafe_allow_html=True)
    
    st.markdown(
        '''
        <div class="content-text">
            This tool allows users to explore how different energy strategies—from building retrofits to distributed solar deployment to grid modernization—can impact Atlanta's energy future. By providing data-driven analysis of various scenarios, we aim to empower policymakers, businesses, community organizations, and residents to make informed decisions that enhance energy affordability, improve resilience, reduce environmental impacts, and ensure equitable access to clean energy benefits throughout the Atlanta region.
        </div>
        ''',
        unsafe_allow_html=True
    )

# Footer
st.markdown('</div>', unsafe_allow_html=True)
st.divider()