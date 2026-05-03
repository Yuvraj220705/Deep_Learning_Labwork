import streamlit as st 
import os
from dotenv import load_dotenv
import time
from langchain.chat_models import init_chat_model


def bot_reply(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.25)
        
def unauthenticated_user_home_page():
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    
    # Enhanced CSS with animations and modern design - FIXED ALL WHITE SPACES
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        /* Main container background with gradient */
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
        
        /* Header styling with glassmorphism */
        .main-header {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px 30px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
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
        
        /* Button styling */
        div.stButton > button {
            width: 120px;
            height: 45px;
            font-size: 16px;
            font-weight: 600;
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            box-shadow: 0 4px 15px 0 rgba(116, 79, 168, 0.4);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        div.stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px 0 rgba(116, 79, 168, 0.6);
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }
        
        div.stButton > button:active {
            transform: translateY(-1px);
        }
        
        /* Chat message styling */
        .stChatMessage {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 15px;
            margin: 10px 0;
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
        
        /* Chat input styling */
        .stChatInputContainer {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 25px;
            padding: 10px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
        }
        
        .stChatInputContainer:focus-within {
            border-color: rgba(255, 255, 255, 0.6);
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
        }
        
        /* Title styling */
        h1, h2, h3 {
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        /* Spinner styling */
        .stSpinner > div {
            border-color: rgba(255, 255, 255, 0.3) !important;
            border-top-color: white !important;
        }
        
        /* Welcome message styling */
        .welcome-card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            animation: fadeIn 1s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .welcome-card h2 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .welcome-card p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 16px;
            line-height: 1.6;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }
        /* Forces all text within chat bubbles to be white */
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] p {
            color: white !important;
            -webkit-text-fill-color: white !important; /* Forces color on some browsers */
        }

        /* Specifically target User prompts if they are still stubborn */
        [data-testid="stChatMessageAvatarUser"] + div p {
            color: white !important;
        }

        /* Specifically target Assistant prompts if they are still stubborn */
        [data-testid="stChatMessageAvatarAssistant"] + div p {
            color: white !important;
        }

        /* Fix for the chat input text while typing */
        .stChatInput textarea {
            color: white !important;
            -webkit-text-fill-color: white !important;
        }    

        /* 1. Make the text INSIDE the chat bubbles WHITE */
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] p {
            color: white !important;
        }

        /* 2. Make the text INSIDE the chat input box DARK (visible) */
        /* This targets the actual input area where you type */
        .stChatInput textarea {
            color: #31333F !important; /* Dark grey/black */
            -webkit-text-fill-color: #31333F !important;
        }

        /* 3. Ensure the placeholder text is also visible */
        .stChatInput textarea::placeholder {
            color: rgba(49, 51, 63, 0.5) !important;
        }            
        </style>
    """, unsafe_allow_html=True)
    
    # Header with glassmorphism effect
    col1, col2, col3 = st.columns([6, 1, 1])

    with col1:
        # st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown("# 💎 Ruby AI Assistant")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        if st.button("🔐 Login"):
            st.session_state.page = "Login"
            st.rerun()
                
    with col3:
        if st.button("✨ Signup"):
            st.session_state.page = "Signup"
            st.rerun()
    
    # Welcome card if no conversation yet
    if not st.session_state.conversation:
        st.markdown("""
            <div class="welcome-card">
                <h2>👋 Welcome to Ruby!</h2>
                <p>Your intelligent AI assistant is here to help. Ask me anything, and I'll do my best to assist you.</p>
                <p style="margin-top: 15px; font-size: 14px; opacity: 0.8;">
                    💡 Tip: Sign up to unlock advanced features and save your conversations!
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Display conversation
    for msg in st.session_state.conversation:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
                    
    user_input = st.chat_input("💬 Say something....>_<") 
    
    if user_input:
       st.session_state.conversation.append({
           "role": "user",
           "content": user_input
       }) 
       
       with st.chat_message("user"):
           st.write(user_input)
           
       with st.chat_message("assistant"):
           with st.spinner("🤔 Thinking...."):
               user_que = st.session_state.conversation[-1]["content"]
               context = f"""
You are an assistant. 
        If answer not found say: information is not available.
        Also remind user to signup at end in short.
        if answer not found : information is not available at website.
        Question: {user_que}
               """

               response = llm.invoke(context)
               reply = response.content
               st.write(reply)
               st.session_state.conversation.append({
                   "role": "assistant",
                   "content": reply
               })

load_dotenv()

llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider= "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY")
)