import streamlit as st

def show():
    """📚 Learning Paths Dashboard"""
    
    st.markdown("""
    <div class="dashboard-header">
        <h1 style="color: #10a37f; margin: 0;">📚 Learning Paths Dashboard</h1>
        <p style="margin: 10px 0 0 0; color: #a0aec0;">Curated learning roadmaps for tech careers</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Learning Path Selector
    st.markdown("## 🛣️ **Choose Your Learning Path**")
    
    selected_path = st.selectbox(
        "Select a career path for detailed roadmap:",
        ["Full Stack Development", "Data Science", "AI/ML Engineering", "DevOps", "Mobile Development", "Cybersecurity"]
    )
    
    # Learning Paths Data
    learning_paths = {
        "Full Stack Development": {
            "duration": "6 months", "difficulty": "Intermediate",
            "phases": [
                {"phase": "Frontend Basics", "duration": "2 months", 
                 "topics": ["HTML5 & CSS3", "JavaScript ES6+", "Responsive Design"],
                 "projects": ["Portfolio Website", "Calculator App", "To-do List"]},
                {"phase": "React.js", "duration": "2 months",
                 "topics": ["Components", "State Management", "Hooks", "Router"],
                 "projects": ["Weather App", "Movie Database", "E-commerce Frontend"]},
                {"phase": "Backend", "duration": "2 months",
                 "topics": ["Node.js", "Express.js", "MongoDB", "APIs"],
                 "projects": ["REST API", "Authentication System", "Full Stack App"]}
            ]
        },
        "Data Science": {
            "duration": "8 months", "difficulty": "Advanced",
            "phases": [
                {"phase": "Python & Math", "duration": "2 months",
                 "topics": ["Python Programming", "Statistics", "Linear Algebra"],
                 "projects": ["Data Analysis Scripts", "Statistical Models"]},
                {"phase": "Data Analysis", "duration": "3 months",
                 "topics": ["Pandas", "NumPy", "Matplotlib", "Data Cleaning"],
                 "projects": ["Sales Analysis", "Customer Segmentation"]},
                {"phase": "Machine Learning", "duration": "3 months",
                 "topics": ["Scikit-learn", "Model Training", "Feature Engineering"],
                 "projects": ["Prediction Models", "Classification Tasks"]}
            ]
        },
        "AI/ML Engineering": {
            "duration": "10 months", "difficulty": "Expert",
            "phases": [
                {"phase": "Foundation", "duration": "3 months",
                 "topics": ["Python", "Mathematics", "Statistics"],
                 "projects": ["Basic ML Models", "Data Preprocessing"]},
                {"phase": "Deep Learning", "duration": "4 months",
                 "topics": ["TensorFlow", "PyTorch", "Neural Networks"],
                 "projects": ["Image Classification", "NLP Models"]},
                {"phase": "MLOps", "duration": "3 months",
                 "topics": ["Model Deployment", "Docker", "Cloud Platforms"],
                 "projects": ["Production ML Pipeline", "Model Monitoring"]}
            ]
        }
    }
    
    if selected_path in learning_paths:
        path_data = learning_paths[selected_path]
        
        # Path Overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Duration", path_data["duration"])
        with col2:
            st.metric("Difficulty", path_data["difficulty"])
        with col3:
            st.metric("Career Outcome", f"{selected_path} Role")
        
        # Detailed Phases
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown("## 📋 **Detailed Learning Roadmap**")
        
        for i, phase in enumerate(path_data["phases"]):
            st.markdown(f"""
            <div class="dashboard-card">
                <h3 style="color: #10a37f;">Phase {i+1}: {phase['phase']} ({phase['duration']})</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
                    <div>
                        <h4 style="color: #a0aec0;">📖 Topics to Learn:</h4>
                        <ul>
            """, unsafe_allow_html=True)
            
            for topic in phase["topics"]:
                st.markdown(f"<li>{topic}</li>", unsafe_allow_html=True)
            
            st.markdown(f"""
                        </ul>
                    </div>
                    <div>
                        <h4 style="color: #a0aec0;">🚀 Projects:</h4>
                        <ul>
            """, unsafe_allow_html=True)
            
            for project in phase["projects"]:
                st.markdown(f"<li>{project}</li>", unsafe_allow_html=True)
            
            st.markdown("""
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Progress Tracker
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 📈 **Track Your Progress**")
    
    progress_topics = ["HTML/CSS", "JavaScript", "React.js", "Node.js", "Databases", "APIs", "Testing", "Deployment"]
    
    col1, col2 = st.columns(2)
    for i, topic in enumerate(progress_topics):
        column = col1 if i % 2 == 0 else col2
        with column:
            progress = st.slider(f"📚 {topic}", 0, 100, 0, key=f"progress_{i}")
            if progress >= 80:
                st.success(f"✅ {topic} - Mastered!")
            elif progress >= 50:
                st.warning(f"⚡ {topic} - In Progress")
            elif progress > 0:
                st.info(f"🚀 {topic} - Getting Started")
