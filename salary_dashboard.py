import streamlit as st
from api_functions import get_market_sentiment

def show():
    """💰 Live Salary Dashboard"""
    
    st.markdown("""
    <div class="dashboard-header">
        <h1 style="color: #10a37f; margin: 0;">💰 Live Salary Dashboard</h1>
        <p style="margin: 10px 0 0 0; color: #a0aec0;">Real-time salary data with market intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get live market data
    market_data = get_market_sentiment()
    
    # Market Overview
    st.markdown("## 📈 **Live Market Sentiment**")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Market Trend", market_data['trend'], f"{market_data['change']:.1f}%")
    with col2:
        st.metric("Salary Multiplier", f"{market_data['multiplier']:.2f}x", "Live adjustment")
    with col3:
        st.metric("Job Market", "🔥 Hot", "High demand")
    with col4:
        st.metric("Best Time to Apply", "✅ Now", "Optimal timing")
    
    # Salary Data
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 💼 **Market-Adjusted Salary Ranges**")
    
    salary_data = [
        {"role": "💻 Software Engineer", "base_min": 4, "base_max": 25, "growth": "+22%"},
        {"role": "📊 Data Scientist", "base_min": 6, "base_max": 30, "growth": "+28%"},
        {"role": "☁️ DevOps Engineer", "base_min": 5, "base_max": 28, "growth": "+35%"},
        {"role": "📱 Product Manager", "base_min": 8, "base_max": 45, "growth": "+20%"},
        {"role": "🤖 AI/ML Engineer", "base_min": 7, "base_max": 35, "growth": "+40%"},
        {"role": "🔒 Cybersecurity Engineer", "base_min": 6, "base_max": 28, "growth": "+25%"}
    ]
    
    for role in salary_data:
        # Apply market adjustment
        multiplier = market_data['multiplier']
        adj_min = int(role["base_min"] * multiplier)
        adj_max = int(role["base_max"] * multiplier)
        
        st.markdown(f"""
        <div class="dashboard-card">
            <h3 style="color: #10a37f;">{role['role']} 
                <span style="color: #68d391; font-size: 0.8em;">{role['growth']}</span>
            </h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <strong>💰 Salary Range:</strong> ₹{adj_min}-{adj_max} LPA<br>
                    <strong>📈 Market Status:</strong> {market_data['trend']}
                </div>
                <div>
                    <strong>🎯 Experience Levels:</strong><br>
                    Entry: ₹{adj_min}-{int(adj_min*1.5)} LPA<br>
                    Mid: ₹{int(adj_min*1.8)}-{int(adj_max*0.7)} LPA<br>
                    Senior: ₹{int(adj_max*0.7)}-{adj_max} LPA
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Geographic Analysis
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 🌍 **City-wise Salary Analysis**")
    
    cities = [
        {"city": "Bangalore", "multiplier": 1.2, "desc": "Tech capital, highest salaries"},
        {"city": "Mumbai", "multiplier": 1.15, "desc": "Financial hub, premium roles"},
        {"city": "Hyderabad", "multiplier": 1.1, "desc": "Growing tech scene"},
        {"city": "Pune", "multiplier": 1.05, "desc": "Balanced cost-salary ratio"},
        {"city": "Chennai", "multiplier": 1.0, "desc": "Steady growth market"},
        {"city": "Delhi NCR", "multiplier": 1.18, "desc": "Corporate headquarters"}
    ]
    
    col1, col2, col3 = st.columns(3)
    for i, city in enumerate(cities):
        column = [col1, col2, col3][i % 3]
        with column:
            st.markdown(f"""
            <div class="dashboard-card">
                <h4 style="color: #10a37f;">{city['city']}</h4>
                <div style="font-size: 1.3em; font-weight: bold; color: #68d391;">{city['multiplier']}x</div>
                <p style="font-size: 0.9em; color: #a0aec0;">{city['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
