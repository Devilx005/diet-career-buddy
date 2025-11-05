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

# ChatGPT-style CSS additions
st.markdown("""
<style>
    /* TOP BAR STYLING - Like ChatGPT */
    .top-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background: #212121;
        border-bottom: 1px solid #444;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 20px;
        z-index: 1000;
    }
    
    .top-bar-left {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .hamburger-menu {
        display: none; /* Hidden when not logged in */
        cursor: pointer;
        padding: 8px;
        border-radius: 6px;
        background: #424242;
        color: white;
        border: none;
        font-size: 18px;
        width: 40px;
        height: 40px;
    }
    
    .hamburger-menu:hover {
        background: #555;
    }
    
    .hamburger-menu.visible {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .app-title {
        font-size: 1.2em;
        font-weight: 600;
        color: #10a37f;
    }
    
    .top-bar-right {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .login-btn {
        background: #10a37f !important;
        color: white !important;
        border: none !important;
        padding: 8px 16px !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
    }
    
    .login-btn:hover {
        background: #0d8f6b !important;
    }
    
    .user-profile {
        display: flex;
        align-items: center;
        gap: 10px;
        background: #424242;
        padding: 6px 12px;
        border-radius: 20px;
        color: white;
    }
    
    .user-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #10a37f;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
    }
    
    /* MAIN CONTENT AREA */
    .main-content {
        margin-top: 80px; /* Space for fixed top bar */
        min-height: calc(100vh - 80px);
    }
    
    /* SIDEBAR MENU - Like ChatGPT */
    .sidebar-menu {
        position: fixed;
        top: 60px;
        left: -300px;
        width: 280px;
        height: calc(100vh - 60px);
        background: #171717;
        border-right: 1px solid #444;
        transition: left 0.3s ease;
        z-index: 999;
        padding: 20px 0;
    }
    
    .sidebar-menu.open {
        left: 0;
    }
    
    .sidebar-item {
        padding: 12px 20px;
        color: #a0aec0;
        cursor: pointer;
        border: none;
        background: none;
        width: 100%;
        text-align: left;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .sidebar-item:hover {
        background: #2d2d2d;
        color: white;
    }
    
    .sidebar-item.active {
        background: #10a37f;
        color: white;
    }
    
    /* LOGIN MODAL - Overlay style */
    .login-modal {
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
    }
    
    .login-modal-content {
        background: #212121;
        padding: 40px;
        border-radius: 12px;
        border: 2px solid #10a37f;
        max-width: 400px;
        width: 90%;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    }
    
    .close-modal {
        position: absolute;
        top: 15px;
        right: 20px;
        background: none;
        border: none;
        color: #a0aec0;
        font-size: 24px;
        cursor: pointer;
    }
    
    .close-modal:hover {
        color: white;
    }
    
    /* Body padding for fixed header */
    body {
        padding-top: 60px !important;
    }
    
    /* Hide Streamlit's default header */
    .main .block-container {
        padding-top: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'show_login_modal' not in st.session_state:
    st.session_state.show_login_modal = False
if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = False

# Simple user database
USERS = {
    "student": "password123",
    "demo": "demo123", 
    "admin": "admin123",
    "diet": "diet2025"
}

def authenticate_user(username, password):
    return username in USERS and USERS[username] == password

def get_user_avatar(username):
    """Get user avatar initials"""
    if not username:
        return "G"  # Guest
    return username[0].upper()

# TOP BAR - Always visible like ChatGPT
hamburger_class = "hamburger-menu visible" if st.session_state.authenticated else "hamburger-menu"
user_display = st.session_state.username if st.session_state.authenticated else ""

st.markdown(f"""
<div class="top-bar">
    <div class="top-bar-left">
        <button class="{hamburger_class}" id="hamburger-btn" onclick="toggleSidebar()">☰</button>
        <div class="app-title">🎓 DIET Career Buddy</div>
    </div>
    <div class="top-bar-right">
        {"" if st.session_state.authenticated else '<button class="login-btn" id="login-btn" onclick="showLoginModal()">Log in</button>'}
        {"" if not st.session_state.authenticated else f'<div class="user-profile"><div class="user-avatar">{get_user_avatar(user_display)}</div><span>{user_display}</span></div>'}
    </div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR MENU - Only visible when logged in
sidebar_class = "sidebar-menu open" if st.session_state.sidebar_open else "sidebar-menu"
if st.session_state.authenticated:
    st.markdown(f"""
    <div class="{sidebar_class}" id="sidebar">
        <div class="sidebar-item" onclick="navigateTo('home')">🏠 Home Dashboard</div>
        <div class="sidebar-item" onclick="navigateTo('tech')">💻 Tech Careers</div>
        <div class="sidebar-item" onclick="navigateTo('salary')">💰 Live Salary</div>
        <div class="sidebar-item" onclick="navigateTo('learn')">📚 Learning Paths</div>
        <div class="sidebar-item" onclick="navigateTo('diet')">🎓 DIET Guide</div>
        <div class="sidebar-item" onclick="navigateTo('interview')">🎯 Interview Prep</div>
        <div class="sidebar-item" onclick="navigateTo('jobs')">📊 Live Jobs</div>
        <hr style="margin: 20px 0; border-color: #444;">
        <div class="sidebar-item" onclick="logout()">🚪 Logout</div>
    </div>
    """, unsafe_allow_html=True)

# LOGIN MODAL - Overlay style
if st.session_state.show_login_modal and not st.session_state.authenticated:
    st.markdown("""
    <div class="login-modal" id="login-modal">
        <div class="login-modal-content" style="position: relative;">
            <button class="close-modal" onclick="hideLoginModal()">×</button>
            <h2 style="color: #10a37f; margin-bottom: 20px;">Welcome Back</h2>
            <p style="color: #a0aec0; margin-bottom: 30px;">Sign in to access your personalized career dashboard</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form in modal
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            username = st.text_input("Username", key="modal_username", placeholder="Enter username")
            password = st.text_input("Password", type="password", key="modal_password", placeholder="Enter password")
            
            col_login, col_demo, col_close = st.columns(3)
            with col_login:
                if st.button("🚀 Login", key="modal_login", use_container_width=True, type="primary"):
                    if authenticate_user(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.show_login_modal = False
                        st.success(f"✅ Welcome, {username}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials!")
            
            with col_demo:
                if st.button("🎯 Demo", key="modal_demo", use_container_width=True):
                    st.session_state.authenticated = True
                    st.session_state.username = "Demo User"
                    st.session_state.show_login_modal = False
                    st.success("✅ Demo access granted!")
                    st.rerun()
            
            with col_close:
                if st.button("❌ Close", key="modal_close", use_container_width=True):
                    st.session_state.show_login_modal = False
                    st.rerun()

# JavaScript for interactivity
st.markdown("""
<script>
function showLoginModal() {
    // This will be handled by Streamlit button
    console.log('Login modal requested');
}

function hideLoginModal() {
    // This will be handled by Streamlit
    console.log('Hide login modal');
}

function toggleSidebar() {
    // This will be handled by Streamlit
    console.log('Toggle sidebar');
}

function navigateTo(page) {
    // This will be handled by Streamlit routing
    console.log('Navigate to:', page);
}

function logout() {
    // This will be handled by Streamlit
    console.log('Logout requested');
}
</script>
""", unsafe_allow_html=True)

# Handle login button click
col_hidden1, col_hidden2, col_hidden3 = st.columns([8, 1, 1])
with col_hidden2:
    if st.button("🔐", key="hidden_login_trigger", help="Show login modal"):
        st.session_state.show_login_modal = True
        st.rerun()

with col_hidden3:
    if st.button("☰", key="hidden_sidebar_trigger", help="Toggle sidebar"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open
        st.rerun()

# MAIN CONTENT AREA
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Content based on authentication and page
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
    # HOME PAGE - Always accessible (like ChatGPT)
    welcome_text = f"Welcome back, {st.session_state.username}!" if st.session_state.authenticated else "Welcome to DIET Career Buddy!"
    
    st.markdown(f"## 🎓 **{welcome_text}**")
    st.markdown("### *Your AI-Powered Career Assistant with Real-Time Data*")
    
    # Navigation buttons - Always visible
    if not st.session_state.authenticated:
        st.info("💡 **Sign in to unlock personalized dashboards and save your progress!**")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("💻\nTech\nCareers", key="nav_tech"):
            if st.session_state.authenticated:
                st.session_state.page = 'tech'
                st.rerun()
            else:
                st.session_state.show_login_modal = True
                st.rerun()
    
    with col2:
        if st.button("💰\nLive\nSalary", key="nav_salary"):
            if st.session_state.authenticated:
                st.session_state.page = 'salary'
                st.rerun()
            else:
                st.session_state.show_login_modal = True
                st.rerun()
    
    with col3:
        if st.button("📚\nLearning\nPaths", key="nav_learn"):
            if st.session_state.authenticated:
                st.session_state.page = 'learn'
                st.rerun()
            else:
                st.session_state.show_login_modal = True
                st.rerun()
    
    with col4:
        if st.button("🎓\nDIET\nGuide", key="nav_diet"):
            if st.session_state.authenticated:
                st.session_state.page = 'diet'
                st.rerun()
            else:
                st.session_state.show_login_modal = True
                st.rerun()
    
    with col5:
        if st.button("🎯\nInterview\nPrep", key="nav_interview"):
            if st.session_state.authenticated:
                st.session_state.page = 'interview'
                st.rerun()
            else:
                st.session_state.show_login_modal = True
                st.rerun()
    
    with col6:
        if st.button("📊\nLive\nJobs", key="nav_jobs"):
            if st.session_state.authenticated:
                st.session_state.page = 'jobs'
                st.rerun()
            else:
                st.session_state.show_login_modal = True
                st.rerun()
    
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
    
    # Chat section - always available
    st.markdown("### 💬 **Ask Your Career Questions!**")
    
    col_input, col_button = st.columns([4, 1])
    
    with col_input:
        placeholder_text = f"Hi {st.session_state.username}, what would you like to know?" if st.session_state.authenticated else "What would you like to know about careers?"
        user_input = st.text_area("💭", 
                                 placeholder=placeholder_text + "\ne.g., What skills do I need for data science?",
                                 height=100,
                                 key="main_chat_input")
    
    with col_button:
        st.markdown("<br>", unsafe_allow_html=True)
        send_clicked = st.button("🚀 Send", 
                                key="main_send", 
                                use_container_width=True,
                                type="primary")
    
    if send_clicked and user_input.strip():
        response_prefix = f"Great question, {st.session_state.username}! " if st.session_state.authenticated else "Great question! "
        
        if not st.session_state.authenticated:
            response_prefix += "💡 Sign in to access detailed dashboards. For now, here's some quick guidance: "
        
        response = response_prefix
        
        if any(word in user_input.lower() for word in ['salary', 'pay', 'money']):
            response += "💰 Check the **Live Salary** dashboard for comprehensive market data!"
        elif any(word in user_input.lower() for word in ['job', 'hiring', 'market']):
            response += "📊 Visit the **Live Jobs** dashboard for real-time insights!"
        else:
            response += "🎓 Explore our dashboards above for detailed insights!"
        
        st.markdown(f"""
        <div class="dashboard-card">
            <strong>❓ You asked:</strong><br>
            <em>"{user_input}"</em><br><br>
            <strong>🎓 AI Assistant:</strong><br>
            {response}
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
