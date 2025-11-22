"""
Week 9: Multi-Domain Intelligence Platform
Main Streamlit Application Entry Point
"""

import streamlit as st
from database import Database Manager

#The stage of Page configuration
st.set_page_config(
    page_title="Intelligence Platform",
    page_icon= "🔒"
    layout="wide"
    initial_sidebar_state="expanded"
)

#Initializing the datbase connection in the session.

if 'db' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None


#content of the main page
st.title("Multi-Domain Intelligence Platform")
st.markdown("---")

if not st.session_state.logged_in:
    st.info("Please login using the sidebar to access the platform")

    st.markdown("""
    ### Welcome to the Intelligence Platform
    
    This platform provides:
    - **Cybersecurity Dashboard** - Monitors and analyze's security incidents
    - **Data Science Dashboard** - Manage datasets and analyze data quality
    - **IT Operations Dashboard** - Track and resolve IT tickets
    
    **Please use the login page in the sidebar to get started.**
    """)

else:
    st.success(f"logged in as **{st.session_state.username}** ({st.session_state.role})")

    st.markdown("""
    ### Quick Start Guide
    
    1. **Navigate** to your domain dashboard using the sidebar
    2. **View** real-time data and analytics
    3. **Manage** records using CRUD oeprations
    4. **Analyze** insights with interactive visualizations
    
     Select a dashboard from the sidebar to begin.
     """)

#Statistics - pulling from the database

stats = st.session_state.db.get_table_stats()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Users", stats ['users'])
with col2:
    st.metric("Cyber Incidents", stats['cyber_incidents'])
with col3:
    st.metric("Datasets", stats ['datasets_metadata'])
with col4:
    st.metric("IT Tickets", stats ['it_tickerts'])


# footer the end of the page/web
st.markdown("---")
st.caption("CST1510 - Multi-Domain Intelligence Platform | Week 9")