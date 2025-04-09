import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from streamlit.components.v1 import html
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages

# Function to switch pages programmatically
def switch_page(page_name: str):
    from streamlit.runtime.scriptrunner import RerunData, RerunException
    from streamlit.source_util import get_pages
    
    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")
    
    page_name = standardize_name(page_name)
    
    pages = get_pages("streamlit_app.py")
    
    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )
    
    page_names = [standardize_name(config["page_name"]) for config in pages.values()]
    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")

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

# Create tabs with click handlers using session state
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'intro'

# Function to handle tab navigation
def navigate_to(tab):
    st.session_state.active_tab = tab
    # Use st.rerun to reload the app with the new state
    st.rerun()

# Top navigation tabs - matching the blue tab design in the image
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("Defining\nAtlanta", key="tab_intro", use_container_width=True, 
                 help="Navigate to Defining Atlanta", type="primary"):
        navigate_to('intro')

with col2:
    if st.button("Energy\nEfficiency", key="tab_energy", use_container_width=True, 
                 help="Navigate to Energy Efficiency"):
        navigate_to('energy_efficiency')

with col3:
    if st.button("Data Centers\n& EVs", key="tab_data", use_container_width=True, 
                 help="Navigate to Data Centers & EVs"):
        navigate_to('data_centers')

with col4:
    if st.button("Our Energy\nGrid", key="tab_grid", use_container_width=True, 
                 help="Navigate to Our Energy Grid"):
        navigate_to('energy_grid')

with col5:
    if st.button("Looking to\nour Future", key="tab_future", use_container_width=True, 
                 help="Navigate to Looking to our Future"):
        navigate_to('future')

# Check if we need to redirect
if st.session_state.active_tab != 'intro':
    switch_page(st.session_state.active_tab)


# Main content section with two columns
st.markdown('<div class="main-container">', unsafe_allow_html=True)
col_left, col_right = st.columns([1, 2])

with col_left:
    # Left column with DEFINING ATLANTA
    st.markdown('<div class="heading-section">DEFINING<br>ATLANTA</div>', unsafe_allow_html=True)

    st.markdown(
        '''
        <div class="content-text">
            Atlanta is a major urban center experiencing significant growth, with over 1.1 million residents in Fulton County alone and expanding rapidly throughout the metro area. As the capital of Georgia and a regional transportation hub, the city has evolved into a consumer-heavy metropolis with increasing energy demands. Our urban landscape, shaped by unique topography and development patterns, creates specific challenges and opportunities for our energy infrastructure as we plan for sustainable growth in the coming decades.
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
            Atlanta\'s energy landscape is transforming rapidly with the rise of electric vehicles and data centers creating unprecedented demand. Traditionally, our power has been delivered from distant generation plants through long transmission lines, suffering 5% transmission losses and an additional 10% in distribution losses. New technologies are enabling a shift toward more localized generation and smart consumption patterns. This evolution means that for every 100 units of energy we use, generation plants currently must produce around 115 units to compensate for system inefficiencies.
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="sub-heading-section">Looking Forward</div>', unsafe_allow_html=True)
    
    st.markdown(
        '''
        <div class="content-text">
            The future of Atlanta\'s energy grid depends on developing load flexibility and energy storage capabilities. Local power generation through solar installations, microgrids, and community energy projects can significantly reduce transmission losses while increasing resilience. Modern demand response systems allow consumers to adjust their energy use during peak times, creating a more efficient and responsive grid. By reimagining our energy infrastructure from centralized to distributed, we can build a more sustainable, adaptable system capable of meeting the challenges of climate change and urban growth.
        </div>
        ''',
        unsafe_allow_html=True
    )

# Footer
st.markdown('</div>', unsafe_allow_html=True)
st.divider()