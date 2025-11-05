def get_main_css():
    return """
<style>
    .main .block-container { 
        padding-top: 0rem !important; 
        padding-left: 1rem !important; 
        padding-right: 1rem !important; 
        margin-top: 0rem !important;
    }
    .stApp > header { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    .stDeployButton { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    
    body { 
        background: #212121 !important; 
        color: white !important; 
        margin: 0 !important;
        padding: 0 !important;
    }
    .stApp { 
        background: #212121 !important; 
        margin-top: -60px !important;
    }
    
    div[data-testid="stVerticalBlock"] { gap: 0.5rem !important; }
    
    .header { 
        background: linear-gradient(135deg, #303030, #424242); 
        padding: 15px; 
        text-align: center; 
        font-weight: bold; 
        border-bottom: 3px solid #10a37f; 
        font-size: 18px;
        margin: 0 -1rem 1rem -1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .stColumns { gap: 0.5rem !important; }
    
    .stButton > button { 
        background: linear-gradient(135deg, #424242, #525252) !important; 
        color: white !important; 
        border: 1px solid #555 !important; 
        width: 100% !important;
        height: 60px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 10px !important;
        transition: all 0.3s ease !important;
        margin: 2px !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.3) !important;
    }
    
    .stButton > button:hover { 
        background: linear-gradient(135deg, #10a37f, #0d8f6b) !important; 
        transform: translateY(-1px) !important;
        box-shadow: 0 5px 15px rgba(16, 163, 127, 0.4) !important;
    }
    
    .dashboard-header {
        background: linear-gradient(135deg, #1a202c, #2d3748);
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #10a37f;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(16, 163, 127, 0.2);
    }
    
    .dashboard-card {
        background: linear-gradient(135deg, #303030, #424242);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #10a37f;
        margin: 12px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #10a37f, transparent);
        margin: 25px 0;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #303030, #424242) !important;
        border: 1px solid #555 !important;
        border-radius: 8px !important;
        padding: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        margin: 6px !important;
    }
    
    @media (max-width: 768px) {
        .header { font-size: 16px !important; padding: 12px !important; }
        .stButton > button { height: 50px !important; font-size: 9px !important; }
        .stColumn { min-width: 30% !important; }
    }
</style>
"""
