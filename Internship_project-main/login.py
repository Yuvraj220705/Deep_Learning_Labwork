import streamlit as st 
import signup as sg
import time

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
if "username" not in st.session_state:
    st.session_state.username = None

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    
def authenticate(username, password):
    users = sg.load_user()

    # normalize input
    username = str(username).strip()
    password = str(password).strip()

    # 🔑 force dataframe columns to string
    users["username"] = users["username"].astype(str).str.strip()
    users["password"] = users["password"].astype(str).str.strip()

    user = users[
        (users["username"] == username) &
        (users["password"] == password)
    ]

    if not user.empty:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.gender = user.iloc[0]["gender"]
        return True

    return False


  
def login_page():
    # Enhanced CSS for login page - FIXED ALL WHITE SPACES
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        /* Background */
        .stApp {
            background: linear-gradient(135deg, #0f2027 0%, #203a43 25%, #2c5364 50%, #1a365d 75%, #0f172a 100%) !important;
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        
        /* FIX ALL WHITE SPACES */
        [data-testid="stAppViewContainer"] {
            background: transparent !important;
        }
        
        [data-testid="stHeader"] {
            background: linear-gradient(135deg, #0f2027 0%, #203a43 100%) !important;
        }
        
        [data-testid="stToolbar"] {
            background: linear-gradient(135deg, #0f2027 0%, #203a43 100%) !important;
        }
        
        [data-testid="collapsedControl"] {
            background: linear-gradient(135deg, #0f2027 0%, #203a43 100%) !important;
        }
        
        [data-testid="stDecoration"] {
            background: linear-gradient(135deg, #0f2027 0%, #203a43 100%) !important;
        }
        
        .main .block-container {
            background: transparent !important;
        }
        
        .main > div:first-child {
            background: transparent !important;
            padding-top: 10px;
        }
        
        .main > div:last-child {
            background: transparent !important;
            padding-bottom: 10px;
        }
        
        [data-testid="stVerticalBlock"] {
            background: transparent !important;
        }
        
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: transparent !important;
        }
        
        [data-testid="stHorizontalBlock"] {
            background: transparent !important;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Login container */
        .login-container {
            max-width: 450px;
            margin: 0 auto;
            padding: 40px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            animation: fadeInUp 0.8s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Header */
        .login-header {
            text-align: center;
            margin-bottom: 35px;
            animation: fadeInDown 0.8s ease-out;
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .login-header h1 {
            color: white;
            font-size: 40px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .login-header p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 16px;
        }
        
        /* Input fields */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.2) !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 15px !important;
            color: black !important;
            padding: 15px 20px !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: rgba(255, 255, 255, 0.6) !important;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.3) !important;
            background: rgba(255, 255, 255, 0.25) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: rgb(49, 51, 63) !important;
        }
        
        /* Labels */
        .stTextInput > label {
            color: white !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            margin-bottom: 8px !important;
        }
        
        /* MATCHING PILL-SHAPED BUTTONS FOR LOGIN PAGE */
        .stButton > button {
            width: 100% !important;
            height: 45px !important;
            border-radius: 25px !important; /* Pill shape */
            font-size: 16px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }

        /* Primary Login Button */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 4px 15px 0 rgba(116, 79, 168, 0.4) !important;
        }

        /* Secondary Buttons (Create Account / Back to Home) */
        .stButton > button:not([kind="primary"]) {
            background: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
        }

        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 6px 20px 0 rgba(116, 79, 168, 0.6) !important;
        }
        
        /* Alert messages */
        .stAlert {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        /* Divider */
        .divider {
            text-align: center;
            margin: 25px 0;
            color: rgba(255, 255, 255, 0.7);
            font-size: 14px;
        }
        
        /* Lock icon animation */
        @keyframes shake {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(-10deg); }
            75% { transform: rotate(10deg); }
        }
        
        .icon-shake {
            display: inline-block;
            animation: shake 2s ease-in-out infinite;
        }
        
        /* Glow effect */
        @keyframes glow {
            0%, 100% { text-shadow: 0 0 10px rgba(255, 255, 255, 0.5); }
            50% { text-shadow: 0 0 20px rgba(255, 255, 255, 0.8); }
        }
        
        .glow-text {
            animation: glow 2s ease-in-out infinite;
        }
        
        </style>
    """, unsafe_allow_html=True)
    
    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div class="login-header">
                <div class="icon-shake">🔐</div>
                <h1 class="glow-text">Welcome Back</h1>
                <p>Login to continue your journey with Ruby AI</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login-form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            login_btn = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
            
            if login_btn:
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("✅ Login successful! Redirecting...")
                    time.sleep(1.5)
                    st.session_state.page = "AuthenticatedUserHome" 
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
        
        # Divider
        st.markdown('<div class="divider">Don\'t have an account?</div>', unsafe_allow_html=True)
        
        # Signup button
        if st.button("✨ Create New Account", use_container_width=True):
            st.session_state.page = "Signup"
            st.rerun()
        
        # Back to home
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.page = "Unauthenticated_User_Home"
            st.rerun()