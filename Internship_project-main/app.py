import streamlit as st 
import pandas as pd
import os
from dotenv import load_dotenv
import UnauthenticatedUserHome as unh
import signup as sg # from signup import signup_page
import login as log
import AuthenticatedUserHome as ah

# load_dotenv()

st.set_page_config(page_title="Home page", page_icon="", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Unauthenticated_User_Home"


if st.session_state.page == "Unauthenticated_User_Home":
    unh.unauthenticated_user_home_page()
elif st.session_state.page == "Login":
    log.login_page()            
elif st.session_state.page == "Signup":
    sg.signup_page()  
else:
    ah.authenticated_user_home_page()
    
    




