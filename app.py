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
    # Home Page - Complete with Enhanced Chat
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
    
    # ENHANCED CHAT SECTION - With Send Button & Larger Input
    st.markdown("### 💬 **Ask Your Career Questions!**")
    
    # Create columns for input and button
    col_input, col_button = st.columns([4, 1])
    
    with col_input:
        user_input = st.text_area("💭 What would you like to know about your career?", 
                                 placeholder="e.g., What skills do I need for data science?\nWhat companies hire from DIET?\nHow much salary can I expect?",
                                 height=100,
                                 key="career_question_input")
    
    with col_button:
        # Add some spacing to align with text area
        st.markdown("<br>", unsafe_allow_html=True)
        send_clicked = st.button("🚀 Send", 
                                key="send_question", 
                                help="Click to get AI-powered career advice",
                                use_container_width=True,
                                type="primary")
    
    # Process the question when Send is clicked
    if send_clicked and user_input.strip():
        response = "Excellent question! "
        
        if any(word in user_input.lower() for word in ['salary', 'pay', 'money', 'package', 'compensation']):
            response += "💰 Check the **Live Salary** dashboard for comprehensive market-adjusted salary data with real-time market intelligence!"
        elif any(word in user_input.lower() for word in ['job', 'hiring', 'market', 'companies', 'openings']):
            response += "📊 Visit the **Live Jobs** dashboard for real-time market insights and hiring trends!"
        elif any(word in user_input.lower() for word in ['learn', 'skill', 'course', 'study', 'roadmap', 'path']):
            response += "📚 Explore the **Learning Paths** dashboard for detailed roadmaps and interactive progress tracking!"
        elif any(word in user_input.lower() for word in ['tech', 'technology', 'career', 'software', 'developer']):
            response += "💻 Check the **Tech Careers** dashboard for comprehensive career guidance and market trends!"
        elif any(word in user_input.lower() for word in ['interview', 'preparation', 'prep', 'coding', 'questions']):
            response += "🎯 Check the **Interview Prep** dashboard for preparation tips, practice tracking, and company-specific guides!"
        elif any(word in user_input.lower() for word in ['diet', 'college', 'placement', 'campus']):
            response += "🎓 Visit the **DIET Guide** dashboard for college-specific placement guidance and company insights!"
        else:
            response += "🎓 Click any dashboard button above for detailed insights and interactive tools tailored to your career journey!"
        
        st.markdown(f"""
        <div class="dashboard-card">
            <strong>❓ You asked:</strong><br>
            <em>"{user_input}"</em><br><br>
            <strong>🎓 AI Assistant:</strong><br>
            {response}
        </div>
        """, unsafe_allow_html=True)
    
    elif send_clicked and not user_input.strip():
        st.warning("💭 Please enter your career question first!")
