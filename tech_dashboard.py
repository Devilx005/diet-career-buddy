import streamlit as st
from api_functions import get_live_job_data

def show():
    """💻 Tech Careers Dashboard"""
    
    st.markdown("""
    <div class="dashboard-header">
        <h1 style="color: #10a37f; margin: 0;">💻 Tech Careers Dashboard</h1>
        <p style="margin: 10px 0 0 0; color: #a0aec0;">Complete guide to technology careers in 2025</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get live data
    job_data = get_live_job_data()
    
    # Tech Market Overview
    st.markdown("## 📊 **Tech Market Overview**")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Tech Jobs", f"{job_data['total']:,}+", "Live data")
    with col2:
        st.metric("Avg Growth", "+22%", "YoY")
    with col3:
        st.metric("Remote Jobs", "65%", "Available")
    with col4:
        st.metric("Demand", "🔥 High", "Current")
    
    # Career paths
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 🛣️ **Top Career Paths**")
    
    careers = [
        {"title": "🤖 AI/ML Engineer", "salary": "₹8-35 LPA", "growth": "+35%"},
        {"title": "☁️ DevOps Engineer", "salary": "₹6-30 LPA", "growth": "+28%"},
        {"title": "🌐 Full Stack Developer", "salary": "₹5-25 LPA", "growth": "+22%"},
        {"title": "📊 Data Engineer", "salary": "₹7-32 LPA", "growth": "+30%"},
    ]
    
    for career in careers:
        st.markdown(f"""
        <div class="dashboard-card">
            <h3 style="color: #10a37f;">{career['title']} <span style="color: #68d391; font-size: 0.8em;">{career['growth']}</span></h3>
            <p><strong>💰 Salary:</strong> {career['salary']}</p>
        </div>
        """, unsafe_allow_html=True)
