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

# Enhanced Auth CSS
st.markdown("""
<style>
    .auth-modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.85);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2000;
        backdrop-filter: blur(5px);
    }
    
    .auth-container {
        max-width: 420px;
        width: 90%;
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        border-radius: 16px;
        border: 2px solid #10a37f;
        box-shadow: 0 25px 80px rgba(16, 163, 127, 0.3);
        padding: 40px 30px;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .auth-header {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .auth-title {
        font-size: 1.8em;
        font-weight: 700;
        color: #10a37f;
        margin-bottom: 8px;
    }
    
    .auth-subtitle {
        color: #a0aec0;
        font-size: 0.95em;
    }
    
    .divider {
        text-align: center;
        margin: 25px 0;
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
        background: linear-gradient(90deg, transparent, #444, transparent);
    }
    
    .divider span {
        background: #1a1a1a;
        padding: 0 15px;
    }
    
    .signup-link {
        text-align: center;
        margin-top: 25px;
        padding-top: 20px;
        border-top: 1px solid #333;
        color: #a0aec0;
        font-size: 0.9em;
    }
    
    .signup-link a {
        color: #10a37f;
        text-decoration: none;
        font-weight: 600;
        cursor: pointer;
    }
    
    .signup-link a:hover {
        text-decoration: underline;
    }

    /* Hide trigger buttons completely */
    button[title="Login trigger"], 
    button[title="Logout trigger"] {
        display: none !important;
        visibility: hidden !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
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
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'

# Enhanced User Database
USER_DB = {
    "emails": {
        "demo@gmail.com": {"password": "demo123", "name": "Demo User"},
        "student@diet.ac.in": {"password": "student123", "name": "DIET Student"},
        "admin@diet.com": {"password": "admin123", "name": "Admin User"}
    }
}

def authenticate_email(email, password):
    if email in USER_DB["emails"]:
        return USER_DB["emails"][email]["password"] == password, USER_DB["emails"][email]["name"]
    return False, None

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def show_login_modal():
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
    
    # Login/Signup Toggle
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", key="login_tab", use_container_width=True,
                    type="primary" if st.session_state.auth_mode == 'login' else "secondary"):
            st.session_state.auth_mode = 'login'
            st.rerun()
    
    with col2:
        if st.button("Sign Up", key="signup_tab", use_container_width=True,
                    type="primary" if st.session_state.auth_mode == 'signup' else "secondary"):
            st.session_state.auth_mode = 'signup'
            st.rerun()
    
    # OAuth Section
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌐 Continue with Google", key="google_login", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.username = "Google User"
            st.session_state.show_login_modal = False
            st.success("✅ Signed in with Google!")
            st.rerun()
    
    with col2:
        if st.button("🎯 Demo Access", key="demo_access", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.username = "Demo User"
            st.session_state.show_login_modal = False
            st.success("✅ Demo access granted!")
            st.rerun()
    
    st.markdown('<div class="divider"><span>Or with email</span></div>', unsafe_allow_html=True)
    
    # Main Auth Form
    if st.session_state.auth_mode == 'login':
        # LOGIN FORM
        st.markdown("### 📧 Login")
        
        email = st.text_input("Email", placeholder="Enter your email address", key="login_email")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        # Remember me and forgot password
        col1, col2 = st.columns([1, 1])
        with col1:
            remember_me = st.checkbox("Remember me", key="remember")
        with col2:
            if st.button("Forgot password?", key="forgot_pass"):
                st.info("🔄 Password reset link sent to your email!")
        
        # Login button
        if st.button("🚀 Login", key="login_submit", use_container_width=True, type="primary"):
            if not email or not password:
                st.error("❌ Please fill in all fields!")
            elif not is_valid_email(email):
                st.error("❌ Please enter a valid email address!")
            else:
                success, name = authenticate_email(email, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.username = name
                    st.session_state.show_login_modal = False
                    st.success(f"✅ Welcome back, {name}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password!")
        
        # Sign up link
        st.markdown("""
        <div class="signup-link">
            Don't have an account? <a href="#" onclick="document.getElementById('signup_tab').click()">Sign up</a>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # SIGNUP FORM
        st.markdown("### 📝 Create Account")
        
        name = st.text_input("Full Name", placeholder="Enter your full name", key="signup_name")
        email = st.text_input("Email", placeholder="Enter your email address", key="signup_email")
        password = st.text_input("Password", type="password", placeholder="Create a password (min 8 chars)", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="confirm_password")
        
        # Terms and conditions
        terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy", key="terms")
        
        # Sign up button
        if st.button("🎯 Create Account", key="signup_submit", use_container_width=True, type="primary"):
            if not all([name, email, password, confirm_password]):
                st.error("❌ Please fill in all fields!")
            elif not is_valid_email(email):
                st.error("❌ Please enter a valid email address!")
            elif len(password) < 8:
                st.error("❌ Password must be at least 8 characters!")
            elif password != confirm_password:
                st.error("❌ Passwords do not match!")
            elif not terms_accepted:
                st.error("❌ Please accept the terms and conditions!")
            elif email in USER_DB["emails"]:
                st.error("❌ Email already registered! Try signing in instead.")
            else:
                # Register new user
                USER_DB["emails"][email] = {"password": password, "name": name}
                st.success("✅ Account created successfully! Please sign in.")
                st.session_state.auth_mode = 'login'
                st.rerun()
        
        # Sign in link
        st.markdown("""
        <div class="signup-link">
            Already have an account? <a href="#" onclick="document.getElementById('login_tab').click()">Sign in</a>
        </div>
        """, unsafe_allow_html=True)
    
    # Close button
    st.markdown("---")
    if st.button("❌ Close", key="close_modal", use_container_width=True):
        st.session_state.show_login_modal = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# HEADER with DIRECTLY FUNCTIONAL Login Button
if st.session_state.authenticated:
    left_section = '<div style="width: 40px; display: flex; align-items: center;"><span style="color: #a0aec0; cursor: pointer;">☰</span></div>'
    title_section = f'<div style="font-size: 1.4em; font-weight: 700; color: #10a37f; text-align: center; flex: 1;">🎓 DIET Career Buddy</div>'
    user_display = f'''<div style="color: #a0aec0; font-size: 14px; width: 200px; text-align: right; cursor: pointer;" onclick="logout()">
        <span style="background: #10a37f; color: white; border-radius: 50%; width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; margin-right: 8px;">{st.session_state.username[0].upper()}</span>
        {st.session_state.username}
    </div>'''
else:
    left_section = '<div style="width: 40px;"></div>'
    title_section = f'<div style="font-size: 1.4em; font-weight: 700; color: #10a37f; text-align: center; flex: 1;">🎓 DIET Career Buddy</div>'
    user_display = '''<div style="width: 200px; text-align: right;">
        <button onclick="openLogin()" style="background: #10a37f; color: white; border: none; padding: 10px 18px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 14px; transition: all 0.3s ease;">Login</button>
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

# HIDDEN TRIGGER BUTTONS (completely invisible)
if st.button("🔓", key="header_login_trigger", help="Login trigger"):
    st.session_state.show_login_modal = True
    st.rerun()

if st.button("🚪", key="header_logout_trigger", help="Logout trigger"):
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.page = 'home'
    st.session_state.show_login_modal = False
    st.rerun()

# JavaScript to make the GREEN LOGIN BUTTON work
st.markdown("""
<script>
function openLogin() {
    // Find the hidden login trigger button
    const buttons = parent.document.querySelectorAll('button');
    buttons.forEach(btn => {
        if (btn.title === 'Login trigger') {
            btn.click();
        }
    });
}

function logout() {
    if (confirm('Sign out?')) {
        // Find the hidden logout trigger button
        const buttons = parent.document.querySelectorAll('button');
        buttons.forEach(btn => {
            if (btn.title === 'Logout trigger') {
                btn.click();
            }
        });
    }
}
</script>
""", unsafe_allow_html=True)

# Show login modal when triggered
if st.session_state.show_login_modal and not st.session_state.authenticated:
    show_login_modal()
    st.stop()

# Dashboard Routing
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
    # HOME PAGE
    welcome_text = f"Welcome back, {st.session_state.username}!" if st.session_state.authenticated else "Welcome to DIET Career Buddy!"
    
    st.markdown(f"## 🎓 **{welcome_text}**")
    st.markdown("### *Your AI-Powered Career Assistant with Real-Time Data*")
    
    if not st.session_state.authenticated:
        st.info("💡 **Sign in to unlock personalized dashboards and save your progress!**")
    
    # Navigation Buttons
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
    
    # Chat Section
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
