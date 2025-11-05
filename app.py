import streamlit as st
from styles import get_main_css

# Import all dashboards (from root directory)
import tech_dashboard
import salary_dashboard
import learning_dashboard
import diet_guide
import interview_prep
import jobs_dashboard

st.set_page_config(
    page_title="🎓 DIET Career Buddy", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Apply CSS
st.markdown(get_main_css(), unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'show_login_modal' not in st.session_state:
    st.session_state.show_login_modal = False

# Simple user database
USERS = {
    "student": "password123",
    "demo": "demo123", 
    "admin": "admin123",
    "diet": "diet2025"
}

def authenticate_user(username, password):
    return username in USERS and USERS[username] == password

# CLEAN TOP BAR - Just title and login button
hamburger_display = "☰ " if st.session_state.authenticated else ""
login_button = "" if st.session_state.authenticated else """
<button style="
    background: #10a37f; 
    color: white; 
    border: none; 
    padding: 8px 16px; 
    border-radius: 6px; 
    font-weight: 600; 
    cursor: pointer;
    font-size: 14px;
" onclick="document.getElementById('login-trigger').click()">Log in</button>
"""

user_info = f"""
<div style="color: #a0aec0; font-size: 14px;">
    <span style="background: #10a37f; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; margin-right: 8px;">
        {st.session_state.username[0].upper() if st.session_state.username else ""}
    </span>
    {st.session_state.username}
</div>
""" if st.session_state.authenticated else ""

st.markdown(f"""
<div style="
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 50px;
    background: #212121;
    border-bottom: 1px solid #444;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    z-index: 1000;
">
    <div style="font-size: 1.1em; font-weight: 600; color: #10a37f;">
        {hamburger_display}🎓 DIET Career Buddy
    </div>
    <div style="display: flex; align-items: center; gap: 15px;">
        {login_button}
        {user_info}
    </div>
</div>
""", unsafe_allow_html=True)

# Hidden buttons for functionality (invisible)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("Login", key="login-trigger", help="Login"):
        st.session_state.show_login_modal = True
        st.rerun()

# LOGIN MODAL - Simple and clean
if st.session_state.show_login_modal and not st.session_state.authenticated:
    st.markdown("""
    <div style="
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2000;
    ">
        <div style="
            background: #212121;
            padding: 30px;
            border-radius: 10px;
            border: 2px solid #10a37f;
            max-width: 400px;
            width: 90%;
        ">
            <h2 style="color: #10a37f; margin-bottom: 15px; text-align: center;">Welcome Back</h2>
            <p style="color: #a0aec0; margin-bottom: 20px; text-align: center;">Sign in to your account</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form in center
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username", key="username", placeholder="Enter username")
        password = st.text_input("Password", type="password", key="password", placeholder="Enter password")
        
        col_login, col_demo, col_close = st.columns(3)
        
        with col_login:
            if st.button("🚀 Login", key="login", use_container_width=True, type="primary"):
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.show_login_modal = False
                    st.success(f"✅ Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials!")
        
        with col_demo:
            if st.button("🎯 Demo", key="demo", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.username = "Demo User"
                st.session_state.show_login_modal = False
                st.success("✅ Demo access!")
                st.rerun()
        
        with col_close:
            if st.button("❌ Close", key="close", use_container_width=True):
                st.session_state.show_login_modal = False
                st.rerun()

# Add logout functionality if logged in
if st.session_state.authenticated:
    with col2:
        if st.button("Logout", key="logout", help="Logout"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.page = 'home'
            st.rerun()

# MAIN CONTENT - Start after top bar with proper spacing
st.markdown("""
<div style="margin-top: 70px;">
""", unsafe_allow_html=True)

# Dashboard routing
if st.session_state.page == 'tech' and st.session_state.authenticated:
    tech_dashboard.show()
elif st.session_state.page == 'salary' and st.session_state.authenticated:
    salary_dashboard.show()
elif st.session_state.page == 'learn' and st.session_state.authenticated:
    learning_dashboard.show()
elif st.session_state.page == 'diet' and st.session_state.authenticated:
    diet_guide.show()
elif st.session_state.page == 'interview' and st.session_state.authenticated:
    interview_prep.show()
elif st.session_state.page == 'jobs' and st.session_state.authenticated:
    jobs_dashboard.show()
else:
    # HOME PAGE - Clean layout
    welcome_text = f"Welcome back, {st.session_state.username}!" if st.session_state.authenticated else "Welcome to DIET Career Buddy!"
    
    st.markdown(f"## 🎓 **{welcome_text}**")
    st.markdown("### *Your AI-Powered Career Assistant with Real-Time Data*")
    
    # Show login prompt for guests
    if not st.session_state.authenticated:
        st.info("💡 **Sign in to unlock personalized dashboards and save your progress!**")
    
    # Navigation buttons
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    dashboard_buttons = [
        ("💻\nTech\nCareers", "tech"),
        ("💰\nLive\nSalary", "salary"), 
        ("📚\nLearning\nPaths", "learn"),
        ("🎓\nDIET\nGuide", "diet"),
        ("🎯\nInterview\nPrep", "interview"),
        ("📊\nLive\nJobs", "jobs")
    ]
    
    columns = [col1, col2, col3, col4, col5, col6]
    
    for i, (label, page_key) in enumerate(dashboard_buttons):
        with columns[i]:
            if st.button(label, key=f"nav_{page_key}"):
                if st.session_state.authenticated:
                    st.session_state.page = page_key
                    st.rerun()
                else:
                    st.session_state.show_login_modal = True
                    st.rerun()
    
    # Features section
    st.markdown("""
    <div class="dashboard-card">
        <strong>🚀 What Makes Us Special:</strong><br><br>
        • <strong>Real-Time APIs:</strong> Live job market data from GitHub & CoinGecko<br>
        • <strong>DIET-Specific Guidance:</strong> Tailored advice for engineering students<br>
        • <strong>Interactive Dashboards:</strong> 6 comprehensive career analysis tools<br>
        • <strong>Professional Design:</strong> Clean, modern interface<br>
        • <strong>Market Intelligence:</strong> AI-powered career insights
    </div>
    """, unsafe_allow_html=True)
    
    # Chat section
    st.markdown("### 💬 **Ask Your Career Questions!**")
    
    col_input, col_button = st.columns([4, 1])
    
    with col_input:
        placeholder = f"Hi {st.session_state.username}, what would you like to know?" if st.session_state.authenticated else "What would you like to know about careers?"
        user_input = st.text_area("💭", 
                                 placeholder=placeholder + "\ne.g., What skills do I need for data science?",
                                 height=100,
                                 key="chat_input")
    
    with col_button:
        st.markdown("<br>", unsafe_allow_html=True)
        send_clicked = st.button("🚀 Send", 
                                key="send_chat", 
                                use_container_width=True,
                                type="primary")
    
    if send_clicked and user_input.strip():
        response_prefix = f"Great question, {st.session_state.username}! " if st.session_state.authenticated else "Great question! "
        
        if not st.session_state.authenticated:
            response_prefix += "💡 Sign in to access detailed dashboards. Here's some quick guidance: "
        
        response = response_prefix + "🎓 Explore our dashboards above for detailed insights!"
        
        st.markdown(f"""
        <div class="dashboard-card">
            <strong>❓ You asked:</strong> <em>"{user_input}"</em><br><br>
            <strong>🎓 AI Assistant:</strong> {response}
        </div>
        """, unsafe_allow_html=True)

# Close the main content div properly (no visible text)
st.markdown("</div>", unsafe_allow_html=True)
