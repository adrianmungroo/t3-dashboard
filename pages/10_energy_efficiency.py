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
        font-size: 28px;
        font-weight: bold;
        margin-top: 0px;
        margin-bottom: 15px;
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
    .see-how-text {
        color: #0A3E5A;
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 10px;
        text-align: right;
    }
    .learn-more-container {
        display: flex;
        align-items: center;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .learn-more-button {
        background-color: #B8E2FA;
        color: #0A3E5A;
        padding: 8px 15px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
    }
    .arrow-icon {
        color: #B8E2FA;
        font-size: 24px;
        margin-left: 5px;
    }
    .main-container {
        padding: 0 20px;
    }
    .learn-more-button {
        background-color: #4BB4DE;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-align: center;
        display: inline-block;
        margin-top: 10px;
        text-decoration: none;
        font-weight: bold;
    }
    .learn-more-container {
        display: flex;
        align-items: center;
    }
    .arrow-icon {
        color: #4BB4DE;
        font-size: 24px;
        margin-left: 10px;
    }
    .see-how-text {
        color: #0A3E5A;
        font-weight: bold;
        text-align: right;
        font-size: 14px;
        margin-bottom: 5px;
    }
    .expand-icon {
        color: #0A3E5A;
        font-size: 24px;
        text-align: right;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Navigation function to handle page transitions
def nav_to(url):
    nav_script = f"""
        <script>
        window.location.href = '{url}'
        </script>
    """
    st.markdown(nav_script, unsafe_allow_html=True)

# Create tabs with click handlers using session state
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'energy_efficiency'

# Function to handle tab navigation
def navigate_to(tab):
    st.session_state.active_tab = tab
    # Use st.rerun to reload the app with the new state
    st.rerun()

# Top navigation tabs - matching the blue tab design in the image
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("Defining\nAtlanta", key="tab_intro", use_container_width=True, 
                 help="Navigate to Defining Atlanta"):
        navigate_to('intro')

with col2:
    if st.button("Energy\nEfficiency", key="tab_energy", use_container_width=True, 
                 help="Navigate to Energy Efficiency", type="primary"):
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
if st.session_state.active_tab != 'energy_efficiency':
    switch_page(st.session_state.active_tab)


# Main content section with a left sidebar and main content area
st.markdown('<div class="main-container">', unsafe_allow_html=True)
col_left, col_main = st.columns([1, 3])

with col_left:
    # Left column with ENERGY EFFICIENCY
    st.markdown('<div class="heading-section">Energy<br>Efficiency</div>', unsafe_allow_html=True)

    st.markdown(
        '''
        <div class="content-text">
            Energy efficiency refers to using less energy to perform the same task or deliver the same service. Improved efficiency reduces energy waste, lowers utility bills, and decreases overall environmental impact in Atlanta's growing urban landscape.
        </div>
        ''',
        unsafe_allow_html=True
    )

with col_main:
    # Main content area with the heat pumps and housing envelope sections
    
    # Create two rows for the content sections
    # First row - Heat Pumps
    st.markdown('<div style="margin-bottom: 40px;">', unsafe_allow_html=True)
    row1_col1, row1_col2 = st.columns([2, 1])

    with row1_col1:
        st.markdown('<div class="sub-heading-section">What are Heat Pumps?</div>', unsafe_allow_html=True)
        
        st.markdown(
            '''
            <div class="content-text">
                Heat pumps are highly efficient devices that transfer heat instead of generating it through combustion. Unlike traditional heating systems that burn fuel, heat pumps move heat from one place to another, making them up to 300% more efficient than conventional heating methods. Modern heat pumps work effectively even in colder southern winters, contrary to outdated perceptions. When paired with proper home insulation, they can dramatically reduce energy consumption while maintaining comfort year-round.
            </div>
            ''',
            unsafe_allow_html=True
        )
        
        # Learn More button with arrow
        st.markdown(
            '''
            <div class="learn-more-container">
                <a href="#" class="learn-more-button">Click to Learn More</a>
                <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/arrow-right.svg" width="30" height="20" style="filter: invert(73%) sepia(95%) saturate(334%) hue-rotate(182deg) brightness(97%) contrast(96%);">
            </div>
            ''',
            unsafe_allow_html=True
        )

    with row1_col2:
        st.markdown('<div class="see-how-text">See how Heat Pumps affect Energy use!</div>', unsafe_allow_html=True)
        
        # Placeholder for heat pump image with expand/collapse arrows
        st.image("https://via.placeholder.com/400x300/0A3E5A/FFFFFF?text=Heat+Pump+Diagram")
        
        # Add expand/collapse arrows
        st.markdown(
            '''
            <div style="text-align: right; margin-top: -30px;">
                <span style="font-size: 24px; color: #0A3E5A;">⤢</span>
            </div>
            ''',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Second row - Housing Envelope
    st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
    row2_col1, row2_col2 = st.columns([2, 1])

    with row2_col1:
        st.markdown('<div class="sub-heading-section">What do we mean by Housing Envelope?</div>', unsafe_allow_html=True)
        
        st.markdown(
            '''
            <div class="content-text">
                A home's envelope consists of all exterior components that separate conditioned indoor areas from the outdoors—including walls, windows, doors, roof, and foundation. A well-designed envelope minimizes unwanted heat transfer and air leakage. In Atlanta's climate, proper insulation and air sealing can reduce heating and cooling needs by up to 20%. Improvements to your home's envelope often provide the best return on investment among energy efficiency upgrades, especially in older homes common throughout our region.
            </div>
            ''',
            unsafe_allow_html=True
        )
        
        # Learn More button with arrow
        st.markdown(
            '''
            <div class="learn-more-container">
                <a href="#" class="learn-more-button">Click to Learn More</a>
                <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/arrow-right.svg" width="30" height="20" style="filter: invert(73%) sepia(95%) saturate(334%) hue-rotate(182deg) brightness(97%) contrast(96%);">
            </div>
            ''',
            unsafe_allow_html=True
        )

    with row2_col2:
        st.markdown('<div class="see-how-text">See how...</div>', unsafe_allow_html=True)
        
        # Placeholder for housing envelope image with expand/collapse arrows
        st.image("https://via.placeholder.com/400x300/0A3E5A/FFFFFF?text=Housing+Envelope+Diagram")
        
        # Add expand/collapse arrows
        st.markdown(
            '''
            <div style="text-align: right; margin-top: -30px;">
                <span style="font-size: 24px; color: #0A3E5A;">⤢</span>
            </div>
            ''',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('</div>', unsafe_allow_html=True)
st.divider()