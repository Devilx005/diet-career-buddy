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

# Session State
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'show_login_modal' not in st.session_state:
    st.session_state.show_login_modal = False

# User database
USERS = {"student": "password123", "demo": "demo123", "admin": "admin123", "diet": "diet2025"}

def authenticate_user(username, password):
    return username in USERS and USERS[username] == password

# HEADER - Clean with proper hamburger positioning
if st.session_state.authenticated:
    header_text = f"☰ 🎓 DIET Career Buddy"
    user_display = f'<div style="color: #a0aec0; font-size: 14px;"><span style="background: #10a37f; color: white; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; margin-right: 8px;">{st.session_state.username[0].upper()}</span>{st.session_state.username}</div>'
    right_section = user_display
else:
    header_text = "🎓 DIET Career Buddy"
    right_section = '<button onclick="window.showLogin=true" style="background: #10a37f; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 14px;">Log in</button>'

st.markdown(f"""
<div style="position: fixed; top: 0; left: 0; right: 0; height: 50px; background: #212121; border-bottom: 1px solid #444; display: flex; justify-content: space-between; align-items: center; padding: 0 20px; z-index: 1000;">
    <div style="font-size: 1.1em; font-weight: 600; color: #10a37f;">{header_text}</div>
    <div>{right_section}</div>
</div>
""", unsafe_allow_html=True)

# MAIN CONTENT - Moved closer to title bar (reduced margin)
st.markdown('<div style="margin-top: 10px;">', unsafe_allow_html=True)

# Simple login handling through URL parameters or session
if not st.session_state.authenticated:
    # Check if login button was clicked (simple approach)
    if st.query_params.get("login") == "1" or st.session_state.show_login_modal:
        st.session_state.show_login_modal = True
        
        st.markdown("### 🔐 Login to Continue")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("Username", placeholder="Enter username", key="user_input")
            password = st.text_input("Password", type="password", placeholder="Enter password", key="pass_input")
            
            col_login, col_demo, col_close = st.columns(3)
            
            with col_login:
                if st.button("🚀 Login", use_container_width=True, type="primary"):
                    if authenticate_user(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.show_login_modal = False
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials!")
            
            with col_demo:
                if st.button("🎯 Demo", use_container_width=True):
                    st.session_state.authenticated = True
                    st.session_state.username = "Demo User"
                    st.session_state.show_login_modal = False
                    st.rerun()
            
            with col_close:
                if st.button("❌ Close", use_container_width=True):
                    st.session_state.show_login_modal = False
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()  # Stop here to show only login

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

# Add invisible logout button for logged in users
if st.session_state.authenticated:
    # Use CSS to hide this button completely
    st.markdown('<div style="display: none;">', unsafe_allow_html=True)
    if st.button("Logout", key="logout_invisible"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.page = 'home'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# JavaScript to handle login button click
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Handle login button clicks
    const loginBtns = document.querySelectorAll('button');
    loginBtns.forEach(btn => {
        if (btn.textContent === 'Log in') {
            btn.addEventListener('click', function() {
                window.location.href = window.location.href + (window.location.href.includes('?') ? '&' : '?') + 'login=1';
            });
        }
    });
});
</script>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
