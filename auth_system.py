import streamlit as st
import random
import re
from datetime import datetime, timedelta
import hashlib

# Simulated user database (in production, use a real database)
USER_DATABASE = {
    "students": {},
    "emails": {},
    "phones": {}
}

class AuthSystem:
    def __init__(self):
        self.otp_storage = {}
    
    def is_valid_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def is_valid_phone(self, phone):
        """Validate phone number (Indian format)"""
        pattern = r'^[6-9]\d{9}$'
        cleaned_phone = re.sub(r'[^\d]', '', phone)
        return len(cleaned_phone) == 10 and re.match(pattern, cleaned_phone)
    
    def generate_otp(self):
        """Generate 6-digit OTP"""
        return f"{random.randint(100000, 999999)}"
    
    def send_otp(self, phone):
        """Simulate OTP sending"""
        otp = self.generate_otp()
        self.otp_storage[phone] = {
            'otp': otp,
            'timestamp': datetime.now(),
            'attempts': 0
        }
        # In production, integrate with SMS service like Twilio
        st.success(f"📱 OTP sent to {phone}! (Demo OTP: {otp})")
        return True
    
    def verify_otp(self, phone, entered_otp):
        """Verify OTP"""
        if phone not in self.otp_storage:
            return False, "OTP not found. Please request a new one."
        
        stored = self.otp_storage[phone]
        
        # Check if OTP is expired (5 minutes)
        if datetime.now() - stored['timestamp'] > timedelta(minutes=5):
            del self.otp_storage[phone]
            return False, "OTP expired. Please request a new one."
        
        # Check attempts
        if stored['attempts'] >= 3:
            del self.otp_storage[phone]
            return False, "Too many attempts. Please request a new OTP."
        
        stored['attempts'] += 1
        
        if stored['otp'] == entered_otp:
            del self.otp_storage[phone]
            return True, "OTP verified successfully!"
        
        return False, f"Invalid OTP. {3 - stored['attempts']} attempts remaining."
    
    def register_user(self, method, identifier, password=None, name=None):
        """Register new user"""
        user_id = f"user_{len(USER_DATABASE['students']) + 1}"
        
        user_data = {
            'id': user_id,
            'name': name or identifier.split('@')[0],
            'created_at': datetime.now().isoformat(),
            'last_login': datetime.now().isoformat(),
            'auth_method': method
        }
        
        if method == 'email':
            if identifier in USER_DATABASE['emails']:
                return False, "Email already registered!"
            USER_DATABASE['emails'][identifier] = {
                'password': hashlib.sha256(password.encode()).hexdigest(),
                'user_id': user_id
            }
        elif method == 'phone':
            if identifier in USER_DATABASE['phones']:
                return False, "Phone number already registered!"
            USER_DATABASE['phones'][identifier] = {'user_id': user_id}
        
        USER_DATABASE['students'][user_id] = user_data
        return True, f"Account created successfully! Welcome, {user_data['name']}!"
    
    def authenticate_email(self, email, password):
        """Authenticate with email/password"""
        if email not in USER_DATABASE['emails']:
            return False, "Email not found!", None
        
        stored_password = USER_DATABASE['emails'][email]['password']
        entered_password = hashlib.sha256(password.encode()).hexdigest()
        
        if stored_password == entered_password:
            user_id = USER_DATABASE['emails'][email]['user_id']
            user = USER_DATABASE['students'][user_id]
            user['last_login'] = datetime.now().isoformat()
            return True, "Login successful!", user
        
        return False, "Invalid password!", None
    
    def authenticate_phone(self, phone):
        """Authenticate with phone (after OTP verification)"""
        if phone not in USER_DATABASE['phones']:
            return False, "Phone number not found!", None
        
        user_id = USER_DATABASE['phones'][phone]['user_id']
        user = USER_DATABASE['students'][user_id]
        user['last_login'] = datetime.now().isoformat()
        return True, "Login successful!", user

# Initialize auth system
auth = AuthSystem()

def show_professional_login():
    """Show professional login interface"""
    
    st.markdown("""
    <style>
        .auth-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 40px 30px;
            background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
            border-radius: 16px;
            border: 2px solid #10a37f;
            box-shadow: 0 20px 60px rgba(16, 163, 127, 0.2);
        }
        
        .auth-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .auth-title {
            font-size: 1.8em;
            font-weight: 700;
            color: #10a37f;
            margin-bottom: 8px;
        }
        
        .auth-subtitle {
            color: #a0aec0;
            font-size: 0.95em;
        }
        
        .auth-tabs {
            display: flex;
            background: #333;
            border-radius: 8px;
            margin-bottom: 25px;
            padding: 4px;
        }
        
        .auth-tab {
            flex: 1;
            padding: 10px;
            text-align: center;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .auth-tab.active {
            background: #10a37f;
            color: white;
        }
        
        .auth-tab:not(.active) {
            color: #a0aec0;
        }
        
        .oauth-button {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border: 1px solid #555;
            border-radius: 8px;
            background: #333;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .oauth-button:hover {
            background: #444;
            border-color: #10a37f;
        }
        
        .oauth-button.google {
            background: #4285f4;
            border-color: #4285f4;
        }
        
        .oauth-button.google:hover {
            background: #3367d6;
        }
        
        .divider {
            text-align: center;
            margin: 20px 0;
            position: relative;
            color: #666;
        }
        
        .divider::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 1px;
            background: #444;
        }
        
        .divider span {
            background: #1a1a1a;
            padding: 0 15px;
            font-size: 0.9em;
        }
        
        .auth-form {
            margin-top: 15px;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-label {
            display: block;
            margin-bottom: 5px;
            color: #a0aec0;
            font-size: 0.9em;
            font-weight: 500;
        }
        
        .form-input {
            width: 100%;
            padding: 12px;
            border: 1px solid #555;
            border-radius: 8px;
            background: #2d2d2d;
            color: white;
            font-size: 14px;
        }
        
        .form-input:focus {
            border-color: #10a37f;
            outline: none;
            box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.2);
        }
        
        .auth-submit {
            width: 100%;
            padding: 12px;
            background: #10a37f;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .auth-submit:hover {
            background: #0d8f6b;
            transform: translateY(-1px);
        }
        
        .auth-footer {
            text-align: center;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #333;
        }
        
        .auth-link {
            color: #10a37f;
            text-decoration: none;
            font-weight: 500;
        }
        
        .auth-link:hover {
            text-decoration: underline;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'  # login or register
    if 'auth_method' not in st.session_state:
        st.session_state.auth_method = 'email'  # email, phone, or google
    if 'otp_sent' not in st.session_state:
        st.session_state.otp_sent = False
    if 'phone_for_otp' not in st.session_state:
        st.session_state.phone_for_otp = ""
    
    # Auth container
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="auth-header">
        <div class="auth-title">Welcome Back!</div>
        <div class="auth-subtitle">Sign in to access your personalized career dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login/Register Toggle
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign In", key="login_tab", use_container_width=True, 
                    type="primary" if st.session_state.auth_mode == 'login' else "secondary"):
            st.session_state.auth_mode = 'login'
            st.session_state.otp_sent = False
            st.rerun()
    
    with col2:
        if st.button("Sign Up", key="register_tab", use_container_width=True,
                    type="primary" if st.session_state.auth_mode == 'register' else "secondary"):
            st.session_state.auth_mode = 'register'
            st.session_state.otp_sent = False
            st.rerun()
    
    # OAuth Buttons
    st.markdown('<div class="divider"><span>Continue with</span></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌐 Google", key="google_auth", use_container_width=True):
            # Simulate Google OAuth
            st.session_state.authenticated = True
            st.session_state.username = "Google User"
            st.session_state.user_email = "user@gmail.com"
            st.success("✅ Signed in with Google!")
            st.rerun()
    
    with col2:
        if st.button("📱 Demo Login", key="demo_auth", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.username = "Demo User"
            st.success("✅ Demo access granted!")
            st.rerun()
    
    st.markdown('<div class="divider"><span>Or continue with</span></div>', unsafe_allow_html=True)
    
    # Method Selection
    tab1, tab2 = st.columns(2)
    with tab1:
        if st.button("📧 Email", key="email_method", use_container_width=True,
                    type="primary" if st.session_state.auth_method == 'email' else "secondary"):
            st.session_state.auth_method = 'email'
            st.session_state.otp_sent = False
            st.rerun()
    
    with tab2:
        if st.button("📱 Phone", key="phone_method", use_container_width=True,
                    type="primary" if st.session_state.auth_method == 'phone' else "secondary"):
            st.session_state.auth_method = 'phone'
            st.session_state.otp_sent = False
            st.rerun()
    
    st.markdown("---")
    
    # Email Authentication
    if st.session_state.auth_method == 'email':
        if st.session_state.auth_mode == 'login':
            st.markdown("### 📧 Sign In with Email")
            
            email = st.text_input("Email Address", placeholder="Enter your email", key="login_email")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button("🚀 Sign In", key="email_signin", use_container_width=True, type="primary"):
                    if not email or not password:
                        st.error("❌ Please fill in all fields!")
                    elif not auth.is_valid_email(email):
                        st.error("❌ Please enter a valid email address!")
                    else:
                        success, message, user = auth.authenticate_email(email, password)
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.username = user['name']
                            st.session_state.user_email = email
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
            
            with col2:
                if st.button("Forgot?", key="forgot_password", use_container_width=True):
                    st.info("🔄 Password reset feature coming soon!")
        
        else:  # Register mode
            st.markdown("### 📧 Create Account with Email")
            
            name = st.text_input("Full Name", placeholder="Enter your full name", key="register_name")
            email = st.text_input("Email Address", placeholder="Enter your email", key="register_email")
            password = st.text_input("Password", type="password", placeholder="Create a password (min 6 chars)", key="register_password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="confirm_password")
            
            if st.button("🎯 Create Account", key="email_register", use_container_width=True, type="primary"):
                if not all([name, email, password, confirm_password]):
                    st.error("❌ Please fill in all fields!")
                elif not auth.is_valid_email(email):
                    st.error("❌ Please enter a valid email address!")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters!")
                elif password != confirm_password:
                    st.error("❌ Passwords do not match!")
                else:
                    success, message = auth.register_user('email', email, password, name)
                    if success:
                        st.success(f"✅ {message}")
                        st.session_state.auth_mode = 'login'
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
    
    # Phone Authentication
    elif st.session_state.auth_method == 'phone':
        if not st.session_state.otp_sent:
            st.markdown("### 📱 Sign In with Phone")
            
            phone = st.text_input("Phone Number", placeholder="Enter 10-digit mobile number", key="phone_input", max_chars=10)
            
            if st.session_state.auth_mode == 'register':
                name = st.text_input("Full Name", placeholder="Enter your full name", key="phone_register_name")
            
            if st.button("📨 Send OTP", key="send_otp", use_container_width=True, type="primary"):
                if not phone:
                    st.error("❌ Please enter your phone number!")
                elif not auth.is_valid_phone(phone):
                    st.error("❌ Please enter a valid 10-digit phone number!")
                else:
                    if st.session_state.auth_mode == 'register':
                        if not name:
                            st.error("❌ Please enter your name!")
                            return
                        success, message = auth.register_user('phone', phone, name=name)
                        if not success and "already registered" not in message:
                            st.error(f"❌ {message}")
                            return
                    
                    if auth.send_otp(phone):
                        st.session_state.otp_sent = True
                        st.session_state.phone_for_otp = phone
                        st.rerun()
        
        else:
            st.markdown(f"### 🔐 Enter OTP sent to {st.session_state.phone_for_otp}")
            
            otp = st.text_input("OTP", placeholder="Enter 6-digit OTP", key="otp_input", max_chars=6)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button("✅ Verify OTP", key="verify_otp", use_container_width=True, type="primary"):
                    if not otp:
                        st.error("❌ Please enter the OTP!")
                    elif len(otp) != 6:
                        st.error("❌ OTP must be 6 digits!")
                    else:
                        success, message = auth.verify_otp(st.session_state.phone_for_otp, otp)
                        if success:
                            # Authenticate user
                            auth_success, auth_message, user = auth.authenticate_phone(st.session_state.phone_for_otp)
                            if auth_success:
                                st.session_state.authenticated = True
                                st.session_state.username = user['name']
                                st.session_state.user_phone = st.session_state.phone_for_otp
                                st.success(f"✅ {message}")
                                st.rerun()
                            else:
                                st.error(f"❌ {auth_message}")
                        else:
                            st.error(f"❌ {message}")
            
            with col2:
                if st.button("🔄 Resend", key="resend_otp", use_container_width=True):
                    if auth.send_otp(st.session_state.phone_for_otp):
                        st.info("📨 New OTP sent!")
    
    # Back to app button
    st.markdown("---")
    if st.button("⬅️ Back to App", key="back_to_app", use_container_width=True):
        st.session_state.show_login_modal = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def get_user_info():
    """Get current user information"""
    if st.session_state.authenticated:
        return {
            'name': st.session_state.username,
            'email': getattr(st.session_state, 'user_email', None),
            'phone': getattr(st.session_state, 'user_phone', None),
            'avatar': st.session_state.username[0].upper() if st.session_state.username else 'U'
        }
    return None
