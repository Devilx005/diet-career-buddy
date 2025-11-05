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
    if not username:
        return "G"
    return username[0].upper()

# FIXED CSS - No extra spacing, proper positioning
st.markdown("""
<style>
    /* Remove all extra margins and padding */
    .main .block-container { 
        padding-top: 0rem !important; 
        padding-left: 1rem !important; 
        padding-right: 1rem !important; 
        margin-top: 0rem !important;
        max-width: 100% !important;
    }
    
    .stApp > header { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    .stDeployButton { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    
    /* TOP BAR - Fixed positioning */
    .top-nav {
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
    }
    
    .nav-left {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .hamburger-btn {
        display: none; /* Hidden by default */
        background: none;
        border: none;
        color: #a0aec0;
        font-size: 18px;
        cursor: pointer;
        padding: 8px;
        border-radius: 4px;
        width: 36px;
        height: 36px;
        text-align: center;
    }
    
    .hamburger-btn:hover {
        background: #424242;
        color: white;
    }
    
    .hamburger-btn.show {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .app-title {
        font-size: 1.1em;
        font-weight: 600;
        color: #10a37f;
    }
    
    .nav-right {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .login-btn {
        background: #10a37f;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        font-size: 14px;
    }
    
    .login-btn:hover {
        background: #0d8f6b;
    }
    
    .user-info {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #a0aec0;
        font-size: 14px;
    }
    
    .user-avatar {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #10a37f;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        font-size: 12px;
    }
    
    /* MAIN CONTENT - Reduced spacing */
    .main-content {
        margin-top: 60px; /* Reduced from 80px */
        padding: 10px 0; /* Reduced padding */
    }
    
    /* CONTENT SPACING - Tighter layout */
    .content-header {
        margin-bottom: 15px !important; /* Reduced from default */
    }
    
    .stColumns { gap: 0.5rem !important; }
    
    div[data-testid="stVerticalBlock"] { 
        gap: 0.3rem !important; /* Reduced gap */
    }
    
    /* SIDEBAR - Left side */
    .sidebar {
        position: fixed;
        top: 50px;
        left: -280px;
        width: 260px;
        height: calc(100vh - 50px);
        background: #171717;
        border-right: 1px solid #444;
        transition: left 0.3s ease;
        z-index: 999;
        padding: 15px 0;
    }
    
    .sidebar.open {
        left: 0;
    }
    
    .sidebar-item {
        padding: 10px 20px;
        color: #a0aec0;
        cursor: pointer;
        display: block;
        text-decoration: none;
        font-size: 14px;
        border: none;
        background: none;
        width: 100%;
        text-align: left;
    }
    
    .sidebar-item:hover {
        background: #2d2d2d;
        color: white;
    }
    
    /* LOGIN MODAL */
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
    
    .modal-content {
        background: #212121;
        padding: 30px;
        border-radius: 10px;
        border: 2px solid #10a37f;
        max-width: 400px;
        width: 90%;
        position: relative;
    }
    
    .close-btn {
        position: absolute;
        top: 10px;
        right: 15px;
        background: none;
        border: none;
        color: #a0aec0;
        font-size: 20px;
        cursor: pointer;
    }
    
    .close-btn:hover {
        color: white;
    }
    
    /* Remove extra spacing */
    .stMarkdown { margin-bottom: 0.5rem !important; }
    .element-container { margin-bottom: 0.5rem !important; }
</style>
""", unsafe_allow_html=True)

# TOP NAVIGATION BAR
hamburger_display = "show" if st.session_state.authenticated else ""

st.markdown(f"""
<div class="top-nav">
    <div class="nav-left">
        <button class="hamburger-btn {hamburger_display}" onclick="window.toggleSidebar = true">☰</button>
        <div class="app-title">🎓 DIET Career Buddy</div>
    </div>
    <div class="nav-right">
        {'' if st.session_state.authenticated else '<button class="login-btn" onclick="window.showLogin = true">Log in</button>'}
        {'' if not st.session_state.authenticated else f'<div class="user-info"><div class="user-avatar">{get_user_avatar(st.session_state.username)}</div><span>{st.session_state.username}</span></div>'}
    </div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR - Only when logged in
if st.session_state.authenticated:
    sidebar_class = "sidebar open" if st.session_state.sidebar_open else "sidebar"
    st.markdown(f"""
    <div class="{sidebar_class}">
        <div class="sidebar-item" style="border-bottom: 1px solid #444; margin-bottom: 10px; padding-bottom: 15px;">
            <strong style="color: #10a37f;">Navigation</strong>
        </div>
        <div class="sidebar-item">🏠 Home Dashboard</div>
        <div class="sidebar-item">💻 Tech Careers</div>
        <div class="sidebar-item">💰 Live Salary</div>
        <div class="sidebar-item">📚 Learning Paths</div>
        <div class="sidebar-item">🎓 DIET Guide</div>
        <div class="sidebar-item">🎯 Interview Prep</div>
        <div class="sidebar-item">📊 Live Jobs</div>
        <div style="margin: 15px 0; border-top: 1px solid #444;"></div>
        <div class="sidebar-item">🚪 Logout</div>
    </div>
    """, unsafe_allow_html=True)

# Hidden buttons for functionality
col_hidden = st.columns([1, 1, 1, 1, 1])

with col_hidden[0]:
    if st.button("🔐", key="show_login", help="Login"):
        st.session_state.show_login_modal = True
        st.rerun()

with col_hidden[1]:
    if st.button("☰", key="toggle_sidebar", help="Menu"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open
        st.rerun()

with col_hidden[2]:
    if st.button("🚪", key="logout", help="Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.page = 'home'
        st.session_state.sidebar_open = False
        st.rerun()

# LOGIN MODAL
if st.session_state.show_login_modal and not st.session_state.authenticated:
    # Modal overlay
    st.markdown("""
    <div class="login-modal">
        <div class="modal-content">
            <button class="close-btn">×</button>
            <h2 style="color: #10a37f; margin-bottom: 15px; text-align: center;">Welcome Back</h2>
            <p style="color: #a0aec0; margin-bottom: 20px; text-align: center;">Sign in to your account</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username", key="modal_user", placeholder="Enter username")
        password = st.text_input("Password", type="password", key="modal_pass", placeholder="Enter password")
        
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("🚀 Login", key="do_login", use_container_width=True, type="primary"):
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.show_login_modal = False
                    st.success(f"✅ Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials!")
        
        with col_btn2:
            if st.button("🎯 Demo", key="demo_login", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.username = "Demo User"
                st.session_state.show_login_modal = False
                st.success("✅ Demo access!")
                st.rerun()
        
        with col_btn3:
            if st.button("❌ Close", key="close_modal", use_container_width=True):
                st.session_state.show_login_modal = False
                st.rerun()

# MAIN CONTENT - Reduced spacing
st.markdown('<div class="main-content">', unsafe_allow_html=True)

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
    # HOME PAGE - Compact layout
    welcome_text = f"Welcome back, {st.session_state.username}!" if st.session_state.authenticated else "Welcome to DIET Career Buddy!"
    
    st.markdown(f'<div class="content-header"><h2>🎓 <strong>{welcome_text}</strong></h2></div>', unsafe_allow_html=True)
    st.markdown("### *Your AI-Powered Career Assistant with Real-Time Data*")
    
    # Show login prompt for guests
    if not st.session_state.authenticated:
        st.info("💡 **Sign in to unlock personalized dashboards and save your progress!**")
    
    # Navigation buttons - compact layout
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
    
    # Features section - compact
    st.markdown("""
    <div class="dashboard-card" style="margin: 15px 0;">
        <strong>🚀 What Makes Us Special:</strong><br><br>
        • <strong>Real-Time APIs:</strong> Live job market data<br>
        • <strong>DIET-Specific Guidance:</strong> Tailored for engineering students<br>
        • <strong>Interactive Dashboards:</strong> 6 comprehensive tools<br>
        • <strong>Professional Design:</strong> Clean, modern interface<br>
        • <strong>Market Intelligence:</strong> AI-powered insights
    </div>
    """, unsafe_allow_html=True)
    
    # Chat section - compact
    st.markdown("### 💬 **Ask Your Career Questions!**")
    
    col_input, col_button = st.columns([4, 1])
    
    with col_input:
        placeholder = f"Hi {st.session_state.username}, what would you like to know?" if st.session_state.authenticated else "What would you like to know about careers?"
        user_input = st.text_area("💭", 
                                 placeholder=placeholder + "\ne.g., What skills do I need for data science?",
                                 height=80,  # Reduced height
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

st.markdown('</div>', unsafe_allow_html=True)
