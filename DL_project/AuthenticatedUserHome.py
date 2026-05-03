import streamlit as st 
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import vector_store as vs 
import time
# Selenium scraping removed to run just the chatbot
# Vector testing load instead of re-scraping
def groq_model():
    return init_chat_model(
        model = "llama-3.3-70b-versatile",
        model_provider = "openai",
        base_url = "https://api.groq.com/openai/v1",
        api_key = os.getenv("GROQ_API_KEY")
    )
    
def gemini_model():
    return init_chat_model(
        model = "gemini-2.5-flash",
        model_provider = "google",
        api_key = os.getenv("GEMINI_API_KEY")
    )    
    
def lm_model():
    return init_chat_model(
        model = "google/gemma-3n-e4b",
        model_provider = "openai",
        base_url = "http://127.0.0.1:1234/v1",
        api_key = "dummy-key"
    )    

def get_vectordb():
    return vs.load_chroma_db()

vectordb = get_vectordb()
# RAG_PROMPT = """
# You are an AI assistant that helps users by providing accurate and concise information based on the provided context from Sunbeam's courses and offerings. Use the context to answer the user's questions effectively.
# If the context does not contain the answer, respond with "I'm sorry, I don't have that information right now."

# """   

def rag_answer(question, model_choice):

    # 🛑 HARD GUARD
    if question is None or not str(question).strip():
        return "Please ask a valid question.", []

    question = str(question).strip()

    docs = vectordb.similarity_search(question, k=5)
    context = "\n\n".join(d.page_content for d in docs)

    llm = (
        groq_model() if model_choice == "GROQ model" else
        gemini_model() if model_choice == "Gemini model" else
        lm_model()
    )

    prompt = f"""
You are the official AI assistant for Sunbeam Infotech Institute Pune and must answer all user queries using the provided scraped data and your internal reasoning. When users ask about Sunbeam generally or ask what it is, provide a bulleted list about the institute including its reputation and values using your thinking power and provided info. If the query concerns available internships, retrieve details specifically from the available internship programs accordion, but if the query is about internship batches schedule, use the internship batches schedule table exclusively. For internship schedules, you must strictly state the start date as 10 dec 2025 and the end date as 5 jan 2026, expressing the duration specifically as 1 month and never guessing a different timeframe. For courses such as Apache Spark Mastery, Aptitude, C++, Core Java, Data Structures and Algorithms, DevOps, Dream LLM, Machine Learning, Mastering GenAI, Mastering MCQs, or MERN Development, provide relevant details and always state the duration in hours; if the exact duration is not found, give a single value between range of 40 hours to 80 hours. You are strictly prohibited from getting confused between internships and courses with similar names. If a user asks for contact details or location, provide the full Pune contact information. In case of missing information, do not say you cannot find it; instead, provide the most relevant and helpful related answer possible. If an error occurs, return a standard error message. For queries specifically about the institute, end your response by inviting the user to visit https://www.sunbeaminfo.in/about-us for more info. For modular course queries, end with a link to https://www.sunbeaminfo.in/modular-courses-home. For internship queries, end with a link to https://www.sunbeaminfo.in/internship.
{context}

Question: {question}
"""

    response = llm.invoke(prompt)
    return response.content, docs


 
def authenticated_user_home_page():
    load_dotenv()
    
    if "chats" not in st.session_state:
        st.session_state.chats = {"Chat 1": []}
        
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = "Chat 1"
        
    if "last_user_index" not in st.session_state:
        st.session_state.last_user_index = None  
        
    if "edit_index" not in st.session_state:
        st.session_state.edit_index = None

    if "edit_text" not in st.session_state:
        st.session_state.edit_text = ""   
    
    if "awaiting_reply" not in st.session_state:
        st.session_state.awaiting_reply = False
    
    # Enhanced CSS with modern design - FIXED WHITE SPACE ISSUES
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        /* Main background */
        .stApp {
            background: linear-gradient(135deg, #0f2027 0%, #203a43 25%, #2c5364 50%, #1a365d 75%, #0f172a 100%) !important;
            background-size: 400% 400%;
            animation: gradientShift 20s ease infinite;
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
        
        
        
        /* Top decoration area */
        [data-testid="stDecoration"] {
            background: linear-gradient(135deg, #0f2027 0%, #203a43 100%) !important;
        }
        
        /* Main content blocks */
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
        
        /* All vertical blocks */
        [data-testid="stVerticalBlock"] {
            background: transparent !important;
        }
        
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: transparent !important;
        }
        
        /* Horizontal blocks */
        [data-testid="stHorizontalBlock"] {
            background: transparent !important;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(135deg, #0f2027 0%, #203a43 25%, #2c5364 50%, #1a365d 75%, #0f172a 100%) !important;
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        section[data-testid="stSidebar"] > div {
            background: transparent !important;
        }
        
        section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            background: transparent !important;
        }
        
        /* Sidebar logo animation */
        .sidebar-logo {
            animation: float 3s ease-in-out infinite;
            filter: drop-shadow(0 5px 15px rgba(255, 255, 255, 0.3));
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        /* Radio buttons styling */
        .stRadio > label {
            color: white !important;
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 10px;
        }
        
        .stRadio > div {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        /* Header styling */
        .main-header {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px 30px;
            margin-bottom: 20px;
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
        
        /* Button styling - New Chat */
        div.stButton > button {
            width: 100%;
            height: 50px;
            font-size: 16px;
            font-weight: 600;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 15px;
            box-shadow: 0 4px 15px 0 rgba(116, 79, 168, 0.4);
            transition: all 0.3s ease;
            margin: 5px 0;
        }
        
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px 0 rgba(116, 79, 168, 0.6);
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }
        
        /* Logout button specific styling */
        .logout-container button {
            background: rgba(220, 38, 38, 0.9) !important;
            height: 45px !important;
            font-size: 16px !important;
            border-radius: 12px !important;
        }
        
        .logout-container button:hover {
            background: rgba(220, 38, 38, 1) !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.5) !important;
        }
        
        /* Chat messages */
        .stChatMessage {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            margin: 15px 0;
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
        
        /* Chat input */
        .stChatInputContainer {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 25px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
        }
        
        .stChatInputContainer:focus-within {
            border-color: rgba(255, 255, 255, 0.6);
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
        }
        
        /* Edit text area */
        .stTextArea textarea {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 15px !important;
            color: white !important;
            padding: 15px !important;
        }
        
        .stTextArea textarea:focus {
            border-color: rgba(255, 255, 255, 0.6) !important;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Divider */
        hr {
            border-color: rgba(255, 255, 255, 0.2) !important;
            margin: 20px 0 !important;
        }
        
        /* Text colors */
        h1, h2, h3, p, label, span {
            color: white !important;
        }
        
        /* Spinner */
        .stSpinner > div {
            border-color: rgba(255, 255, 255, 0.3) !important;
            border-top-color: white !important;
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
        
        /* Welcome message for empty chat */
        .welcome-msg {
            text-align: center;
            padding: 60px 20px;
            animation: fadeIn 1s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .welcome-msg h2 {
            font-size: 32px;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .welcome-msg p {
            font-size: 18px;
            opacity: 0.9;
        }
                
        /* Ensure the overall container fills the screen */
        [data-testid="stAppViewContainer"] {
            background: transparent !important;
            min-height: 100vh;
        }

        /* Force the main scrollable area to be transparent to show the background */
        [data-testid="stAppViewMain"] {
            background: transparent !important;
        }

        /* Remove padding/margin that creates white gaps at the bottom */
        .main .block-container {
            padding-bottom: 0rem !important;
            min-height: 100vh;
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
                
        /* Fix for the footer area that sometimes appears white */
        footer {
            display: none; /* This removes the "Made with Streamlit" footer which often creates a gap */
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Fixed header layout - showing full title and logout button properly
    col1, col2 = st.columns([10, 1])
    
    with col1:
        # st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.markdown(f"# 💎 Ruby - Welcome, {st.session_state.get('username', 'User')}!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="logout-container">', unsafe_allow_html=True)
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.page = "Unauthenticated_User_Home"
            st.session_state.authenticated = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
            
    with st.sidebar:
        bot_logo = "photos\\botlogo.png"
        st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
        st.image(bot_logo, width=90)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 🤖 AI Model Selection")
        model = st.radio(
            "Choose your model:",
            ["GROQ model", "Gemini model", "LM Model"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("➕ New Chat", use_container_width=True):
            name = f"Chat {len(st.session_state.chats) + 1}"
            st.session_state.chats[name] = []
            st.session_state.current_chat = name
            st.rerun()
        
        if st.button("🧹 Clear Chat History", use_container_width=True):
            st.session_state.chats[st.session_state.current_chat] = []
            st.session_state.last_user_index = None
            st.session_state.edit_index = None
            st.session_state.awaiting_reply = False
            st.rerun()
   
        st.divider()
        st.markdown("### 📝 Chat History")
        
        for chat in st.session_state.chats:
            if st.button(f"💬 {chat}", key=chat, use_container_width=True):
                st.session_state.current_chat = chat
                st.rerun()
                
    gender = st.session_state.get("gender", "Male")
    user_icon = "photos\\male.png" if gender == "Male" else "photos\\female.png"
    bot_icon = "photos\\bot.png" 
                   
    messages = st.session_state.chats[st.session_state.current_chat]
    
    if not messages:
        st.markdown("""
            <div class="welcome-msg">
                <h2>👋 Ready to Chat!</h2>
                <p>Start a conversation by typing a message below.</p>
                <p style="margin-top: 15px; font-size: 14px; opacity: 0.8;">
                    💡 You can edit your messages and regenerate responses anytime!
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    
            
    user_input = st.chat_input("💬 Say something....>_<")

    if user_input:
        messages.append({"role": "user", "content": user_input})
        st.session_state.last_user_index = len(messages) - 1
        st.session_state.awaiting_reply = True
        # st.rerun()
    for i, msg in enumerate(messages):
        avatar = user_icon if msg["role"] == "user" else bot_icon
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])
            
            if (msg["role"] == "user" 
                and i == st.session_state.last_user_index
                and st.session_state.edit_index is None
            ):
                if st.button("✏️ Edit Prompt", key=f"edit_{i}"):
                    st.session_state.edit_index = i
                    st.session_state.edit_text = msg["content"]
                    st.rerun()
                    
    if st.session_state.edit_index is not None:
        edited = st.text_area("✨ Modify your prompt", st.session_state.edit_text, height=100)
        col1, col2 = st.columns(2)
        
        if col1.button("🔄 Regenerate", use_container_width=True):
            idx = st.session_state.edit_index
            messages[idx]["content"] = edited
            messages.pop(idx + 1)

            answer, _ = rag_answer(edited, model)
            messages.insert(idx + 1, {"role": "assistant", "content": answer})

            st.session_state.edit_index = None
            st.rerun()
            
        if col2.button("❌ Cancel", use_container_width=True):
            st.session_state.edit_index = None
            st.rerun()
            
    if st.session_state.awaiting_reply:
        with st.chat_message("assistant", avatar=bot_icon):
            with st.spinner("🤔 Thinking..."):
                time.sleep(1)  # Simulate thinking time
                answer, docs = rag_answer(user_input, model)
                st.write(answer)
                # st.write(reply.content)
                with st.expander("📚 Sources"):
                    for d in docs:
                        st.write(
                            f"- {d.metadata.get('source')} "
                            f"(chunk {d.metadata.get('chunk_id')})"
                        )

        messages.append({
            "role": "assistant",
            "content": answer
        })
        st.session_state.awaiting_reply = False
        st.rerun()