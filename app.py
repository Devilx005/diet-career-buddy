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
if 'show_login_modal' not in st.session_state:
    st.session_state.show_login_modal = False

# User Database
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

# Login Modal Function
def show_login_modal():
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
    </style>
    
    <div class="auth-modal">
        <div class="auth-container">
            <div style="text-align: center; margin-bottom: 30px;">
                <div style="font-size: 1.8em; font-weight: 700; color: #10a37f; margin-bottom: 8px;">Welcome Back!</div>
                <div style="color: #a0aec0; font-size: 0.95em;">Sign in to access your personalized career dashboard</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 Quick Login Options")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 Demo Access", key="demo_login", use_container_width=True, type="primary"):
            st.session_state.authenticated = True
            st.session_state.username = "Demo User"
            st.session_state.show_login_modal = False
            st.success("✅ Demo access granted!")
            st.rerun()
    
    with col2:
        if st.button("🌐 Google Login", key="google_login", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.username = "Google User"
            st.session_state.show_login_modal = False
            st.success("✅ Signed in with Google!")
            st.rerun()
    
    st.markdown("### 📧 Email Login")
    
    email = st.text_input("Email", placeholder="Enter your email address", key="login_email")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("🚀 Login", key="email_login", use_container_width=True, type="primary"):
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
    
    with col2:
        if st.button("❌ Close", key="close_login", use_container_width=True):
            st.session_state.show_login_modal = False
            st.rerun()
    
    st.markdown("""
    **Demo Credentials:**
    - 📧 demo@gmail.com / demo123
    - 🎓 student@diet.ac.in / student123
    - 👨‍💼 admin@diet.com / admin123
    """)

# HEADER WITH WORKING GREEN LOGIN BUTTON
if st.session_state.authenticated:
    header_html = f'''
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
        <div style="width: 40px; display: flex; align-items: center;"><span style="color: #a0aec0; cursor: pointer;">☰</span></div>
        <div style="font-size: 1.4em; font-weight: 700; color: #10a37f; text-align: center; flex: 1;">🎓 DIET Career Buddy</div>
        <div style="color: #a0aec0; font-size: 14px; width: 200px; text-align: right; cursor: pointer;" onclick="if(confirm('Sign out?')) window.location.reload()">
            <span style="background: #10a37f; color: white; border-radius: 50%; width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; margin-right: 8px;">{st.session_state.username[0].upper()}</span>
            {st.session_state.username}
        </div>
    </div>
    '''
else:
    header_html = '''
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
        <div style="width: 40px;"></div>
        <div style="font-size: 1.4em; font-weight: 700; color: #10a37f; text-align: center; flex: 1;">🎓 DIET Career Buddy</div>
        <div style="width: 200px; text-align: right;">
            <button id="headerLoginBtn" style="
                background: #10a37f !important;
                color: white !important;
                border: none !important;
                padding: 10px 18px !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
                cursor: pointer !important;
                font-size: 14px !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 2px 8px rgba(16, 163, 127, 0.3) !important;
            " onmouseover="this.style.background='#0d8f6b'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(16, 163, 127, 0.4)'" 
               onmouseout="this.style.background='#10a37f'; this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(16, 163, 127, 0.3)'">Login</button>
        </div>
    </div>
    '''

st.markdown(header_html, unsafe_allow_html=True)

# MAIN CONTENT
st.markdown('<div style="margin-top: 60px;">', unsafe_allow_html=True)

# COMPLETELY ISOLATED HIDDEN LOGIN TRIGGER
if not st.session_state.authenticated:
    # Create a completely separate container for the hidden trigger
    st.markdown('<div id="hidden-login-container" style="position: absolute; left: -9999px; top: -9999px; width: 1px; height: 1px; opacity: 0; visibility: hidden; pointer-events: none; z-index: -9999;"></div>', unsafe_allow_html=True)
    
    # Use expander to further isolate the button
    with st.expander("🔐", expanded=False):
        login_clicked = st.button("HIDDEN_LOGIN_TRIGGER_XYZ123", key="completely_isolated_login_btn_xyz789", help="Completely isolated login trigger")
        
        if login_clicked:
            st.session_state.show_login_modal = True
            st.rerun()
    
    # JavaScript to connect header button to isolated hidden button
    st.markdown("""
    <script>
    // Wait longer for page to fully load
    setTimeout(function() {
        const headerBtn = document.getElementById('headerLoginBtn');
        if (headerBtn) {
            // Completely replace the button to remove all event listeners
            const newBtn = headerBtn.cloneNode(true);
            headerBtn.parentNode.replaceChild(newBtn, headerBtn);
            
            newBtn.addEventListener('click', function(event) {
                // Completely prevent any default behavior
                event.preventDefault();
                event.stopImmediatePropagation();
                event.stopPropagation();
                
                // Find the isolated hidden button
                const allButtons = parent.document.querySelectorAll('button');
                let targetBtn = null;
                
                allButtons.forEach(btn => {
                    if (btn.textContent && (
                        btn.textContent.includes('HIDDEN_LOGIN_TRIGGER_XYZ123') ||
                        btn.getAttribute('data-testid') === 'completely_isolated_login_btn_xyz789'
                    )) {
                        targetBtn = btn;
                    }
                });
                
                if (targetBtn) {
                    // Trigger click on isolated button
                    targetBtn.click();
                } else {
                    console.log('Hidden login trigger not found');
                }
                
                return false;
            });
        }
    }, 2000);
    </script>
    
    <style>
    /* Completely hide all traces of the hidden login trigger */
    
    /* Hide by content */
    button:contains("HIDDEN_LOGIN_TRIGGER_XYZ123"),
    button[title*="isolated"],
    button[data-testid="completely_isolated_login_btn_xyz789"] {
        display: none !important;
        position: absolute !important;
        left: -99999px !important;
        top: -99999px !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
        visibility: hidden !important;
        pointer-events: none !important;
        z-index: -99999 !important;
        overflow: hidden !important;
    }
    
    /* Hide the expander containing the hidden button */
    details:has(button:contains("HIDDEN_LOGIN_TRIGGER_XYZ123")) {
        display: none !important;
        position: absolute !important;
        left: -99999px !important;
        top: -99999px !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
        visibility: hidden !important;
        pointer-events: none !important;
        z-index: -99999 !important;
        overflow: hidden !important;
    }
    
    /* Hide any container with the hidden button */
    .element-container:has(button:contains("HIDDEN_LOGIN_TRIGGER_XYZ123")),
    .streamlit-expanderHeader:contains("🔐"),
    .streamlit-expander:has(button:contains("HIDDEN_LOGIN_TRIGGER_XYZ123")) {
        display: none !important;
        position: absolute !important;
        left: -99999px !important;
        top: -99999px !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
        visibility: hidden !important;
        pointer-events: none !important;
        z-index: -99999 !important;
        overflow: hidden !important;
    }
    
    /* Ensure main login button stays visible */
    #headerLoginBtn {
        display: inline-block !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: static !important;
        pointer-events: auto !important;
        z-index: 1000 !important;
    }
    
    /* Hide expander with 🔐 icon */
    div[data-testid="stExpander"]:has(summary:contains("🔐")),
    details:has(summary:contains("🔐")) {
        display: none !important;
        position: absolute !important;
        left: -99999px !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    
    /* Additional nuclear option - hide anything with isolated keywords */
    *[class*="isolated"],
    *[id*="isolated"],
    *[data-testid*="isolated"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
    </style>
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
    
    # Navigation Buttons - FIXED TO EXCLUDE LOGIN BUTTON
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
