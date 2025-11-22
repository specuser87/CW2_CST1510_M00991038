import streamlit as st  
from database import DatabaseManager

st.set_page_config(page_title="Login", page_icon="🔐", layout="Centered")

# initializing the database if it does not exist.
if 'db' not in st.session_state:
    st.session_state.db = DatabaseManager()


# initializing the login state

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None

st.title("🔐User Authentication")

# checking if the user is already logged in
if st.session_state.logged_in:
    st.success(f"You are already logged in as **{st.session_state.username}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button (" Go to Home", use_container_width= True):
            st.swtich_page("app.py")
    with col2:
        if st.button (" Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            st.rerun()

    st.stop()

#creating the tabs for login and register

tab1, tab2 = st.tabs([" Login", " Register"])
