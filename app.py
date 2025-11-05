import streamlit as st
from streamlit_chat import message
import json
from datetime import datetime
import pandas as pd

# Enhanced page configuration for deployment
st.set_page_config(
    page_title="🎓 DIET Career Buddy - AI Career Guidance", 
    page_icon="🎓",
    layout="wide"
)

# Modern CSS styling for mobile + cloud
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #FF8C00 0%, #FF6B35 50%, #FF4500 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(255, 140, 0, 0.3);
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #FF8C00;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #FF8C00, #FF6B35);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 140, 0, 0.4);
    }
    
    /* Mobile optimizations */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 0.5rem;
        }
        
        .stTextInput > div > div > input {
            font-size: 16px !important;
        }
        
        .stButton > button {
            width: 100%;
        }
        
        .main-header h1 {
            font-size: 2rem !important;
        }
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>

<!-- PWA Meta Tags -->
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#FF8C00">
""", unsafe_allow_html=True)

# =================== USER DATA MANAGEMENT (Cloud Compatible) ===================
@st.cache_data(ttl=3600)  # Cache for 1 hour
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
        return f"""{greeting}🎓 **Welcome to DIET Career Buddy - Cloud Edition!**

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

    elif any(word in msg for word in ['interview', 'job', 'placement', 'company']):
        return """🎯 **Interview & Job Search Guide for DIET Students**

**📍 Best Job Search Platforms:**
• **LinkedIn**: Professional networking + direct applications
• **Naukri.com**: Traditional Indian job portal
• **AngelList**: Startup opportunities with equity
• **Company websites**: Direct career page applications
• **Referrals**: Most effective method (70% success rate)

**📋 Application Essentials:**
• **ATS-Optimized Resume**: Keywords matching job requirements
• **GitHub Portfolio**: 4-5 quality projects with documentation
• **LinkedIn Profile**: Professional summary + recommendations
• **Cover Letter**: Personalized for each application

**🧠 Technical Interview Prep:**
• **Data Structures**: Arrays, LinkedLists, Trees, Graphs
• **Algorithms**: Sorting, Searching, Dynamic Programming
• **System Design**: Basic scalability concepts (senior roles)
• **Coding Practice**: LeetCode (Easy→Medium), HackerRank

**🗣️ Behavioral Interview (STAR Method):**
• **Situation**: Set the context
• **Task**: Explain your responsibility
• **Action**: Detail what you did
• **Result**: Share the positive outcome

**📅 DIET Placement Timeline:**
• **Pre-Final Year**: Build skills, complete internships
• **Final Year (July-Aug)**: Resume prep, company applications
• **Sep-Nov**: Peak placement season
• **Dec-Feb**: Off-campus applications, startup opportunities

**🎓 DIET Advantages to Highlight:**
• Strong engineering fundamentals from rigorous curriculum
• Hands-on project experience from lab sessions
• Problem-solving mindset from technical courses
• Team collaboration from group projects

**💡 Interview Success Tips:**
• Research company culture and recent news
• Practice explaining technical projects clearly
• Prepare thoughtful questions about the role
• Show enthusiasm for learning and growth

Need specific prep for any company or role? 💪"""

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

**📊 Recent Placement Highlights:**
• **Overall Success Rate**: 75-85% placement in good academic years
• **Average Package**: ₹4-6 LPA across engineering branches
• **Top Packages**: ₹15-25 LPA for exceptional performers
• **Diverse Sectors**: IT services, product companies, fintech, consulting

**💡 Career Growth Strategy:**
• **Year 1-2**: Focus on learning and skill building (₹3.5-8 LPA)
• **Year 3-5**: Specialization and leadership roles (₹8-20 LPA)
• **Year 5+**: Senior positions, possible entrepreneurship (₹20-50+ LPA)

**🤝 Alumni Network Benefits:**
• **Referral Opportunities**: Direct connections in target companies
• **Career Mentorship**: Guidance from industry professionals
• **Industry Insights**: Real-world perspectives on career paths
• **Networking Events**: Professional connections and opportunities

**🚀 Next Steps for Success:**
1. **Assess Current Skills**: Identify strengths and improvement areas
2. **Choose Specialization**: Web Dev, Data Science, Mobile, or Cloud
3. **Build Portfolio**: Create impressive projects showcasing skills
4. **Practice Interviews**: Technical and behavioral preparation
5. **Network Actively**: Connect with alumni and industry professionals

**You're from DIET - you have the foundation for a successful tech career!** 🌟

What specific aspect would you like to focus on? 🎯"""

    else:
        return f"""Thanks for asking: "{user_message}" 🤔

I'm your enhanced DIET Career AI Assistant running in the cloud! I can help with:

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

# =================== MAIN APPLICATION ===================

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "🎓 Hello! I'm your DIET Career Assistant powered by cloud AI. I can help with career guidance, salary insights, job market trends, and skill development. 💡 **Tip:** Login to save your chat history!"
        }
    ]

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Load user data
load_user_data()

# Main Header
st.markdown("""
<div class="main-header">
    <h1 style="color: white; margin: 0; font-size: 3rem;">🎓 DIET Career Buddy</h1>
    <h2 style="color: white; margin: 0.5rem 0; font-size: 1.5rem;">Cloud AI Edition</h2>
    <p style="color: white; margin: 0; font-size: 1.1rem; opacity: 0.9;">
        Advanced AI Career Guidance • Real-time Market Data • Mobile Optimized
    </p>
</div>
""", unsafe_allow_html=True)

# Feature showcase
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🤖 Cloud AI Engine</h3>
        <p><strong>Status:</strong> 🟢 Online</p>
        <p>Advanced AI running in the cloud for intelligent career guidance</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Real-time Data</h3>
        <p><strong>Status:</strong> 🟢 Active</p>
        <p>Current job market insights and salary information for 2025</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>🎓 DIET Focused</h3>
        <p><strong>Status:</strong> 🟢 Specialized</p>
        <p>Customized guidance for engineering students and tech careers</p>
    </div>
    """, unsafe_allow_html=True)

# =================== SIDEBAR ===================
with st.sidebar:
    st.markdown("### 🎓 DIET Career AI")
    
    # Login/Register Section
    if not st.session_state.logged_in:
        st.markdown("#### 🔐 Login / Register")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                login_username = st.text_input("Username", key="login_user")
                login_password = st.text_input("Password", type="password", key="login_pass")
                login_btn = st.form_submit_button("🚀 Login")
                
                if login_btn and login_username and login_password:
                    success, msg = login_user(login_username, login_password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.current_user = login_username.lower()
                        # Load saved chat history
                        saved_history = get_user_chat_history(login_username.lower())
                        if saved_history:
                            st.session_state.messages = saved_history
                        st.success(f"Welcome back, {login_username}! 🎉")
                        st.rerun()
                    else:
                        st.error(msg)
        
        with tab2:
            with st.form("register_form"):
                reg_username = st.text_input("Choose Username", key="reg_user")
                reg_password = st.text_input("Choose Password", type="password", key="reg_pass")
                reg_btn = st.form_submit_button("📝 Register")
                
                if reg_btn and reg_username and reg_password:
                    success, msg = register_user(reg_username, reg_password)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
        
        st.markdown("---")
        st.markdown("**Demo Accounts:**")
        st.markdown("• `demo` / `demo123`")
        st.markdown("• `student` / `diet123`")
        st.markdown("• DIET team: `vinayak`, `prathmesh`, `satwik`, `rohan` / `diet2025`")
        
        st.markdown("---")
        st.markdown("**🌟 Guest Mode**")
        st.markdown("✅ Full functionality  \n❌ No chat saving  \n💡 Login to persist chats")
    
    else:
        # Logged in user
        st.markdown(f"#### 👤 Welcome, {st.session_state.current_user.title()}!")
        st.markdown("**💾 Status:** Chat history saving automatically")
        
        if st.button("🚪 Logout", use_container_width=True):
            if st.session_state.current_user and st.session_state.messages:
                save_user_chat_history(st.session_state.current_user, st.session_state.messages)
            
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.messages = [
                {"role": "assistant", "content": "Logged out successfully! You're now in guest mode. Login to save conversations."}
            ]
            st.rerun()
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("### ⚡ **Quick Topics**")
    
    if st.button("🚀 Tech Careers", key="tech_quick"):
        user_msg = "What are the best technology careers for 2025?"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        response = smart_ai_response(user_msg, st.session_state.current_user)
        st.session_state.messages.append({"role": "assistant", "content": response})
        if st.session_state.logged_in:
            save_user_chat_history(st.session_state.current_user, st.session_state.messages)
        st.rerun()
    
    if st.button("💰 Salaries", key="salary_quick"):
        user_msg = "Show me tech salary ranges for 2025"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        response = smart_ai_response(user_msg, st.session_state.current_user)
        st.session_state.messages.append({"role": "assistant", "content": response})
        if st.session_state.logged_in:
            save_user_chat_history(st.session_state.current_user, st.session_state.messages)
        st.rerun()
    
    if st.button("📚 Learning", key="learn_quick"):
        user_msg = "Create a skill development roadmap"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        response = smart_ai_response(user_msg, st.session_state.current_user)
        st.session_state.messages.append({"role": "assistant", "content": response})
        if st.session_state.logged_in:
            save_user_chat_history(st.session_state.current_user, st.session_state.messages)
        st.rerun()
    
    if st.button("🎯 DIET Guide", key="diet_quick"):
        user_msg = "Career guidance for DIET students"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        response = smart_ai_response(user_msg, st.session_state.current_user)
        st.session_state.messages.append({"role": "assistant", "content": response})
        if st.session_state.logged_in:
            save_user_chat_history(st.session_state.current_user, st.session_state.messages)
        st.rerun()
    
    if st.button("🗑️ New Chat", key="new_chat"):
        if st.session_state.logged_in and st.session_state.current_user:
            save_user_chat_history(st.session_state.current_user, st.session_state.messages)
        
        welcome_msg = f"Hello {st.session_state.current_user.title()}! New chat started. How can I help?" if st.session_state.logged_in else "New chat started! How can I help with your career today?"
        st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 👥 **About**")
    st.markdown("""
    **DIET Career Buddy**
    
    **Enhanced by:**
    • VINAYAK KHARADE
    • PRATHMESH SANDIM  
    • SATWIK TAMBEWAGH
    • ROHAN SAWANT
    
    **Features:**
    ✅ Cloud AI responses
    💾 Chat persistence
    📱 Mobile optimized
    🎓 DIET specialized
    """)

# =================== CHAT INTERFACE ===================

# Status indicator
status = "🟢 Logged in" if st.session_state.logged_in else "🔵 Guest Mode"
st.markdown(f"**Status:** {status} {'(Chats saving)' if st.session_state.logged_in else '(Chats not saved)'}")

# Display messages
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        message(msg["content"], is_user=True, key=f"user_{i}")
    else:
        message(msg["content"], key=f"bot_{i}")

# Chat input
st.markdown("---")
with st.form(key='chat_form', clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask me about careers, skills, salaries, or job trends...",
            key="user_input",
            placeholder="💭 Example: 'What skills do I need for data science?'"
        )
    
    with col2:
        send_button = st.form_submit_button("Send 🚀")

# Process input
if send_button and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate response
    with st.spinner("🤖 Generating response..."):
        bot_response = smart_ai_response(user_input, st.session_state.current_user)
    
    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    # Save if logged in
    if st.session_state.logged_in and st.session_state.current_user:
        save_user_chat_history(st.session_state.current_user, st.session_state.messages)
    
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666666; font-size: 14px;'>
    <p><strong>🎓 DIET Career Buddy - Cloud AI Edition</strong></p>
    <p>Enhanced AI Career Guidance • Mobile Optimized • Built by DIET Students</p>
    <p>Dnyanshree Institute of Engineering & Technology | 2025</p>
</div>
""", unsafe_allow_html=True)
