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


# Session State - MINIMAL ONLY + LOGIN FEATURE
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'show_login_form' not in st.session_state:
    st.session_state.show_login_form = False


# Optional Login Function
def show_login_form():
    st.markdown("### 🔑 **Optional Login**")
    st.info("💡 **Note:** Login is optional - you can close this and use all features without logging in!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        username = st.text_input("Username", placeholder="Enter username", key="opt_username")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="opt_password")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Login", key="opt_login_btn", use_container_width=True, type="primary"):
            if username == "admin" and password == "password":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.show_login_form = False
                st.success("✅ Login successful!")
                st.rerun()
            elif username and password:
                st.error("❌ Invalid credentials!")
            else:
                st.error("❌ Please enter username and password!")
        
        if st.button("❌ Close", key="close_login_btn", use_container_width=True):
            st.session_state.show_login_form = False
            st.rerun()
    
    st.info("**Demo Login:** username: `admin` | password: `password`")


# HEADER WITH LOGIN BUTTON IN RIGHT CORNER
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
        <div style="width: 200px; text-align: right; display: flex; align-items: center; justify-content: flex-end;">
            <span style="
                color: #a0aec0; 
                cursor: pointer; 
                font-size: 14px;
                background: rgba(16, 163, 127, 0.1);
                padding: 6px 12px;
                border-radius: 6px;
                border: 1px solid rgba(16, 163, 127, 0.3);
            " 
            onclick="if(confirm('Logout?')) window.location.reload()">
                👋 {st.session_state.username}
            </span>
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
        <div style="width: 200px; text-align: right; display: flex; align-items: center; justify-content: flex-end;">
            <button onclick="triggerLogin()" style="
                background: rgba(16, 163, 127, 0.8);
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                font-weight: 600;
                cursor: pointer;
                font-size: 13px;
            ">🔐 Login Trigger</button>
        </div>
    </div>
    
    <script>
    function triggerLogin() {
        const buttons = parent.document.querySelectorAll('button');
        buttons.forEach(btn => {
            if (btn.getAttribute('key') === 'working_login_trigger') {
                btn.click();
            }
        });
    }
    </script>
    '''


st.markdown(header_html, unsafe_allow_html=True)


# MAIN CONTENT
st.markdown('<div style="margin-top: 60px;">', unsafe_allow_html=True)


# WORKING LOGIN TRIGGER - HIDDEN BUT FUNCTIONAL
if not st.session_state.logged_in:
    if st.button("🔐 Login Trigger", key="working_login_trigger", help="working_login_trigger"):
        st.session_state.show_login_form = True
        st.rerun()
    
    st.markdown("""
    <style>
    button[key="working_login_trigger"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)


# Show optional login form when triggered
if st.session_state.show_login_form:
    show_login_form()
    st.stop()


# Dashboard Routing - WORKS FOR EVERYONE
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
    # HOME PAGE - WORKS FOR EVERYONE
    if st.session_state.logged_in:
        st.markdown(f"## 🎓 **Welcome back, {st.session_state.username}!**")
    else:
        st.markdown("## 🎓 **Welcome to DIET Career Buddy!**")
    
    st.markdown("### *Your AI-Powered Career Assistant with Real-Time Data*")
    
    if not st.session_state.logged_in:
        st.info("💡 **All features are accessible! Login is optional for a personalized experience.**")
    
    # Navigation Buttons - DIRECT ACCESS FOR EVERYONE
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
    st.markdown("### 💬 **Ask Your Career Questions!**")
    
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
