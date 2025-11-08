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
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# IMPROVED HEADER WITH LOGIN IN RIGHT CORNER
if st.session_state.logged_in:
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
        <div style="text-align: right; display: flex; align-items: center; gap: 10px;">
            <span style="color: #a0aec0; font-size: 14px;">👋 {st.session_state.username}</span>
            <a href="?logout=true" style="
                color: #ff6b6b;
                text-decoration: none;
                font-size: 14px;
                padding: 6px 12px;
                border: 1px solid #ff6b6b;
                border-radius: 6px;
                transition: all 0.3s ease;
            " onmouseover="this.style.background='#ff6b6b'; this.style.color='white';" 
               onmouseout="this.style.background='transparent'; this.style.color='#ff6b6b';">
                Logout
            </a>
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
        <div style="text-align: right;">
            <a href="?login=true" style="
                background: rgba(16, 163, 127, 0.8);
                color: white;
                text-decoration: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
                display: inline-block;
                transition: all 0.3s ease;
            " onmouseover="this.style.background='#10a37f'; this.style.transform='scale(1.05)';" 
               onmouseout="this.style.background='rgba(16, 163, 127, 0.8)'; this.style.transform='scale(1)';">
                🔐 Login
            </a>
        </div>
    </div>
    '''

st.markdown(header_html, unsafe_allow_html=True)

# Handle logout
if st.query_params.get('logout') == 'true':
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.query_params.clear()
    st.rerun()

# Handle login trigger
show_login = st.query_params.get('login') == 'true'

# MAIN CONTENT
st.markdown('<div style="margin-top: 60px;">', unsafe_allow_html=True)

# IMPROVED LOGIN MODAL
if show_login and not st.session_state.logged_in:
    st.markdown("""
    <style>
    .login-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        z-index: 2000;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .login-modal {
        background: #1e1e1e;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        max-width: 400px;
        width: 90%;
    }
    </style>
    <div class="login-overlay"></div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔐 Login to DIET Career Buddy")
    st.info("💡 Login is optional - all features are accessible without login!")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
        with col2:
            if st.form_submit_button("❌ Cancel", use_container_width=True):
                st.query_params.clear()
                st.rerun()
        
        if submit:
            if username == "admin" and password == "password":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.query_params.clear()
                st.success("✅ Login successful!")
                st.rerun()
            elif username and password:
                st.error("❌ Invalid credentials!")
            else:
                st.error("❌ Please enter username and password!")
    
    st.info("**Demo Credentials:** username: `admin` | password: `password`")
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
    if st.session_state.logged_in:
        st.markdown(f"## 🎓 Welcome back, **{st.session_state.username}**!")
    else:
        st.markdown("## 🎓 Welcome to DIET Career Buddy!")
    
    st.markdown("### *Your AI-Powered Career Assistant with Real-Time Data*")
    
    if not st.session_state.logged_in:
        st.info("💡 All features are accessible! Login is optional for a personalized experience.")
    
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
        • <strong>Market Intelligence:</strong> AI-powered career insights<br><br>
        <strong>✨ All features unlocked for everyone!</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat Section
    st.markdown("### 💬 Ask Your Career Questions!")
    
    col_input, col_button = st.columns([4, 1])
    
    with col_input:
        if st.session_state.logged_in:
            placeholder = f"Hi {st.session_state.username}, what would you like to know?\ne.g., What skills do I need for data science?"
        else:
            placeholder = "What would you like to know about careers?\ne.g., What skills do I need for data science?"
        
        user_input = st.text_area("💭", 
                                 placeholder=placeholder,
                                 height=100,
                                 key="career_question_input")
    
    with col_button:
        st.markdown("<br>", unsafe_allow_html=True)
        send_clicked = st.button("🚀 Send", 
                                key="send_question", 
                                use_container_width=True,
                                type="primary")
    
    if send_clicked and user_input.strip():
        if st.session_state.logged_in:
            response = f"Great question, {st.session_state.username}! 🎓 Explore our dashboards above for detailed insights!"
        else:
            response = "Great question! 🎓 Explore our dashboards above for detailed insights!"
        
        st.markdown(f"""
        <div class="dashboard-card">
            <strong>❓ You asked:</strong><br>
            <em>"{user_input}"</em><br><br>
            <strong>🎓 AI Assistant:</strong><br>
            {response}
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
