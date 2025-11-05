import streamlit as st

def show():
    """🎯 Interview Prep Dashboard"""
    
    st.markdown("""
    <div class="dashboard-header">
        <h1 style="color: #10a37f; margin: 0;">🎯 Interview Prep Dashboard</h1>
        <p style="margin: 10px 0 0 0; color: #a0aec0;">Complete interview preparation with practice tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Interview Stats
    st.markdown("## 📊 **Interview Success Metrics**")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Success Rate", "85%", "With proper prep")
    with col2:
        st.metric("Avg Prep Time", "3-4 months", "Recommended")
    with col3:
        st.metric("Practice Questions", "500+", "Minimum target")
    with col4:
        st.metric("Mock Interviews", "10+", "Before real ones")
    
    # Interview Rounds
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 🎪 **Interview Round Breakdown**")
    
    rounds = [
        {"round": "Technical Round 1", "focus": "Data Structures & Algorithms", "duration": "45-60 min",
         "tips": "Focus on clean code and optimal solutions"},
        {"round": "Technical Round 2", "focus": "System Design & Problem Solving", "duration": "45-60 min", 
         "tips": "Think out loud and discuss trade-offs"},
        {"round": "HR Round", "focus": "Behavioral & Cultural Fit", "duration": "30-45 min",
         "tips": "Prepare STAR format answers"},
        {"round": "Managerial Round", "focus": "Project Discussion", "duration": "30-45 min",
         "tips": "Focus on impact and learning"}
    ]
    
    for round_info in rounds:
        st.markdown(f"""
        <div class="dashboard-card">
            <h3 style="color: #10a37f;">{round_info['round']} ({round_info['duration']})</h3>
            <p><strong>Focus:</strong> {round_info['focus']}</p>
            <p><strong>💡 Key Tip:</strong> {round_info['tips']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # DSA Practice Tracker
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 📈 **DSA Practice Progress**")
    
    topics = [
        {"topic": "Arrays & Strings", "easy": 20, "medium": 15, "hard": 5},
        {"topic": "LinkedLists", "easy": 10, "medium": 8, "hard": 2},
        {"topic": "Trees & Graphs", "easy": 15, "medium": 12, "hard": 5},
        {"topic": "Dynamic Programming", "easy": 8, "medium": 15, "hard": 10}
    ]
    
    for topic in topics:
        st.markdown(f"""
        <div class="dashboard-card">
            <h4 style="color: #10a37f;">{topic['topic']}</h4>
            <p>Target: Easy({topic['easy']}) | Medium({topic['medium']}) | Hard({topic['hard']})</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            easy_done = st.number_input(f"Easy", 0, topic['easy'], 0, key=f"{topic['topic']}_easy")
        with col2:
            medium_done = st.number_input(f"Medium", 0, topic['medium'], 0, key=f"{topic['topic']}_medium")
        with col3:
            hard_done = st.number_input(f"Hard", 0, topic['hard'], 0, key=f"{topic['topic']}_hard")
    
    # Company Guide
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 🏢 **Company-specific Preparation**")
    
    companies = {
        "Google": {"difficulty": "Very High", "focus": "Algorithms, System Design", "rounds": "5-6 rounds"},
        "Microsoft": {"difficulty": "High", "focus": "Problem Solving, Design", "rounds": "4-5 rounds"},
        "Amazon": {"difficulty": "High", "focus": "Leadership Principles", "rounds": "4-6 rounds"},
        "TCS": {"difficulty": "Medium", "focus": "Programming Basics", "rounds": "3 rounds"},
        "Infosys": {"difficulty": "Medium", "focus": "Aptitude, Programming", "rounds": "3 rounds"}
    }
    
    selected_company = st.selectbox("Select target company:", list(companies.keys()))
    
    if selected_company:
        company_info = companies[selected_company]
        st.markdown(f"""
        <div class="dashboard-card">
            <h3 style="color: #10a37f;">{selected_company} Preparation Guide</h3>
            <p><strong>Difficulty:</strong> {company_info['difficulty']}</p>
            <p><strong>Focus Areas:</strong> {company_info['focus']}</p>
            <p><strong>Interview Rounds:</strong> {company_info['rounds']}</p>
        </div>
        """, unsafe_allow_html=True)
