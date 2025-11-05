import streamlit as st

def show():
    """🎓 DIET Guide Dashboard"""
    
    st.markdown("""
    <div class="dashboard-header">
        <h1 style="color: #10a37f; margin: 0;">🎓 DIET Guide Dashboard</h1>
        <p style="margin: 10px 0 0 0; color: #a0aec0;">Complete placement and career guidance for DIET students</p>
    </div>
    """, unsafe_allow_html=True)
    
    # DIET Stats
    st.markdown("## 🏫 **DIET Placement Statistics**")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Placement Rate", "78%", "+5% YoY")
    with col2:
        st.metric("Average Package", "₹6.2 LPA", "+12%")
    with col3:
        st.metric("Top Package", "₹25 LPA", "2024")
    with col4:
        st.metric("Companies Visited", "120+", "2024")
    
    # Top Companies
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 🏢 **Top Recruiting Companies**")
    
    companies = [
        {"company": "TCS", "package": "₹3.5-7 LPA", "hiring": "120+ students", "roles": "Software Engineer, System Engineer"},
        {"company": "Infosys", "package": "₹4-8 LPA", "hiring": "80+ students", "roles": "Software Developer, Consultant"},
        {"company": "Wipro", "package": "₹3.5-6.5 LPA", "hiring": "60+ students", "roles": "Project Engineer, Developer"},
        {"company": "Accenture", "package": "₹4.5-9 LPA", "hiring": "45+ students", "roles": "Associate Software Engineer"},
        {"company": "Cognizant", "package": "₹4-7.5 LPA", "hiring": "55+ students", "roles": "Programmer Analyst"},
        {"company": "IBM", "package": "₹5-12 LPA", "hiring": "25+ students", "roles": "Application Developer"},
        {"company": "Amazon", "package": "₹15-25 LPA", "hiring": "5-8 students", "roles": "SDE I"}
    ]
    
    for company in companies:
        st.markdown(f"""
        <div class="dashboard-card">
            <div style="display: grid; grid-template-columns: 1fr 2fr 1fr 1fr; gap: 15px; align-items: center;">
                <div>
                    <h4 style="color: #10a37f; margin: 0;">{company['company']}</h4>
                </div>
                <div>
                    <strong>Roles:</strong> {company['roles']}
                </div>
                <div>
                    <strong>Package:</strong> {company['package']}
                </div>
                <div>
                    <strong>Hiring:</strong> {company['hiring']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Placement Strategy
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 📋 **Placement Preparation Timeline**")
    
    timeline = [
        {"phase": "Pre-Final Year", "timeline": "3rd Year", 
         "tasks": ["Build programming foundation", "Complete 2-3 projects", "Start competitive programming", "Maintain good CGPA"]},
        {"phase": "Final Year - Phase 1", "timeline": "June-August",
         "tasks": ["Resume preparation", "Mock interviews", "Advanced DSA practice", "Internship completion"]},
        {"phase": "Final Year - Phase 2", "timeline": "September-December", 
         "tasks": ["Company applications", "Aptitude preparation", "HR interview skills", "Final preparations"]}
    ]
    
    for phase in timeline:
        st.markdown(f"""
        <div class="dashboard-card">
            <h3 style="color: #10a37f;">{phase['phase']} ({phase['timeline']})</h3>
            <div style="margin-top: 15px;">
                <h4 style="color: #a0aec0;">🎯 Key Tasks:</h4>
                <ul>
        """, unsafe_allow_html=True)
        
        for task in phase["tasks"]:
            st.markdown(f"<li>{task}</li>", unsafe_allow_html=True)
        
        st.markdown("""
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Branch-wise Guidance
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 🎯 **Branch-wise Career Guidance**")
    
    branches = {
        "Computer Science": {"companies": "Google, Microsoft, Amazon", "avg_package": "₹6-15 LPA", "tips": "Focus on DSA and system design"},
        "Information Technology": {"companies": "TCS, Infosys, IBM", "avg_package": "₹5-12 LPA", "tips": "Learn cloud and database technologies"},
        "Electronics & Communication": {"companies": "Intel, Qualcomm, Samsung", "avg_package": "₹4-10 LPA", "tips": "Combine hardware with programming"},
        "Mechanical Engineering": {"companies": "Tata, Mahindra, L&T", "avg_package": "₹3.5-8 LPA", "tips": "Focus on automation and Industry 4.0"}
    }
    
    selected_branch = st.selectbox("Select your branch:", list(branches.keys()))
    
    if selected_branch:
        branch_info = branches[selected_branch]
        st.markdown(f"""
        <div class="dashboard-card">
            <h3 style="color: #10a37f;">{selected_branch}</h3>
            <p><strong>🏢 Top Companies:</strong> {branch_info['companies']}</p>
            <p><strong>💰 Average Package:</strong> {branch_info['avg_package']}</p>
            <p><strong>💡 Key Tips:</strong> {branch_info['tips']}</p>
        </div>
        """, unsafe_allow_html=True)
