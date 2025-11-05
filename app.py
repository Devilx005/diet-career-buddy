import streamlit as st
from styles import get_main_css
import random
import re
from datetime import datetime, timedelta
import hashlib

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

# Professional Auth CSS
st.markdown("""
<style>
    .auth-modal {
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
    
    .auth-container {
        max-width: 420px;
        width: 90%;
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        border-radius: 16px;
        border: 2px solid #10a37f;
        box-shadow: 0 20px 60px rgba(16, 163, 127, 0.3);
        padding: 40px 30px;
    }
    
    .auth-header {
        text-align: center;
        margin-bottom: 25px;
    }
    
    .auth-title {
        font-size: 1.6em;
        font-weight: 700;
        color: #10a37f;
        margin-bottom: 8px;
    }
    
    .auth-subtitle {
        color: #a0aec0;
        font-size: 0.9em;
    }
    
    .oauth-btn {
        width: 100%;
        padding: 12px;
        margin: 6px 0;
        border: 1px solid #555;
        border-radius: 8px;
        background: #333;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
    
    .oauth-btn:hover {
        background: #444;
        border-color: #10a37f;
        transform: translateY(-1px);
    }
    
    .google-btn {
        background: #4285f4 !important;
        border-color: #4285f4 !important;
    }
    
    .google-btn:hover {
        background: #3367d6 !important;
    }
    
    .divider {
        text-align: center;
        margin: 20px 0;
        position: relative;
        color: #666;
        font-size: 0.85em;
    }
    
    .divider::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 1px;
        background: #444;
    }
    
    .divider span {
        background: #1a1a1a;
        padding: 0 12px;
    }
</style>
""", unsafe_allow_html=True)

# Session State
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'show_login_modal' not in st.session_state:
    st.session_state.show_login_modal = False
if 'auth_method' not in st.session_state:
    st.session_state.auth_method = 'email'
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'phone_for_otp' not in st.session_state:
    st.session_state.phone_for_otp = ""
if 'current_otp' not in st.session_state:
    st.session_state.current_otp = ""

# Enhanced User Database
USER_DB = {
    "emails": {
        "demo@gmail.com": {"password": "demo123", "name": "Demo User"},
        "student@diet.ac.in": {"password": "student123", "name": "DIET Student"}
    },
    "phones": {
        "9876543210": {"name": "Phone User"}
    }
}

def authenticate_user(username, password):
    """Simple username/password auth"""
    USERS = {"student": "password123", "demo": "demo123", "admin": "admin123", "diet": "diet2025"}
    return username in USERS and USERS[username] == password

def authenticate_email(email, password):
    """Email authentication"""
    if email in USER_DB["emails"]:
        return USER_DB["emails"][email]["password"] == password, USER_DB["emails"][email]["name"]
    return False, None

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    cleaned = re.sub(r'[^\d]', '', phone)
    return len(cleaned) == 10 and cleaned.startswith(('6', '7', '8', '9'))

def generate_otp():
    return f"{random.randint(100000, 999999)}"

def show_professional_login():
    """Professional login modal"""
    st.markdown('<div class="auth-modal">', unsafe_allow_html=True)
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="auth-header">
        <div class="auth-title">Welcome Back!</div>
        <div class="auth-subtitle">Sign in to access your personalized career dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    
    # OAuth Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌐 Google", key="google_auth", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.username = "Google User"
            st.session_state.show_login_modal = False
            st.success("✅ Signed in with Google!")
            st.rerun()
    
    with col2:
        if st.button("🎯 Demo", key="demo_quick", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.username = "Demo User"
            st.session_state.show_login_modal = False
            st.success("✅ Demo access!")
            st.rerun()
    
    st.markdown('<div class="divider"><span>Or continue with</span></div>', unsafe_allow_html=True)
    
    # Method Selection
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📧 Email", key="email_method", use_container_width=True,
                    type="primary" if st.session_state.auth_method == 'email' else "secondary"):
            st.session_state.auth_method = 'email'
            st.session_state.otp_sent = False
            st.rerun()
    
    with col2:
        if st.button("📱 Phone", key="phone_method", use_container_width=True,
                    type="primary" if st.session_state.auth_method == 'phone' else "secondary"):
            st.session_state.auth_method = 'phone'
            st.session_state.otp_sent = False
            st.rerun()
    
    st.markdown("---")
    
    # Email Method
    if st.session_state.auth_method == 'email':
        st.markdown("**📧 Email Login**")
        
        email = st.text_input("Email", placeholder="Enter your email", key="email_input")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="email_password")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("🚀 Sign In", key="email_signin", use_container_width=True, type="primary"):
                if not email or not password:
                    st.error("❌ Please fill all fields!")
                elif not is_valid_email(email):
                    st.error("❌ Invalid email format!")
                else:
                    success, name = authenticate_email(email, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.username = name
                        st.session_state.show_login_modal = False
                        st.success(f"✅ Welcome, {name}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials!")
        
        with col2:
            if st.button("📝 Register", key="email_register", use_container_width=True):
                st.info("📝 Registration coming soon!")
    
    # Phone Method
    elif st.session_state.auth_method == 'phone':
        if not st.session_state.otp_sent:
            st.markdown("**📱 Phone Login**")
            
            phone = st.text_input("Phone Number", placeholder="Enter 10-digit number", key="phone_input", max_chars=10)
            
            if st.button("📨 Send OTP", key="send_otp", use_container_width=True, type="primary"):
                if not phone:
                    st.error("❌ Enter phone number!")
                elif not is_valid_phone(phone):
                    st.error("❌ Invalid phone number!")
                else:
                    otp = generate_otp()
                    st.session_state.current_otp = otp
                    st.session_state.phone_for_otp = phone
                    st.session_state.otp_sent = True
                    st.success(f"📱 OTP sent to {phone}! (Demo OTP: {otp})")
                    st.rerun()
        else:
            st.markdown(f"**🔐 Enter OTP sent to {st.session_state.phone_for_otp}**")
            
            otp_input = st.text_input("OTP", placeholder="Enter 6-digit OTP", key="otp_input", max_chars=6)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button("✅ Verify", key="verify_otp", use_container_width=True, type="primary"):
                    if otp_input == st.session_state.current_otp:
                        name = USER_DB["phones"].get(st.session_state.phone_for_otp, {}).get("name", "Phone User")
                        st.session_state.authenticated = True
                        st.session_state.username = name
                        st.session_state.show_login_modal = False
                        st.success(f"✅ Welcome, {name}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid OTP!")
            
            with col2:
                if st.button("🔄 Resend", key="resend_otp", use_container_width=True):
                    new_otp = generate_otp()
                    st.session_state.current_otp = new_otp
                    st.info(f"📨 New OTP: {new_otp}")
    
    # Close button
    st.markdown("---")
    if st.button("❌ Close", key="close_auth", use_container_width=True):
        st.session_state.show_login_modal = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# HEADER - Centered title with larger size
if st.session_state.authenticated:
    left_section = '<div style="width: 40px; display: flex; align-items: center;"><span style="color: #a0aec0; cursor: pointer;">☰</span></div>'
    title_section = f'<div style="font-size: 1.4em; font-weight: 700; color: #10a37f; text-align: center; flex: 1;">🎓 DIET Career Buddy</div>'
    user_display = f'''<div style="color: #a0aec0; font-size: 14px; width: 200px; text-align: right; cursor: pointer;">
        <span style="background: #10a37f; color: white; border-radius: 50%; width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; margin-right: 8px;">{st.session_state.username[0].upper()}</span>
        <span onclick="document.getElementById('user-menu-btn').click()">{st.session_state.username}</span>
    </div>'''
else:
    left_section = '<div style="width: 40px;"></div>'
    title_section = f'<div style="font-size: 1.4em; font-weight: 700; color: #10a37f; text-align: center; flex: 1;">🎓 DIET Career Buddy</div>'
    user_display = '''<div style="width: 200px; text-align: right;">
        <button onclick="document.getElementById('login-trigger-btn').click()" style="background: #10a37f; color: white; border: none; padding: 10px 18px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 14px;">Sign In</button>
    </div>'''

st.markdown(f"""
<div style="
    position: fixed; 
    top: 0; 
    left: 0; 
    right: 0; 
    height: 55px; 
    background: #212121; 
    border-bottom: 1px solid #444; 
    display: flex; 
    align-items: center; 
    padding: 0 20px; 
    z-index: 1000;
">
    {left_section}
    {title_section}
    {user_display}
</div>
""", unsafe_allow_html=True)

# MAIN CONTENT
st.markdown('<div style="margin-top: 60px;">', unsafe_allow_html=True)

# Hidden trigger buttons
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Login Trigger", key="login-trigger-btn"):
        st.session_state.show_login_modal = True
        st.rerun()

with col2:
    if st.button("User Menu", key="user-menu-btn"):
        if st.session_state.authenticated:
            if st.button("🚪 Sign Out", key="logout_btn"):
                st.session_state.authenticated = False
                st.session_state.username = ""
                st.session_state.page = 'home'
                st.session_state.show_login_modal = False
                st.rerun()

# Show professional login modal
if st.session_state.show_login_modal and not st.session_state.authenticated:
    show_professional_login()
    st.stop()

# Dashboard Routing (your existing code)
if st.session_state.page == 'tech':
    tech_dashboard.show()
    if st.button("🏠 Back to Home", key="back_tech"):
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'salary':
    salary_dashboard.show()
    if st.button("🏠 Back to Home", key="back_salary"):
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'learn':
    learning_dashboard.show()
    if st.button("🏠 Back to Home", key="back_learn"):
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'diet':
    diet_guide.show()
    if st.button("🏠 Back to Home", key="back_diet"):
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'interview':
    interview_prep.show()
    if st.button("🏠 Back to Home", key="back_interview"):
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'jobs':
    jobs_dashboard.show()
    if st.button("🏠 Back to Home", key="back_jobs"):
        st.session_state.page = 'home'
        st.rerun()

else:
    # HOME PAGE (your existing code)
    welcome_text = f"Welcome back, {st.session_state.username}!" if st.session_state.authenticated else "Welcome to DIET Career Buddy!"
    
    st.markdown(f"## 🎓 **{welcome_text}**")
    st.markdown("### *Your AI-Powered Career Assistant with Real-Time Data*")
    
    if not st.session_state.authenticated:
        st.info("💡 **Sign in to unlock personalized dashboards and save your progress!**")
    
    # Navigation Buttons (your existing code)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("💻\nTech\nCareers", key="tech"):
            if st.session_state.authenticated:
                st.session_state.page = 'tech'
                st.rerun()
            else:
                st.session_state.show_login_modal = True
                st.rerun()

    with col2:
        if st.button("💰\nLive\nSalary", key="salary"):
            if st.session_state.authenticated:
                st.session_state.page = 'salary'
                st.rerun()
            else:
                st.session_state.show_login_modal = True
                st.rerun()

    with col3:
        if st.button("📚\nLearning\nPaths", key="learn"):
            if st.session_state.authenticated:
                st.session_state.page = 'learn'
                st.rerun()
            else:
                st.session_state.show_login_modal = True
                st.rerun()

    with col4:
        if st.button("🎓\nDIET\nGuide", key="diet"):
            if st.session_state.authenticated:
                st.session_state.page = 'diet'
                st.rerun()
            else:
                st.session_state.show_login_modal = True
                st.rerun()

    with col5:
        if st.button("🎯\nInterview\nPrep", key="interview"):
            if st.session_state.authenticated:
                st.session_state.page = 'interview'
                st.rerun()
            else:
                st.session_state.show_login_modal = True
                st.rerun()

    with col6:
        if st.button("📊\nLive\nJobs", key="jobs"):
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
    
    # Chat Section (your existing code)
    st.markdown("### 💬 **Ask Your Career Questions!**")
    
    col_input, col_button = st.columns([4, 1])
    
    with col_input:
        placeholder = f"Hi {st.session_state.username}, what would you like to know?" if st.session_state.authenticated else "What would you like to know about careers?"
        user_input = st.text_area("💭", 
                                 placeholder=placeholder + "\ne.g., What skills do I need for data science?",
                                 height=100,
                                 key="career_question_input")
    
    with col_button:
        st.markdown("<br>", unsafe_allow_html=True)
        send_clicked = st.button("🚀 Send", 
                                key="send_question", 
                                use_container_width=True,
                                type="primary")
    
    if send_clicked and user_input.strip():
        response_prefix = f"Great question, {st.session_state.username}! " if st.session_state.authenticated else "Great question! "
        
        if not st.session_state.authenticated:
            response_prefix += "💡 Sign in to access detailed dashboards. Here's some guidance: "
        
        response = response_prefix + "🎓 Explore our dashboards above for detailed insights!"
        
        st.markdown(f"""
        <div class="dashboard-card">
            <strong>❓ You asked:</strong><br>
            <em>"{user_input}"</em><br><br>
            <strong>🎓 AI Assistant:</strong><br>
            {response}
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
