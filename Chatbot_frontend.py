import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import nltk
import json
import pickle
import numpy as np
from keras.models import load_model
from PIL import Image
import random
from datetime import datetime

# Load AI components
nltk.download('stopwords')
nltk.download("punkt") 
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# Page Config
im = Image.open('bot.jpg')
st.set_page_config(layout="wide", page_title="DIET Career Guidance Chatbot", page_icon=im)

# Load AI Backend Data
with open('intents3.json', 'r') as file:
    intents = json.load(file)
with open('words.pkl', 'rb') as file:
    words = pickle.load(file)
with open('classes.pkl', 'rb') as file:
    classes = pickle.load(file)
model = load_model('chatbot_model.h5')

# =================== USER DATA MANAGEMENT ===================
def load_user_data():
    """Load registered users and their chat history"""
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except:
        return {"users": {}, "chat_histories": {}}

def save_user_data(data):
    """Save user data to file"""
    try:
        with open('user_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    except:
        pass

def get_user_chat_history(username):
    """Get chat history for logged-in user"""
    user_data = load_user_data()
    return user_data.get("chat_histories", {}).get(username, [])

def save_user_chat_history(username, messages):
    """Save chat history for logged-in user"""
    user_data = load_user_data()
    if "chat_histories" not in user_data:
        user_data["chat_histories"] = {}
    user_data["chat_histories"][username] = messages
    user_data["users"][username]["last_active"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_user_data(user_data)

# =================== AUTHENTICATION FUNCTIONS ===================
def register_user(username, password):
    """Register a new user"""
    user_data = load_user_data()
    if "users" not in user_data:
        user_data["users"] = {}
    
    if username in user_data["users"]:
        return False, "Username already exists!"
    
    user_data["users"][username] = {
        "password": password,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_active": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_user_data(user_data)
    return True, "Registration successful!"

def login_user(username, password):
    """Login existing user"""
    user_data = load_user_data()
    users = user_data.get("users", {})
    
    if username in users and users[username]["password"] == password:
        return True, "Login successful!"
    return False, "Invalid credentials!"

# =================== CHAT RESPONSE FUNCTIONS ===================
def fallback_response(user_text, username=None):
    """Generate career guidance responses"""
    user_text = user_text.lower().strip()
    
    greeting = f"Hello {username}! " if username else "Hello! "
    
    if any(word in user_text for word in ["hello", "hi", "hey"]):
        base_msg = f"{greeting}Welcome to DIET Career Guidance! I can help with career paths, salaries, job market trends, and skills development."
        if username:
            base_msg += f" Your chat history is being saved. 💾"
        else:
            base_msg += f" 💡 Tip: Login to save your chat history!"
        return base_msg
    
    elif "career" in user_text or "job" in user_text:
        return f"🎯 **Career Domains I can help with:**\n\n🖥️ **Technology:** Software Development, Data Science, AI/ML\n🏥 **Healthcare:** Medicine, Nursing, Pharmacy\n💼 **Business:** Marketing, Finance, Management\n🎨 **Creative:** Design, Content, Media\n\nWhich field interests you most?"
    
    elif any(word in user_text for word in ["technology", "tech", "software", "programming"]):
        return "🚀 **Technology Careers - Perfect for DIET Students:**\n\n**High-Demand Roles:**\n• Software Developer (₹3-20+ LPA)\n• Data Scientist (₹4-25+ LPA)\n• Mobile App Developer (₹3-18+ LPA)\n• AI/ML Engineer (₹5-30+ LPA)\n• DevOps Engineer (₹5-25+ LPA)\n\n**Key Skills:** Python, Java, JavaScript, React, SQL, Git\n\nWhich tech role interests you?"
    
    elif "salary" in user_text or "pay" in user_text:
        return "💰 **Salary Ranges in India (Tech Sector):**\n\n**Entry Level (0-2 years):** ₹3-8 LPA\n**Mid Level (3-6 years):** ₹8-20 LPA\n**Senior Level (6+ years):** ₹15-35+ LPA\n\n*Varies by company, location, and skills!*"
    
    elif "maker" in user_text or "creator" in user_text:
        return "🎓 **Created by DIET Engineering Students:**\n\nVINAYAK KHARADE, PRATHMESH SANDIM, SATWIK TAMBEWAGH & ROHAN SAWANT\n\n**Institution:** Dnyanshree Institute of Engineering & Technology\n**Project:** AI Career Guidance System with ChatGPT-like interface"
    
    else:
        tip = f" 💡 Login to save this conversation!" if not username else f" Your responses are being saved, {username}! 💾"
        return f"Thanks for your question! I'm your DIET Career AI Assistant.{tip}\n\nI can help with:\n• Career path exploration\n• Salary information & trends\n• Skill development guidance\n• Job market insights\n\nWhat would you like to know?"

def chatbot_response(msg, username=None):
    """Main response function with AI model + fallback"""
    try:
        # You can add your AI model logic here
        return fallback_response(msg, username)
    except:
        return fallback_response(msg, username)

# =================== MAIN INTERFACE ===================
# Initialize session state for guest usage
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your DIET Career Assistant. I can help with career guidance, job searches, and skill development. 💡 **Tip:** Login to save your chat history!"}
    ]

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Main Header
st.markdown(
    """
    <div style="background-color: #FF8C00 ; padding: 10px">
        <h1 style="color: brown; font-size: 48px; font-weight: bold; text-align: center">
           <span style="color: black; font-size: 64px">C</span>areer <span style="color: black; font-size: 64px">B</span>uddy
        </h1>
        <p style="color: white; text-align: center; margin: 0;">💬 ChatGPT-like Career Guidance • 🎓 Built by DIET Students</p>
    </div>
    """, unsafe_allow_html=True
)

# Hide streamlit menu
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# =================== SIDEBAR - ChatGPT Style ===================
with st.sidebar:
    st.markdown("### 🎓 DIET Career AI")
    
    # Login/User Status
    if not st.session_state.logged_in:
        st.markdown("#### 🔐 Login / Register")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                login_username = st.text_input("Username", key="login_user")
                login_password = st.text_input("Password", type="password", key="login_pass")
                login_btn = st.form_submit_button("🚀 Login")
                
                if login_btn and login_username and login_password:
                    success, msg = login_user(login_username, login_password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.current_user = login_username
                        # Load saved chat history
                        saved_history = get_user_chat_history(login_username)
                        if saved_history:
                            st.session_state.messages = saved_history
                        st.success(f"Welcome back, {login_username}! 🎉")
                        st.rerun()
                    else:
                        st.error(msg)
        
        with tab2:
            with st.form("register_form"):
                reg_username = st.text_input("Choose Username", key="reg_user")
                reg_password = st.text_input("Choose Password", type="password", key="reg_pass")
                reg_btn = st.form_submit_button("📝 Register")
                
                if reg_btn and reg_username and reg_password:
                    success, msg = register_user(reg_username, reg_password)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
        
        st.markdown("---")
        st.markdown("**🌟 Guest Mode Active**")
        st.markdown("✅ Browse freely\n\n❌ Chat history not saved\n\n💡 Login to save conversations!")
    
    else:
        # User is logged in
        st.markdown(f"#### 👤 Welcome, {st.session_state.current_user}!")
        
        user_data = load_user_data()
        user_info = user_data.get("users", {}).get(st.session_state.current_user, {})
        
        st.markdown(f"**💾 Chat History:** Saving automatically")
        st.markdown(f"**📅 Member since:** {user_info.get('created', 'Unknown')}")
        
        if st.button("🚪 Logout", use_container_width=True):
            # Save current chat before logout
            if st.session_state.current_user and st.session_state.messages:
                save_user_chat_history(st.session_state.current_user, st.session_state.messages)
            
            # Reset to guest mode
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm your DIET Career Assistant. You're now in guest mode. Login to save your chat history!"}
            ]
            st.rerun()
    
    st.markdown("---")
    
    # New Chat Button (ChatGPT style)
    if st.button("➕ New Chat", use_container_width=True):
        # Save current chat if logged in
        if st.session_state.logged_in and st.session_state.current_user:
            save_user_chat_history(st.session_state.current_user, st.session_state.messages)
        
        # Start new chat
        welcome_msg = f"Hello {st.session_state.current_user}! Starting a new chat. Previous conversation saved. How can I help you today?" if st.session_state.logged_in else "Hello! Starting a new chat session. How can I help you with your career today? 💡 Login to save conversations!"
        
        st.session_state.messages = [
            {"role": "assistant", "content": welcome_msg}
        ]
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 👥 About")
    st.markdown("""
    **DIET Team:**
    • VINAYAK KHARADE
    • PRATHMESH SANDIM  
    • SATWIK TAMBEWAGH
    • ROHAN SAWANT
    
    **Features:**
    ✅ Guest browsing
    💾 Login to save chats
    🤖 AI-powered responses
    📊 Real job market data
    """)

# =================== MAIN CHAT INTERFACE ===================
# Status indicator
status_color = "🟢" if st.session_state.logged_in else "🔵"
status_text = f"{status_color} {'Logged in as ' + st.session_state.current_user + ' (Saving chats)' if st.session_state.logged_in else 'Guest Mode (Chats not saved)'}"
st.markdown(f"**Status:** {status_text}")

# Display chat messages
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        message(msg["content"], is_user=True, key=f"user_{i}")
    else:
        message(msg["content"], key=f"bot_{i}")

# Chat input
st.markdown("---")
with st.form(key='chat_form', clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Message Career Buddy...", 
            key="user_input", 
            placeholder="Ask about careers, salaries, skills, or job market trends..."
        )
    
    with col2:
        send_button = st.form_submit_button("Send ⬆️")

# Process user input
if send_button and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate bot response
    current_user = st.session_state.current_user if st.session_state.logged_in else None
    bot_response = chatbot_response(user_input, current_user)
    
    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    # Save to persistent storage if logged in
    if st.session_state.logged_in and st.session_state.current_user:
        save_user_chat_history(st.session_state.current_user, st.session_state.messages)
    
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666666; font-size: 14px;'>
        <p><strong>🎓 DIET Career AI Assistant</strong> | ChatGPT-like Interface | Built by Computer Science Students</p>
        <p>💡 Free to browse • 🔐 Login to save • 🤖 AI-powered career guidance</p>
    </div>
    """, unsafe_allow_html=True
)
