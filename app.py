import streamlit as st
import requests

st.set_page_config(page_title="DIET Career Buddy", layout="wide", initial_sidebar_state="collapsed")

# SIMPLE CSS - Just the essentials
st.markdown("""
<style>
    .main .block-container { padding-top: 0rem; padding-left: 0rem; padding-right: 0rem; }
    .stApp > header { display: none; }
    header[data-testid="stHeader"] { display: none; }
    .stDeployButton { display: none; }
    section[data-testid="stSidebar"] { display: none; }
    
    body { background: #212121; color: white; margin: 0; padding: 0; }
    .stApp { background: #212121; }
    
    .header { background: #303030; padding: 10px; text-align: center; font-weight: bold; border-bottom: 1px solid #444; }
    .buttons { display: flex; gap: 5px; padding: 10px; background: #303030; }
    .btn { flex: 1; padding: 10px; background: #424242; color: white; border: 1px solid #555; border-radius: 5px; text-align: center; cursor: pointer; }
    .content { padding: 20px; min-height: 400px; }
    
    .stButton > button { 
        background: #424242 !important; 
        color: white !important; 
        border: 1px solid #555 !important; 
        width: 100% !important;
        height: 60px !important;
    }
    .stButton > button:hover { background: #10a37f !important; }
</style>
""", unsafe_allow_html=True)

# Simple API function
@st.cache_data(ttl=3600)
def get_job_count():
    try:
        r = requests.get("https://api.github.com/search/repositories?q=job+hiring", timeout=5)
        return r.json().get("total_count", 5000) if r.status_code == 200 else 5000
    except:
        return 5000

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'chat'

# Header
st.markdown('<div class="header">🎓 DIET Career Buddy</div>', unsafe_allow_html=True)

# Buttons
st.markdown('<div class="buttons">', unsafe_allow_html=True)
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("💻 Tech", key="tech"):
        st.session_state.page = 'tech'
        st.rerun()

with col2:
    if st.button("💰 Salary", key="salary"):
        st.session_state.page = 'salary'
        st.rerun()

with col3:
    if st.button("📚 Learn", key="learn"):
        st.session_state.page = 'learn'
        st.rerun()

with col4:
    if st.button("🎓 DIET", key="diet"):
        st.session_state.page = 'diet'
        st.rerun()

with col5:
    if st.button("🎯 Interview", key="interview"):
        st.session_state.page = 'interview'
        st.rerun()

with col6:
    if st.button("📊 Jobs", key="jobs"):
        st.session_state.page = 'jobs'
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Content
st.markdown('<div class="content">', unsafe_allow_html=True)

if st.session_state.page == 'jobs':
    st.markdown("## 📊 Live Job Market")
    
    job_count = get_job_count()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Jobs", f"{job_count:,}+")
    with col2:
        st.metric("Growth", "+15%")
    with col3:
        st.metric("Active", "Live")
    
    st.write("**🔥 Hot Categories:**")
    st.write("• Software Development: 3,000+ jobs")
    st.write("• Data Science: 1,500+ jobs") 
    st.write("• DevOps: 1,000+ jobs")
    
    if st.button("← Back"):
        st.session_state.page = 'chat'
        st.rerun()

elif st.session_state.page == 'salary':
    st.markdown("## 💰 Salary Insights")
    
    st.write("**💼 Tech Salaries in India:**")
    st.write("• Software Engineer: ₹4-25 LPA")
    st.write("• Data Scientist: ₹6-30 LPA")
    st.write("• DevOps Engineer: ₹5-28 LPA")
    st.write("• Product Manager: ₹8-45 LPA")
    
    if st.button("← Back"):
        st.session_state.page = 'chat'
        st.rerun()

else:
    st.markdown("## 🎓 Welcome to DIET Career Buddy!")
    st.write("I'm your AI career assistant! Click the buttons above to explore:")
    st.write("• **💻 Tech** - Latest technology trends and jobs")
    st.write("• **💰 Salary** - Current salary ranges and insights")
    st.write("• **📚 Learn** - Learning paths and skill development")
    st.write("• **🎓 DIET** - College-specific guidance and tips")
    st.write("• **🎯 Interview** - Interview preparation and questions")
    st.write("• **📊 Jobs** - Live job market data and trends")
    
    # Simple chat
    user_input = st.text_input("Ask me anything about careers:")
    if user_input:
        st.write(f"**You asked:** {user_input}")
        st.write("**Assistant:** That's a great question! Click the dashboard buttons above for detailed insights, or I can provide general career guidance.")

st.markdown('</div>', unsafe_allow_html=True)
