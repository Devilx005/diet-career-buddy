import streamlit as st
from streamlit_chat import message
import json
from datetime import datetime
import pandas as pd

# Enhanced page configuration for ChatGPT-style deployment
st.set_page_config(
    page_title="🎓 DIET Career Buddy - ChatGPT Style", 
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ChatGPT-Style CSS and Mobile Interface
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {display: none;}
    .stMainBlockContainer {padding: 0 !important;}
    .main .block-container {padding: 0 !important; max-width: 100% !important;}
    section[data-testid="stSidebar"] {display: none;}
    
    /* ChatGPT-style color scheme */
    :root {
        --bg-primary: #212121;
        --bg-secondary: #303030;
        --bg-chat: #424242;
        --text-primary: #ffffff;
        --text-secondary: #b0b0b0;
        --accent: #10a37f;
        --accent-hover: #0d8f6b;
        --border: #4a4a4a;
    }
    
    /* Main layout */
    .chat-container {
        height: 100vh;
        display: flex;
        flex-direction: column;
        background: var(--bg-primary);
        color: var(--text-primary);
    }
    
    /* Header */
    .chat-header {
        background: var(--bg-secondary);
        padding: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid var(--border);
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .header-btn {
        background: transparent;
        border: none;
        color: var(--text-primary);
        font-size: 1.2rem;
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 0.5rem;
        transition: background 0.2s;
    }
    
    .header-btn:hover {
        background: rgba(255,255,255,0.1);
    }
    
    .app-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
    }
    
    /* Sidebar */
    .sidebar-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        z-index: 200;
        display: none;
    }
    
    .sidebar {
        position: fixed;
        top: 0;
        left: -320px;
        width: 300px;
        height: 100%;
        background: var(--bg-secondary);
        transition: left 0.3s ease;
        z-index: 300;
        display: flex;
        flex-direction: column;
        border-right: 1px solid var(--border);
    }
    
    .sidebar.open {
        left: 0;
    }
    
    .sidebar-header {
        padding: 1rem;
        border-bottom: 1px solid var(--border);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .sidebar-title {
        font-weight: 600;
        margin: 0;
    }
    
    .close-btn {
        background: transparent;
        border: none;
        color: var(--text-primary);
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0.25rem;
    }
    
    .sidebar-content {
        flex: 1;
        padding: 1rem;
        overflow-y: auto;
    }
    
    .new-chat-btn {
        background: var(--accent);
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        width: 100%;
        margin-bottom: 1.5rem;
        cursor: pointer;
        font-weight: 500;
        transition: background 0.2s;
    }
    
    .new-chat-btn:hover {
        background: var(--accent-hover);
    }
    
    .section-title {
        color: var(--text-secondary);
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        margin: 1.5rem 0 0.5rem 0;
        letter-spacing: 0.5px;
    }
    
    .chat-history-item {
        padding: 0.75rem;
        margin: 0.25rem 0;
        background: var(--bg-chat);
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.2s;
        border: 1px solid transparent;
    }
    
    .chat-history-item:hover {
        border-color: var(--border);
        background: #4a4a4a;
    }
    
    .chat-title {
        font-weight: 500;
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
    }
    
    .chat-preview {
        font-size: 0.75rem;
        color: var(--text-secondary);
        line-height: 1.3;
    }
    
    /* Login section */
    .login-section {
        border-top: 1px solid var(--border);
        padding-top: 1rem;
    }
    
    .login-form {
        margin-bottom: 1rem;
    }
    
    .login-input {
        width: 100%;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        background: var(--bg-chat);
        border: 1px solid var(--border);
        border-radius: 0.5rem;
        color: var(--text-primary);
        font-size: 14px;
        outline: none;
    }
    
    .login-input:focus {
        border-color: var(--accent);
    }
    
    .login-btn {
        background: transparent;
        color: var(--accent);
        border: 1px solid var(--accent);
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        width: 100%;
        cursor: pointer;
        font-weight: 500;
        margin-bottom: 0.5rem;
        transition: all 0.2s;
    }
    
    .login-btn:hover {
        background: var(--accent);
        color: white;
    }
    
    .user-profile {
        display: flex;
        align-items: center;
        padding: 0.75rem;
        background: var(--bg-chat);
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: var(--accent);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 0.75rem;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .user-info {
        flex: 1;
    }
    
    .username {
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    .user-plan {
        font-size: 0.75rem;
        color: var(--text-secondary);
    }
    
    .demo-accounts {
        margin-top: 1rem;
        padding: 0.75rem;
        background: var(--bg-chat);
        border-radius: 0.5rem;
    }
    
    .demo-title {
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .demo-list {
        font-size: 0.75rem;
        line-height: 1.4;
        color: var(--accent);
    }
    
    /* Messages area */
    .messages-area {
        flex: 1;
        padding: 1rem;
        overflow-y: auto;
        background: var(--bg-primary);
    }
    
    .message-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .message {
        margin: 1.5rem 0;
        display: flex;
        gap: 1rem;
    }
    
    .message-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.8rem;
        flex-shrink: 0;
    }
    
    .user-avatar {
        background: var(--accent);
        color: white;
    }
    
    .assistant-avatar {
        background: var(--bg-secondary);
        color: var(--text-primary);
        border: 1px solid var(--border);
    }
    
    .message-content {
        flex: 1;
        padding-top: 0.25rem;
    }
    
    .message-text {
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    /* Input area */
    .input-area {
        padding: 1rem;
        background: var(--bg-primary);
        border-top: 1px solid var(--border);
    }
    
    .input-container {
        max-width: 800px;
        margin: 0 auto;
        position: relative;
    }
    
    .chat-input {
        width: 100%;
        padding: 1rem 3rem 1rem 1rem;
        border-radius: 1.5rem;
        border: 1px solid var(--border);
        background: var(--bg-secondary);
        color: var(--text-primary);
        font-size: 16px;
        outline: none;
        resize: none;
        min-height: 24px;
        max-height: 200px;
    }
    
    .chat-input:focus {
        border-color: var(--accent);
    }
    
    .send-btn {
        position: absolute;
        right: 0.5rem;
        top: 50%;
        transform: translateY(-50%);
        background: var(--accent);
        border: none;
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 0.2s;
    }
    
    .send-btn:hover {
        background: var(--accent-hover);
    }
    
    .send-btn:disabled {
        background: var(--text-secondary);
        cursor: not-allowed;
    }
    
    /* Quick actions */
    .quick-actions {
        padding: 0.5rem 1rem;
        background: var(--bg-secondary);
        border-bottom: 1px solid var(--border);
        overflow-x: auto;
    }
    
    .quick-actions-row {
        display: flex;
        gap: 0.5rem;
        min-width: max-content;
    }
    
    .quick-action-btn {
        background: var(--bg-chat);
        color: var(--text-primary);
        border: 1px solid var(--border);
        padding: 0.5rem 1rem;
        border-radius: 1rem;
        cursor: pointer;
        font-size: 0.85rem;
        white-space: nowrap;
        transition: all 0.2s;
    }
    
    .quick-action-btn:hover {
        border-color: var(--accent);
        background: var(--accent);
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .sidebar {
            width: 85%;
        }
        
        .message {
            gap: 0.75rem;
        }
        
        .message-avatar {
            width: 28px;
            height: 28px;
        }
        
        .chat-input {
            font-size: 16px;
            padding: 0.875rem 3rem 0.875rem 1rem;
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }
</style>

<script>
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    
    if (sidebar.classList.contains('open')) {
        sidebar.classList.remove('open');
        overlay.style.display = 'none';
    } else {
        sidebar.classList.add('open');
        overlay.style.display = 'block';
    }
}

function closeSidebar() {
    document.querySelector('.sidebar').classList.remove('open');
    document.querySelector('.sidebar-overlay').style.display = 'none';
}

function newChat() {
    closeSidebar();
    // This will be handled by Streamlit
    document.getElementById('new-chat-trigger').click();
}

function quickAction(action) {
    const input = document.querySelector('.chat-input');
    input.value = action;
    input.focus();
}
</script>
""", unsafe_allow_html=True)

# =================== USER DATA MANAGEMENT ===================
@st.cache_data(ttl=3600)
def load_user_data():
    """Load users - using session state for cloud deployment"""
    if 'user_database' not in st.session_state:
        st.session_state.user_database = {
            "users": {
                "demo": {"password": "demo123", "created": "2025-11-05"},
                "student": {"password": "diet123", "created": "2025-11-05"},
                "vinayak": {"password": "diet2025", "created": "2025-11-05"},
                "prathmesh": {"password": "diet2025", "created": "2025-11-05"},
                "satwik": {"password": "diet2025", "created": "2025-11-05"},
                "rohan": {"password": "diet2025", "created": "2025-11-05"}
            },
            "chat_histories": {}
        }
    return st.session_state.user_database

def save_user_data(data):
    """Save user data to session state"""
    st.session_state.user_database = data

def get_user_chat_history(username):
    """Get chat history for logged-in user"""
    user_data = load_user_data()
    return user_data.get("chat_histories", {}).get(username, [])

def save_user_chat_history(username, messages):
    """Save chat history for logged-in user"""
    user_data = load_user_data()
    if "chat_histories" not in user_data:
        user_data["chat_histories"] = {}
    user_data["chat_histories"][username] = messages
    save_user_data(user_data)

# =================== AUTHENTICATION ===================
def login_user(username, password):
    """Login existing user"""
    user_data = load_user_data()
    users = user_data.get("users", {})
    
    if username.lower() in users and users[username.lower()]["password"] == password:
        return True, "Login successful!"
    return False, "Invalid credentials!"

def register_user(username, password):
    """Register new user"""
    user_data = load_user_data()
    if username.lower() in user_data["users"]:
        return False, "Username already exists!"
    
    user_data["users"][username.lower()] = {
        "password": password,
        "created": datetime.now().strftime("%Y-%m-%d")
    }
    save_user_data(user_data)
    return True, "Registration successful!"

# =================== ENHANCED AI RESPONSES ===================
def get_enhanced_career_response(user_message, username=None):
    """Enhanced career guidance system - deployment ready"""
    msg = user_message.lower().strip()
    greeting = f"Hi {username}! " if username else "Hello! "
    
    if any(word in msg for word in ['hello', 'hi', 'hey', 'start']):
        return f"""{greeting}🎓 **Welcome to DIET Career Buddy - ChatGPT Edition!**

I'm your AI-powered career assistant! Here's how I can help:

🤖 **Smart Career Guidance**: Advanced responses for all career questions
📊 **Real Market Data**: Current job trends and salary information 
🎯 **DIET Specialized**: Customized for engineering students
📱 **Mobile Ready**: Perfect on any device, anywhere

**🔥 Popular Topics:**
• "Technology careers for 2025"
• "Data science learning roadmap"
• "Software developer salaries in India"
• "Interview preparation tips"
• "Skills for campus placements"

What career aspect interests you today? 🚀"""

    elif any(word in msg for word in ['technology', 'tech', 'software', 'programming', 'developer']):
        return """🚀 **Technology Careers - Perfect for DIET Students!**

**🔥 Hottest Tech Roles in 2025:**
• **Full Stack Developer**: ₹4-25 LPA | React, Node.js, Python
• **Data Scientist**: ₹6-30 LPA | Python, ML, Statistics  
• **AI/ML Engineer**: ₹8-35 LPA | TensorFlow, PyTorch
• **DevOps Engineer**: ₹5-28 LPA | AWS, Docker, Kubernetes
• **Mobile Developer**: ₹4-22 LPA | Flutter, React Native
• **Cloud Engineer**: ₹6-32 LPA | AWS, Azure, GCP

**📈 Career Growth Path:**
Junior Developer → Senior Developer → Tech Lead → Engineering Manager/Architect

**🎯 Essential Skills Stack:**
• **Programming**: Python, JavaScript, Java, TypeScript
• **Frameworks**: React, Angular, Django, Spring Boot
• **Cloud**: AWS, Docker, Kubernetes, CI/CD
• **Databases**: PostgreSQL, MongoDB, Redis

**💡 DIET Student Advantage**: Your engineering foundation gives you a strong start in tech!

Which specific area interests you? I can create a detailed roadmap! 🎯"""

    elif any(word in msg for word in ['data science', 'ai', 'machine learning', 'ml', 'analytics']):
        return """🤖 **Data Science & AI/ML - The Future Career Path!**

**📊 High-Demand Data Roles in 2025:**
• **Data Scientist**: ₹6-35 LPA | Statistics, ML, Business insights
• **ML Engineer**: ₹8-40 LPA | Model deployment, MLOps
• **Data Analyst**: ₹4-16 LPA | SQL, Python, Visualization
• **AI Research Engineer**: ₹12-50+ LPA | Deep learning, Research
• **Business Intelligence**: ₹5-20 LPA | Tableau, Power BI

**🛠️ Complete Tech Stack:**
• **Programming**: Python, R, SQL, Scala
• **ML Libraries**: scikit-learn, TensorFlow, PyTorch, Keras
• **Data Tools**: pandas, NumPy, Jupyter, Apache Spark
• **Visualization**: Matplotlib, Seaborn, Plotly, Tableau
• **Cloud ML**: AWS SageMaker, Google AI Platform

**📚 6-Month Learning Roadmap:**
• **Month 1-2**: Python + SQL fundamentals
• **Month 3**: Statistics + Data analysis with pandas
• **Month 4**: Machine Learning with scikit-learn
• **Month 5**: Deep Learning with TensorFlow
• **Month 6**: MLOps + Portfolio projects

**🎓 Perfect for DIET Students**: Your math and programming background is ideal!

Want a personalized learning plan? 🚀"""

    elif any(word in msg for word in ['salary', 'pay', 'income', 'package', 'compensation']):
        return """💰 **2025 Tech Salary Guide - Complete Market Analysis**

**📈 Software Development Salaries (India):**
• **Fresher (0-1 years)**: ₹3.5-8 LPA
• **Junior (1-3 years)**: ₹6-16 LPA
• **Mid-level (3-6 years)**: ₹12-30 LPA
• **Senior (6-10 years)**: ₹25-55 LPA
• **Lead/Principal (10+ years)**: ₹40-80+ LPA

**🤖 AI/ML & Data Science:**
• **Entry Level**: ₹5-12 LPA
• **Experienced**: ₹15-40 LPA
• **Senior/Lead**: ₹30-70+ LPA

**☁️ DevOps & Cloud:**
• **Junior**: ₹4-12 LPA
• **Mid-level**: ₹12-25 LPA
• **Senior**: ₹20-45+ LPA

**🏢 By Company Type:**
• **FAANG**: ₹25-100+ LPA (Google, Amazon, Microsoft)
• **Unicorns**: ₹15-60+ LPA (Flipkart, Paytm, Byju's)
• **Product**: ₹10-50+ LPA (Adobe, Atlassian, VMware)
• **Service**: ₹3.5-25 LPA (TCS, Infosys, Wipro)

**🌟 Salary Boosters:**
• **Skills**: AWS, React, Python, Kubernetes (+20-40%)
• **Location**: Bangalore, Pune, Hyderabad (+10-25%)
• **Remote**: Global companies (USD packages!)

**💡 DIET Strategy**: Focus on high-demand skills + strong portfolio = ₹8-15 LPA direct placement possible!

Want salary info for specific roles? 💼"""

    elif any(word in msg for word in ['skills', 'learn', 'roadmap', 'course', 'study']):
        return """📚 **Skills Development Roadmap for Career Success**

**🔥 Most In-Demand Tech Skills 2025:**

**Programming Languages (Master These):**
• **Python** 🐍: AI/ML, Backend, Data Science, Automation
• **JavaScript** ⚡: Frontend, Backend (Node.js), Full Stack
• **Java** ☕: Enterprise apps, Android, Big Data
• **TypeScript**: Better JavaScript for large applications

**🌐 Web Development:**
• **Frontend**: React, Angular, Vue.js + TypeScript
• **Backend**: Node.js, Django, Spring Boot, FastAPI
• **Full Stack**: MERN, MEAN, Django + React

**☁️ Cloud & DevOps (High Growth):**
• **Cloud Platforms**: AWS, Azure, Google Cloud Platform
• **Containerization**: Docker, Kubernetes, Microservices
• **CI/CD**: Jenkins, GitHub Actions, GitLab CI
• **Infrastructure**: Terraform, Ansible, Monitoring

**📱 Mobile Development:**
• **Cross-Platform**: Flutter (Dart), React Native (JS)
• **Native**: Android (Kotlin), iOS (Swift)

**📖 Learning Resources:**
• **Free**: freeCodeCamp, Coursera (audit), YouTube, Kaggle Learn
• **Paid**: Udemy courses (₹500-2000), Pluralsight, bootcamps

**🎯 3-Month Sprint Plan:**
• **Month 1**: Pick ONE skill (Python/JavaScript), build 2 projects
• **Month 2**: Learn frameworks, build 2-3 medium projects
• **Month 3**: Advanced concepts, 1 comprehensive portfolio project

**💡 Pro Tips:**
• Learn by building, not just watching tutorials
• Practice coding problems daily (LeetCode, HackerRank)
• Join tech communities (Discord, Reddit, Stack Overflow)
• Contribute to open source projects

Which skill area interests you most? 🚀"""

    elif any(word in msg for word in ['diet', 'college', 'dnyanshree', 'placement']):
        return """🎓 **Career Excellence Guide for DIET Students**

**🏛️ DIET (Dnyanshree Institute of Engineering & Technology) Advantages:**

**Academic Strengths:**
• **Solid Engineering Curriculum**: Strong CS fundamentals
• **Practical Learning**: Hands-on lab sessions, project-based approach
• **Industry Connections**: Guest lectures, industrial visits
• **Faculty Support**: Experienced professors with industry insights
• **Modern Infrastructure**: Well-equipped labs and facilities

**📈 DIET Alumni Success Stories:**
• **Service Companies**: TCS, Infosys, Wipro (₹3.5-8 LPA packages)
• **Product Companies**: Amazon, Microsoft via referrals (₹15-30 LPA)
• **Startups**: Growing presence in fintech, ed-tech (₹6-15 LPA)
• **Higher Studies**: MTech in IITs, MS abroad with scholarships
• **Entrepreneurship**: Alumni founding successful tech startups

**💼 Placement Cell Support:**
• **Pre-placement Training**: Technical + aptitude + soft skills
• **Company Partnerships**: Regular recruitment drives
• **Mock Interviews**: HR and technical rounds practice
• **Resume Workshops**: ATS optimization and formatting
• **Industry Exposure**: Guest lectures from corporate leaders

**🎯 DIET Student Action Plan:**
• **Academic Excellence**: Maintain 7+ CGPA for company eligibility
• **Skill Development**: Master programming + choose specialization
• **Project Portfolio**: 4-5 comprehensive projects with documentation
• **Competitive Programming**: Regular practice on coding platforms
• **Professional Network**: Connect with alumni in target companies

**🌟 Local Advantage:**
• **Pune IT Hub**: Proximity to major tech companies
• **Mumbai Financial District**: Fintech and banking opportunities
• **Growing Startup Ecosystem**: Local entrepreneur network
• **Industry 4.0**: Manufacturing + tech convergence opportunities

What specific aspect would you like to focus on? 🎯"""

    else:
        return f"""Thanks for asking: "{user_message}" 🤔

I'm your enhanced DIET Career AI Assistant! I can help with:

**💼 Career Exploration:**
• Technology roles (Software, Data Science, AI/ML, DevOps, Mobile)
• Career growth paths and salary analysis
• Industry trends and emerging opportunities

**💰 Market Intelligence:**
• Real-time salary data for 2025 job market
• High-demand skills and certification guidance
• Company-wise compensation analysis

**🎯 Professional Development:**
• Personalized learning roadmaps
• Interview preparation strategies
• Portfolio building guidance
• Job search optimization

**🎓 DIET-Specific Support:**
• Campus placement preparation
• Alumni networking opportunities
• College resource utilization
• Local industry insights

**Try asking:**
• "What are the best tech careers for 2025?"
• "Create a learning roadmap for full-stack development"
• "How much do data scientists earn in India?"
• "Interview tips for DIET students"

What career topic interests you most? 🌟"""

def smart_ai_response(user_message, username=None):
    """Main AI response function"""
    return get_enhanced_career_response(user_message, username)

# =================== INITIALIZE SESSION STATE ===================
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "🎓 Hello! I'm your DIET Career Assistant. I can help with career guidance, salary insights, job market trends, and skill development. What would you like to explore today?"
        }
    ]

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'chat_histories' not in st.session_state:
    st.session_state.chat_histories = {
        "Tech Career Planning": ["What are the best tech careers?", "How to become a data scientist?"],
        "Salary Research": ["Software developer salaries", "FAANG compensation"],
        "Interview Prep": ["Common interview questions", "How to prepare for coding interviews"],
        "DIET Guidance": ["College placement tips", "Alumni network benefits"],
        "Learning Roadmaps": ["Python learning path", "Full-stack development guide"]
    }

if 'show_login_form' not in st.session_state:
    st.session_state.show_login_form = False

if 'show_register_form' not in st.session_state:
    st.session_state.show_register_form = False

# Load user data
load_user_data()

# =================== MAIN CHATGPT-STYLE INTERFACE ===================

# Main container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="chat-header">
    <button class="header-btn" onclick="toggleSidebar()">☰</button>
    <h1 class="app-title">🎓 DIET Career Buddy</h1>
    <button class="header-btn" onclick="document.querySelector('.messages-area').scrollTop = 0">↻</button>
</div>
""", unsafe_allow_html=True)

# Quick actions bar
st.markdown("""
<div class="quick-actions">
    <div class="quick-actions-row">
        <button class="quick-action-btn" onclick="quickAction('What are the best technology careers for 2025?')">💻 Tech Careers</button>
        <button class="quick-action-btn" onclick="quickAction('Show me tech salary ranges for 2025')">💰 Salaries</button>
        <button class="quick-action-btn" onclick="quickAction('Create a skill development roadmap')">📚 Learning</button>
        <button class="quick-action-btn" onclick="quickAction('Career guidance for DIET students')">🎓 DIET Guide</button>
        <button class="quick-action-btn" onclick="quickAction('Interview preparation tips')">🎯 Interviews</button>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar overlay and menu
st.markdown("""
<div class="sidebar-overlay" onclick="closeSidebar()"></div>
<div class="sidebar">
    <div class="sidebar-header">
        <h2 class="sidebar-title">Menu</h2>
        <button class="close-btn" onclick="closeSidebar()">×</button>
    </div>
    <div class="sidebar-content">
        <button class="new-chat-btn" onclick="newChat()">+ New Chat</button>
""", unsafe_allow_html=True)

# Recent chats section
st.markdown('<div class="section-title">Recent Chats</div>', unsafe_allow_html=True)

for chat_name, messages in st.session_state.chat_histories.items():
    preview = messages[0][:40] + "..." if messages else "New conversation"
    st.markdown(f"""
    <div class="chat-history-item" onclick="closeSidebar()">
        <div class="chat-title">{chat_name}</div>
        <div class="chat-preview">{preview}</div>
    </div>
    """, unsafe_allow_html=True)

# Login/User section
st.markdown('<div class="login-section">', unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.markdown('<div class="section-title">Account</div>', unsafe_allow_html=True)
    
    # Login form
    with st.form("sidebar_login_form"):
        login_username = st.text_input("Username", key="sidebar_login_user", placeholder="Enter username")
        login_password = st.text_input("Password", type="password", key="sidebar_login_pass", placeholder="Enter password")
        login_col1, login_col2 = st.columns(2)
        
        with login_col1:
            login_btn = st.form_submit_button("🚀 Login", use_container_width=True)
        with login_col2:
            register_btn = st.form_submit_button("📝 Register", use_container_width=True)
        
        if login_btn and login_username and login_password:
            success, msg = login_user(login_username, login_password)
            if success:
                st.session_state.logged_in = True
                st.session_state.current_user = login_username.lower()
                saved_history = get_user_chat_history(login_username.lower())
                if saved_history:
                    st.session_state.messages = saved_history
                st.success(f"Welcome back, {login_username}!")
                st.rerun()
            else:
                st.error(msg)
        
        if register_btn and login_username and login_password:
            success, msg = register_user(login_username, login_password)
            if success:
                st.success(msg)
            else:
                st.error(msg)
    
    # Demo accounts
    st.markdown("""
    <div class="demo-accounts">
        <div class="demo-title">Demo Accounts</div>
        <div class="demo-list">
            • demo / demo123<br>
            • student / diet123<br>
            • DIET team: vinayak, prathmesh, satwik, rohan / diet2025
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # Logged in user profile
    username = st.session_state.current_user
    st.markdown(f"""
    <div class="user-profile">
        <div class="avatar">{username[0].upper()}</div>
        <div class="user-info">
            <div class="username">{username.title()}</div>
            <div class="user-plan">Free Plan • Chat history saved</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Logout", key="sidebar_logout", use_container_width=True):
        if st.session_state.current_user and st.session_state.messages:
            save_user_chat_history(st.session_state.current_user, st.session_state.messages)
        
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.messages = [
            {"role": "assistant", "content": "Logged out successfully! You're now in guest mode."}
        ]
        st.rerun()

st.markdown('</div></div></div>', unsafe_allow_html=True)  # Close login-section, sidebar-content, sidebar

# Messages area
st.markdown('<div class="messages-area"><div class="message-container">', unsafe_allow_html=True)

for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="message">
            <div class="message-avatar user-avatar">You</div>
            <div class="message-content">
                <div class="message-text">{msg["content"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message">
            <div class="message-avatar assistant-avatar">🎓</div>
            <div class="message-content">
                <div class="message-text">{msg["content"]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)  # Close message-container and messages-area

# Input area
st.markdown('<div class="input-area"><div class="input-container">', unsafe_allow_html=True)

# Hidden button for new chat functionality
if st.button("New Chat", key="new_chat_trigger", type="primary"):
    if st.session_state.logged_in and st.session_state.current_user:
        save_user_chat_history(st.session_state.current_user, st.session_state.messages)
    
    current_time = datetime.now().strftime("%H:%M")
    st.session_state.messages = [
        {"role": "assistant", "content": f"New chat started! How can I help you with your career today?"}
    ]
    st.rerun()

# Chat input form
with st.form(key='chatgpt_chat_form', clear_on_submit=True):
    user_input = st.text_area(
        "",
        placeholder="Ask about careers, skills, salaries, or job market trends...",
        key="chatgpt_chat_input",
        height=50,
        label_visibility="collapsed"
    )
    
    submit = st.form_submit_button("Send", use_container_width=True)

st.markdown('</div></div>', unsafe_allow_html=True)  # Close input-container and input-area

# Process input
if submit and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate response
    with st.spinner("🤖 Thinking..."):
        bot_response = smart_ai_response(user_input, st.session_state.current_user)
    
    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    # Save if logged in
    if st.session_state.logged_in and st.session_state.current_user:
        save_user_chat_history(st.session_state.current_user, st.session_state.messages)
    
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)  # Close main chat-container

# Footer info
st.markdown("""
<div style="position: fixed; bottom: 0; right: 0; padding: 0.5rem; background: rgba(33, 33, 33, 0.9); border-radius: 0.5rem 0 0 0; font-size: 0.7rem; color: #b0b0b0;">
    DIET Career Buddy • Enhanced by VINAYAK, PRATHMESH, SATWIK, ROHAN
</div>
""", unsafe_allow_html=True)
