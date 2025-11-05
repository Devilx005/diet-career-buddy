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
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'show_login_form' not in st.session_state:
    st.session_state.show_login_form = False

# Simple Login Function
def show_login_form():
    st.markdown("### 🔑 **Login to Continue**")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        username = st.text_input("Username", placeholder="Enter username", key="simple_username")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="simple_password")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Login", key="simple_login_btn", use_container_width=True, type="primary"):
            # Simple username/password check
            if username == "admin" and password == "password":
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.show_login_form = False
                st.success("✅ Login successful!")
                st.rerun()
            elif username and password:
                st.error("❌ Invalid credentials!")
            else:
                st.error("❌ Please enter username and password!")
        
        if st.button("❌ Cancel", key="cancel_login_btn", use_container_width=True):
            st.session_state.show_login_form = False
            st.rerun()
    
    st.info("**Demo Login:** username: `admin` | password: `password`")

# HEADER WITH WORKING LOGIN BUTTON
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
        <div style="width: 40px; display: flex; align-items: center;">
            <span style="color: #a0aec0; cursor: pointer;">☰</span>
        </div>
        <div style="font-size: 1.4em; font-weight: 700; color: #10a37f; text-align: center; flex: 1;">
            🎓 DIET Career Buddy
        </div>
        <div style="width: 200px; text-align: right; color: #a0aec0; cursor: pointer;" 
             onclick="if(confirm('Logout?')) window.location.reload()">
            Welcome, {st.session_state.username}! (Click to logout)
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
        <div style="width: 40px; display: flex; align-items: center;">
            <span style="color: #a0aec0; cursor: pointer;">☰</span>
        </div>
        <div style="font-size: 1.4em; font-weight: 700; color: #10a37f; text-align: center; flex: 1;">
            🎓 DIET Career Buddy
        </div>
        <div style="width: 200px; text-align: right;">
            <button onclick="triggerLogin()" style="
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
            " 
            onmouseover="this.style.background='#0d8f6b'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(16, 163, 127, 0.4)'" 
            onmouseout="this.style.background='#10a37f'; this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(16, 163, 127, 0.3)'">
                Login
            </button>
        </div>
    </div>
    
    <script>
    function triggerLogin() {
        // Find and click the hidden Streamlit login trigger
        const buttons = parent.document.querySelectorAll('button');
        buttons.forEach(btn => {
            if (btn.getAttribute('data-testid') === 'trigger_login_form') {
                btn.click();
                return;
            }
        });
    }
    </script>
    '''

st.markdown(header_html, unsafe_allow_html=True)

# MAIN CONTENT
st.markdown('<div style="margin-top: 60px;">', unsafe_allow_html=True)

# Hidden login trigger button
if not st.session_state.authenticated:
    if st.button("🔐 Trigger Login", key="trigger_login", help="trigger_login_form"):
        st.session_state.show_login_form = True
        st.rerun()
    
    # Hide the trigger button with CSS
    st.markdown("""
    <style>
    button[title="trigger_login_form"] {
        display: none !important;
        position: absolute !important;
        left: -9999px !important;
        visibility: hidden !important;
    }
    
    .element-container:has(button[title="trigger_login_form"]) {
        display: none !important;
        position: absolute !important;
        left: -9999px !important;
        visibility: hidden !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Show login form when triggered
if st.session_state.show_login_form and not st.session_state.authenticated:
    show_login_form()
    st.stop()

# Dashboard Routing (only accessible after login)
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
    if st.session_state.authenticated:
        st.markdown(f"## 🎓 **Welcome back, {st.session_state.username}!**")
        st.markdown("### *Your AI-Powered Career Assistant with Real-Time Data*")
        
        # Navigation Buttons
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            if st.button("💻\nTech\nCareers", key="tech", use_container_width=True):
                st.session_state.page = 'tech'
                st.rerun()

        with col2:
            if st.button("💰\nLive\nSalary", key="salary", use_container_width=True):
                st.session_state.page = 'salary'
                st.rerun()

        with col3:
            if st.button("📚\nLearning\nPaths", key="learn", use_container_width=True):
                st.session_state.page = 'learn'
                st.rerun()

        with col4:
            if st.button("🎓\nDIET\nGuide", key="diet", use_container_width=True):
                st.session_state.page = 'diet'
                st.rerun()

        with col5:
            if st.button("🎯\nInterview\nPrep", key="interview", use_container_width=True):
                st.session_state.page = 'interview'
                st.rerun()

        with col6:
            if st.button("📊\nLive\nJobs", key="jobs", use_container_width=True):
                st.session_state.page = 'jobs'
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
            user_input = st.text_area("💭", 
                                     placeholder=f"Hi {st.session_state.username}, what would you like to know?\ne.g., What skills do I need for data science?",
                                     height=100,
                                     key="career_question_input")
        
        with col_button:
            st.markdown("<br>", unsafe_allow_html=True)
            send_clicked = st.button("🚀 Send", 
                                    key="send_question", 
                                    use_container_width=True,
                                    type="primary")
        
        if send_clicked and user_input.strip():
            st.markdown(f"""
            <div class="dashboard-card">
                <strong>❓ You asked:</strong><br>
                <em>"{user_input}"</em><br><br>
                <strong>🎓 AI Assistant:</strong><br>
                Great question, {st.session_state.username}! 🎓 Explore our dashboards above for detailed insights!
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # Welcome page for non-authenticated users
        st.markdown("## 🎓 **Welcome to DIET Career Buddy!**")
        st.markdown("### *Your AI-Powered Career Assistant with Real-Time Data*")
        
        st.info("💡 **Click the Login button in the top-right corner to access all features!**")
        
        st.markdown("""
        <div class="dashboard-card">
            <strong>🚀 What awaits you after login:</strong><br><br>
            • <strong>💻 Tech Careers:</strong> Explore programming roles and requirements<br>
            • <strong>💰 Live Salary Data:</strong> Real-time salary information<br>
            • <strong>📚 Learning Paths:</strong> Personalized skill development roadmaps<br>
            • <strong>🎓 DIET Guide:</strong> Institution-specific career guidance<br>
            • <strong>🎯 Interview Prep:</strong> Practice and preparation tools<br>
            • <strong>📊 Live Jobs:</strong> Current job market trends and openings
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
