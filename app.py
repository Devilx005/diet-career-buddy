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

# Session State
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# User Database
USER_DB = {
    "emails": {
        "demo@gmail.com": {"password": "demo123", "name": "Demo User"},
        "student@diet.ac.in": {"password": "student123", "name": "DIET Student"},
        "admin@diet.com": {"password": "admin123", "name": "Admin User"}
    }
}

# HEADER with THE ONLY LOGIN BUTTON
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
    # THE ONLY LOGIN BUTTON - uses checkbox hack for functionality
    user_display = '''<div style="width: 200px; text-align: right;">
        <label for="login-trigger" style="background: #10a37f; color: white; border: none; padding: 10px 18px; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 14px; transition: all 0.3s ease; display: inline-block;">Login</label>
        <input type="checkbox" id="login-trigger" style="display: none;">
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

# CSS and JavaScript to make THE ONLY LOGIN BUTTON work
st.markdown("""
<style>
    .auth-modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.85);
        display: none;
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
    
    .auth-input {
        width: calc(100% - 24px);
        padding: 12px;
        border: 1px solid #555;
        border-radius: 8px;
        background: #2d2d2d;
        color: white;
        font-size: 14px;
        margin-bottom: 15px;
    }
    
    .auth-input:focus {
        border-color: #10a37f;
        outline: none;
        box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.2);
    }
    
    .auth-button {
        width: 100%;
        padding: 12px;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-bottom: 10px;
    }
    
    .primary-btn {
        background: #10a37f;
        color: white;
    }
    
    .primary-btn:hover {
        background: #0d8f6b;
        transform: translateY(-1px);
    }
    
    .secondary-btn {
        background: #333;
        color: white;
        border: 1px solid #555;
    }
    
    .secondary-btn:hover {
        background: #444;
        border-color: #10a37f;
    }
    
    .google-btn {
        background: #4285f4;
        color: white;
    }
    
    .google-btn:hover {
        background: #3367d6;
    }
</style>

<script>
// Handle login button click
document.addEventListener('DOMContentLoaded', function() {
    const loginTrigger = document.getElementById('login-trigger');
    const modal = document.querySelector('.auth-modal');
    
    if (loginTrigger) {
        loginTrigger.addEventListener('change', function() {
            if (this.checked) {
                modal.style.display = 'flex';
            }
        });
    }
});

function closeModal() {
    document.getElementById('login-trigger').checked = false;
    document.querySelector('.auth-modal').style.display = 'none';
}

function doLogin() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    if (!email || !password) {
        alert('❌ Please fill in all fields!');
        return;
    }
    
    // Check credentials
    const validCredentials = {
        'demo@gmail.com': { password: 'demo123', name: 'Demo User' },
        'student@diet.ac.in': { password: 'student123', name: 'DIET Student' },
        'admin@diet.com': { password: 'admin123', name: 'Admin User' }
    };
    
    if (validCredentials[email] && validCredentials[email].password === password) {
        // Store login state
        sessionStorage.setItem('authenticated', 'true');
        sessionStorage.setItem('username', validCredentials[email].name);
        alert('✅ Login successful!');
        location.reload();
    } else {
        alert('❌ Invalid credentials!\\n\\nTry:\\ndemo@gmail.com / demo123\\nstudent@diet.ac.in / student123\\nadmin@diet.com / admin123');
    }
}

function demoLogin() {
    sessionStorage.setItem('authenticated', 'true');
    sessionStorage.setItem('username', 'Demo User');
    alert('✅ Demo access granted!');
    location.reload();
}

function googleLogin() {
    sessionStorage.setItem('authenticated', 'true');
    sessionStorage.setItem('username', 'Google User');
    alert('✅ Signed in with Google!');
    location.reload();
}

function logout() {
    if (confirm('Sign out?')) {
        sessionStorage.removeItem('authenticated');
        sessionStorage.removeItem('username');
        location.reload();
    }
}

// Check if user is logged in on page load
window.addEventListener('load', function() {
    if (sessionStorage.getItem('authenticated') === 'true') {
        // User is logged in - this will be handled by Streamlit session state
    }
});
</script>

<!-- THE LOGIN MODAL (triggered by THE ONLY LOGIN BUTTON) -->
<div class="auth-modal">
    <div class="auth-container">
        <div style="text-align: center; margin-bottom: 30px;">
            <div style="font-size: 1.8em; font-weight: 700; color: #10a37f; margin-bottom: 8px;">Welcome Back!</div>
            <div style="color: #a0aec0; font-size: 0.95em;">Sign in to access your personalized career dashboard</div>
        </div>
        
        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 6px; color: #a0aec0; font-size: 0.9em; font-weight: 500;">Email</label>
            <input type="email" id="login-email" placeholder="Enter your email address" class="auth-input">
        </div>
        
        <div style="margin-bottom: 25px;">
            <label style="display: block; margin-bottom: 6px; color: #a0aec0; font-size: 0.9em; font-weight: 500;">Password</label>
            <input type="password" id="login-password" placeholder="Enter your password" class="auth-input">
        </div>
        
        <button onclick="doLogin()" class="auth-button primary-btn">🚀 Login</button>
        
        <div style="text-align: center; margin: 20px 0; color: #666; font-size: 0.85em;">
            <div style="position: relative;">
                <div style="position: absolute; top: 50%; left: 0; right: 0; height: 1px; background: #444;"></div>
                <span style="background: #1a1a1a; padding: 0 15px;">Or continue with</span>
            </div>
        </div>
        
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <button onclick="demoLogin()" class="auth-button secondary-btn" style="flex: 1;">🎯 Demo Access</button>
            <button onclick="googleLogin()" class="auth-button google-btn" style="flex: 1;">🌐 Google</button>
        </div>
        
        <button onclick="closeModal()" class="auth-button secondary-btn" style="background: transparent; color: #666; border: 1px solid #444;">❌ Close</button>
        
        <div style="text-align: center; margin-top: 20px; padding-top: 15px; border-top: 1px solid #333; color: #666; font-size: 0.85em;">
            <strong>Demo Credentials:</strong><br>
            📧 demo@gmail.com / demo123<br>
            🎓 student@diet.ac.in / student123<br>
            👨‍💼 admin@diet.com / admin123
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Check session storage for authentication
st.markdown("""
<script>
if (sessionStorage.getItem('authenticated') === 'true') {
    const username = sessionStorage.getItem('username');
    if (username) {
        // Set Streamlit session state via URL parameter
        if (!window.location.href.includes('?authenticated=true')) {
            window.location.href = window.location.href + '?authenticated=true&username=' + encodeURIComponent(username);
        }
    }
}
</script>
""", unsafe_allow_html=True)

# Handle authentication from URL parameters
if st.query_params.get("authenticated") == "true":
    username = st.query_params.get("username", "User")
    st.session_state.authenticated = True
    st.session_state.username = username
    st.query_params.clear()
    st.rerun()

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
                st.info("Please login to access dashboards")

    with col2:
        if st.button("💰\nLive\nSalary", key="salary"):
            if st.session_state.authenticated:
                st.session_state.page = 'salary'
                st.rerun()
            else:
                st.info("Please login to access dashboards")

    with col3:
        if st.button("📚\nLearning\nPaths", key="learn"):
            if st.session_state.authenticated:
                st.session_state.page = 'learn'
                st.rerun()
            else:
                st.info("Please login to access dashboards")

    with col4:
        if st.button("🎓\nDIET\nGuide", key="diet"):
            if st.session_state.authenticated:
                st.session_state.page = 'diet'
                st.rerun()
            else:
                st.info("Please login to access dashboards")

    with col5:
        if st.button("🎯\nInterview\nPrep", key="interview"):
            if st.session_state.authenticated:
                st.session_state.page = 'interview'
                st.rerun()
            else:
                st.info("Please login to access dashboards")

    with col6:
        if st.button("📊\nLive\nJobs", key="jobs"):
            if st.session_state.authenticated:
                st.session_state.page = 'jobs'
                st.rerun()
            else:
                st.info("Please login to access dashboards")
    
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
