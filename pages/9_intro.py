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

# Create navigation with direct links using markdown
st.markdown(
    '''
    <style>
    .nav-button {
        background-color: #F0F2F6;
        border: none;
        color: #0A3E5A;
        padding: 10px 15px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
        width: 100%;
        white-space: pre-wrap;
        font-weight: bold;
    }
    .nav-button.active {
        background-color: #FF4B4B;
        color: white;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        f'''
        <a href="/intro" target="_self">
            <button class="nav-button active">Defining<br>Atlanta</button>
        </a>
        ''',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'''
        <a href="/energy_efficiency" target="_self">
            <button class="nav-button">Energy<br>Efficiency</button>
        </a>
        ''',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'''
        <a href="#" target="_self">
            <button class="nav-button">Data Centers<br>& EVs</button>
        </a>
        ''',
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f'''
        <a href="#" target="_self">
            <button class="nav-button">Our Energy<br>Grid</button>
        </a>
        ''',
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f'''
        <a href="#" target="_self">
            <button class="nav-button">Looking to<br>our Future</button>
        </a>
        ''',
        unsafe_allow_html=True
    )


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