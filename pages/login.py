import streamlit as st  
from database import DatabaseManager

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

# initializing the database if it does not exist.
if 'db' not in st.session_state:
    st.session_state.db = DatabaseManager()


# initializing the login state

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None

st.title("User Authentication")

# checking if the user is already logged in
if st.session_state.logged_in:
    st.success(f"You are already logged in as **{st.session_state.username}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button (" Go to Home", use_container_width= True):
            st.switch_page("app.py")
    with col2:
        if st.button (" Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            st.rerun()

    st.stop()

#creating the tabs for login and register

tab1, tab2 = st.tabs(["Login", "Register"])

# ========================== LOGIN TAB ==========================
with tab1:
    st.subheader("Login to your Account")

    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("username",placeholder="Enter your username") 
        password = st.text_input("password", type="password", placeholder="Enter your password")

        submitted = st.form_submit_button(" Login", use_container_width=True)

        if submitted:
            if not username or not password:
             st.error(" Please enter both username and password")
        else:
            # to verify the credentials
            if st.session_state.db.verify_user_password(username, password):
                #getting the users details
                user = st.session_state.db.get_user_by_username(username)

                #setting the session state

                st.session_state.logged_in = True
                st.session_state.username = user [1] #username
                st.session_state.role = user [3] # role

                st.success(f" Login successful! Welcome, {username}!")
                st.toast("Logged in Successfully")

                # A delay before redirecting

                import time
                time.sleep(1)
                st.rerun()

            else:
                st.error(" Invalid username or password")


# ================================= Tab where the user registers ================================= 

with tab2:
   st.subheader("Create New Account")     

   with st.form ("register_form", clear_on_submit=True):  
       new_username = st.text_input("Username", placeholder="Enter your Username")  
       new_password = st.text_input("Password", type="password", placeholder="Choose a password")
       confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")   
       role = st.selectbox("Role", ["user", "analyst", "admin"])

       submitted = st.form_submit_button(" Register", use_container_width=True)

       if submitted:
           #This section is to validate
           if not new_username or not new_password:
               st.error(" Please fill in all fields")
           elif new_password != confirm_password:
               st.error(" Password do not match")
           elif len(new_password) < 6:
               st.error(" Password must be at least 6 characters")
           else:
               #checking if the user exists
               existing_user = st.session_state.db.get_user_by_username(new_username)
               if existing_user:
                   st.error(f" Username '{new_username}' already exists")
               else:
                   #creating the user user if they dont exist
                   if st.session_state.db.create_user(new_username, new_password, role):
                       st.success(f" Account created successfully! You can now login.")
                   else:
                       st.error(" Registration failed. Please try again. ")

st.markdown("---")
st.info("""
**Demo Credentials:**
- Username: `alice` / Password: (check your users.txt from Week 7)
- Or register a new account above
""")

         