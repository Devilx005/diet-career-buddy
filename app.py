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

# Header
st.markdown('<div class="header">🎓 DIET Career Buddy - Enhanced Edition</div>', unsafe_allow_html=True)

# Navigation Buttons
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("💻\nTech\nCareers", key="tech"):
        st.session_state.page = 'tech'
        st.rerun()

with col2:
    if st.button("💰\nLive\nSalary", key="salary"):
        st.session_state.page = 'salary'
        st.rerun()

with col3:
    if st.button("📚\nLearning\nPaths", key="learn"):
        st.session_state.page = 'learn'
        st.rerun()

with col4:
    if st.button("🎓\nDIET\nGuide", key="diet"):
        st.session_state.page = 'diet'
        st.rerun()

with col5:
    if st.button("🎯\nInterview\nPrep", key="interview"):
        st.session_state.page = 'interview'
        st.rerun()

with col6:
    if st.button("📊\nLive\nJobs", key="jobs"):
        st.session_state.page = 'jobs'
        st.rerun()

# Simple Routing
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
    # Home Page - COMPLETE with missing chat feature
    st.markdown("## 🎓 **Welcome to DIET Career Buddy!**")
    st.markdown("### *Your AI-Powered Career Assistant with Real-Time Data*")
    
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
    
    # MISSING FEATURE RESTORED - Interactive Chat Section
    st.markdown("### 💬 **Ask Your Career Questions!**")
    user_input = st.text_input("💭 What would you like to know about your career?", 
                              placeholder="e.g., What skills do I need for data science?")
    
    if user_input:
        response = "Excellent question! "
        
        if any(word in user_input.lower() for word in ['salary', 'pay', 'money']):
            response += "💰 Check the **Live Salary** dashboard for comprehensive market-adjusted salary data!"
        elif any(word in user_input.lower() for word in ['job', 'hiring', 'market']):
            response += "📊 Visit the **Live Jobs** dashboard for real-time market insights!"
        elif any(word in user_input.lower() for word in ['learn', 'skill', 'course', 'study']):
            response += "📚 Explore the **Learning Paths** dashboard for detailed roadmaps and progress tracking!"
        elif any(word in user_input.lower() for word in ['tech', 'technology', 'career']):
            response += "💻 Check the **Tech Careers** dashboard for comprehensive career guidance and market trends!"
        elif any(word in user_input.lower() for word in ['interview', 'preparation', 'prep']):
            response += "🎯 Check the **Interview Prep** dashboard for preparation tips and practice tracking!"
        elif any(word in user_input.lower() for word in ['diet', 'college', 'placement']):
            response += "🎓 Visit the **DIET Guide** dashboard for college-specific placement guidance!"
        else:
            response += "🎓 Click any dashboard button above for detailed insights and interactive tools!"
        
        st.markdown(f"""
        <div class="dashboard-card">
            <strong>You asked:</strong> {user_input}<br><br>
            <strong>🎓 Assistant:</strong> {response}
        </div>
        """, unsafe_allow_html=True)
