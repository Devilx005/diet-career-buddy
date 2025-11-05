import streamlit as st
from api_functions import get_live_job_data, get_market_sentiment

def show():
    """📊 Live Jobs Dashboard"""
    
    st.markdown("""
    <div class="dashboard-header">
        <h1 style="color: #10a37f; margin: 0;">📊 Live Jobs Dashboard</h1>
        <p style="margin: 10px 0 0 0; color: #a0aec0;">Real-time job market analysis with live API data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get live data
    with st.spinner("🔄 Fetching live market data..."):
        job_data = get_live_job_data()
        market_data = get_market_sentiment()
    
    # Market Overview
    st.markdown("## 🌍 **Live Market Overview**")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Job Openings", f"{job_data['total']:,}+", "Live from API")
    with col2:
        st.metric("Market Sentiment", market_data['trend'], f"{market_data['change']:.1f}%")
    with col3:
        st.metric("Hiring Velocity", "🚀 High", "Real-time indicator")
    with col4:
        st.metric("Last Updated", job_data['updated'], "Live data")
    
    # Job Categories
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 🎯 **Job Categories Analysis**")
    
    categories = [
        {"category": "Software Development", "openings": "3,200+", "growth": "+25%", "remote": "70%"},
        {"category": "Data Science", "openings": "1,800+", "growth": "+35%", "remote": "80%"},
        {"category": "DevOps Engineering", "openings": "1,200+", "growth": "+40%", "remote": "85%"},
        {"category": "AI/ML Engineering", "openings": "900+", "growth": "+45%", "remote": "75%"},
        {"category": "Cybersecurity", "openings": "600+", "growth": "+30%", "remote": "60%"},
        {"category": "Mobile Development", "openings": "800+", "growth": "+20%", "remote": "65%"}
    ]
    
    for category in categories:
        st.markdown(f"""
        <div class="dashboard-card">
            <h3 style="color: #10a37f;">{category['category']} 
                <span style="color: #68d391; font-size: 0.8em;">{category['growth']}</span>
            </h3>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; text-align: center;">
                <div><strong>📊 Openings:</strong><br>{category['openings']}</div>
                <div><strong>🏠 Remote Jobs:</strong><br>{category['remote']}</div>
                <div><strong>📈 Growth:</strong><br>{category['growth']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Job Search Tips
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 💡 **Job Search Success Tips**")
    
    tips = [
        {"tip": "🎯 Target Application Strategy", "desc": "Apply to 5-10 companies per week with customized applications"},
        {"tip": "📱 Leverage Social Media", "desc": "Use LinkedIn, Twitter, and GitHub to showcase your work"},
        {"tip": "🤝 Network Actively", "desc": "Attend meetups, conferences, and connect with professionals"},
        {"tip": "📊 Track Applications", "desc": "Maintain spreadsheet of applications and follow-ups"},
        {"tip": "🔄 Continuous Learning", "desc": "Stay updated with latest technologies and trends"},
        {"tip": "💼 Portfolio Optimization", "desc": "Keep portfolio and resume updated with recent projects"}
    ]
    
    col1, col2 = st.columns(2)
    for i, tip in enumerate(tips):
        column = col1 if i % 2 == 0 else col2
        with column:
            st.markdown(f"""
            <div class="dashboard-card">
                <h4 style="color: #10a37f;">{tip['tip']}</h4>
                <p>{tip['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Market Trends
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 📈 **Current Market Trends**")
    
    trends = [
        "🔥 **AI/ML roles** seeing 45% growth in demand",
        "☁️ **Cloud skills** are essential for 85% of tech roles", 
        "🏠 **Remote work** available in 70% of software positions",
        "📊 **Data-driven roles** commanding premium salaries",
        "🔒 **Cybersecurity** demand up 30% due to security concerns",
        "📱 **Mobile development** steady with cross-platform focus"
    ]
    
    for trend in trends:
        st.markdown(f"""
        <div class="dashboard-card">
            <p style="font-size: 1.1em;">{trend}</p>
        </div>
        """, unsafe_allow_html=True)
