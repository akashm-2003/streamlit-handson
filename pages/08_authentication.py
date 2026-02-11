import streamlit as st
import hashlib
import json
from datetime import datetime

st.set_page_config(
    page_title="Chapter 8: Authentication",
    page_icon="🔐",
    layout="wide"
)

# Initialize authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'users_db' not in st.session_state:
    # Simulated user database (in real apps, use actual database)
    st.session_state.users_db = {
        'admin': {
            'password': hashlib.sha256('admin123'.encode()).hexdigest(),
            'role': 'admin',
            'email': 'admin@example.com',
            'created': '2024-01-01'
        },
        'user1': {
            'password': hashlib.sha256('user123'.encode()).hexdigest(),
            'role': 'user',
            'email': 'user1@example.com',
            'created': '2024-01-15'
        }
    }

st.title("🔐 Chapter 8: User Authentication")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📖 Learn",
    "🔑 Login Demo",
    "🛡️ Protected Content",
    "🧪 Quiz"
])

# ============ TAB 1: LEARN ============
with tab1:
    st.header("Authentication Concepts")
    
    with st.expander("🔒 1. Password Hashing (Security)", expanded=True):
        st.markdown("""
        **Never store passwords in plain text!**
        
        Always hash passwords before storing them.
        """)
        
        st.code("""
import hashlib

# Hash a password
password = "mypassword123"
hashed = hashlib.sha256(password.encode()).hexdigest()

# Store the hashed password (not the original!)
print(hashed)  
# Output: 6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090

# To verify login:
input_password = "mypassword123"
input_hashed = hashlib.sha256(input_password.encode()).hexdigest()

if input_hashed == stored_hashed:
    print("Login successful!")
        """, language="python")
        
        st.warning("⚠️ **Security Note:** Use `bcrypt` or `argon2` in production for better security!")
    
    with st.expander("🔑 2. Simple Login System"):
        st.code("""
import streamlit as st
import hashlib

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'username' not in st.session_state:
    st.session_state.username = None

# Simulated user database
USERS = {
    'admin': hashlib.sha256('admin123'.encode()).hexdigest(),
    'user1': hashlib.sha256('user123'.encode()).hexdigest()
}

def login(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    if username in USERS and USERS[username] == hashed_password:
        st.session_state.authenticated = True
        st.session_state.username = username
        return True
    return False

def logout():
    st.session_state.authenticated = False
    st.session_state.username = None

# Login form
if not st.session_state.authenticated:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if login(username, password):
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials!")
else:
    st.success(f"Welcome, {st.session_state.username}!")
    if st.button("Logout"):
        logout()
        st.rerun()
        """, language="python")
    
    with st.expander("🛡️ 3. Protecting Pages"):
        st.markdown("""
        **Method 1: Check at Page Level**
        """)
        
        st.code("""
import streamlit as st

# At the top of your protected page
if not st.session_state.get('authenticated', False):
    st.warning("🔒 Please login to access this page")
    if st.button("Go to Login"):
        st.switch_page("pages/login.py")
    st.stop()  # Stop execution here

# Rest of your page (only runs if authenticated)
st.title("Protected Content")
st.write("Only logged-in users see this!")
        """, language="python")
        
        st.markdown("**Method 2: Authentication Decorator**")
        
        st.code("""
import streamlit as st
from functools import wraps

def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get('authenticated', False):
            st.error("🔒 Authentication required!")
            if st.button("Login"):
                st.switch_page("pages/login.py")
            st.stop()
        return func(*args, **kwargs)
    return wrapper

@require_auth
def protected_page():
    st.title("Admin Dashboard")
    st.write("Only authenticated users see this")

protected_page()
        """, language="python")
    
    with st.expander("👥 4. User Registration"):
        st.code("""
import streamlit as st
import hashlib

def register_user(username, password, email):
    # Check if username exists
    if username in st.session_state.users_db:
        return False, "Username already exists"
    
    # Validate input
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    # Hash password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Store user
    st.session_state.users_db[username] = {
        'password': hashed_password,
        'email': email,
        'role': 'user',
        'created': datetime.now().strftime('%Y-%m-%d')
    }
    
    return True, "Registration successful!"

# Registration form
with st.form("register_form"):
    st.subheader("Create Account")
    
    new_username = st.text_input("Username")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    submit = st.form_submit_button("Register")
    
    if submit:
        if new_password != confirm_password:
            st.error("Passwords don't match!")
        else:
            success, message = register_user(new_username, new_password, new_email)
            if success:
                st.success(message)
            else:
                st.error(message)
        """, language="python")
    
    with st.expander("🔐 5. Role-Based Access"):
        st.code("""
# Store user role during login
st.session_state.user_role = user_data['role']

# Check role before showing content
if st.session_state.get('user_role') == 'admin':
    st.button("Admin Panel")  # Only admins see this
    
elif st.session_state.get('user_role') == 'user':
    st.button("User Dashboard")  # Only regular users

# Or check multiple roles
allowed_roles = ['admin', 'manager']
if st.session_state.get('user_role') in allowed_roles:
    st.write("Management content")
        """, language="python")
    
    with st.expander("💡 6. Best Practices"):
        st.markdown("""
        **Security Best Practices:**
        
        ✅ **DO:**
        - Hash passwords (use `bcrypt` or `argon2` in production)
        - Use HTTPS in production
        - Implement rate limiting (prevent brute force)
        - Add password strength requirements
        - Use secure session management
        - Log authentication attempts
        - Implement "forgot password" functionality
        - Use environment variables for secrets
        
        ❌ **DON'T:**
        - Store passwords in plain text
        - Hardcode credentials in code
        - Share session tokens via URL
        - Allow weak passwords
        - Display detailed error messages (security risk)
        - Store sensitive data in session state without encryption
        """)

# ============ TAB 2: LOGIN DEMO ============
with tab2:
    st.header("🔑 Interactive Login Demo")
    
    # Show current authentication status
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.authenticated:
            st.success(f"✅ Logged in as: **{st.session_state.current_user}**")
        else:
            st.warning("🔒 Not logged in")
    
    with col2:
        if st.session_state.authenticated:
            user_data = st.session_state.users_db[st.session_state.current_user]
            st.info(f"👤 Role: **{user_data['role'].title()}**")
    
    st.markdown("---")
    
    # Main content based on authentication
    if not st.session_state.authenticated:
        # LOGIN SECTION
        st.subheader("🔐 Login")
        
        # Test credentials info
        with st.expander("ℹ️ Test Credentials", expanded=True):
            st.markdown("""
            **Available test accounts:**
            
            | Username | Password | Role |
            |----------|----------|------|
            | admin    | admin123 | Admin |
            | user1    | user123  | User |
            """)
        
        # Login form
        with st.form("login_form", clear_on_submit=True):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            
            col1, col2 = st.columns(2)
            
            with col1:
                submit = st.form_submit_button("🔑 Login", type="primary", use_container_width=True)
            
            with col2:
                register = st.form_submit_button("📝 Register", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("❌ Please fill in all fields")
                else:
                    # Hash input password
                    hashed_input = hashlib.sha256(password.encode()).hexdigest()
                    
                    # Check credentials
                    if username in st.session_state.users_db:
                        stored_hash = st.session_state.users_db[username]['password']
                        
                        if hashed_input == stored_hash:
                            # Login successful
                            st.session_state.authenticated = True
                            st.session_state.current_user = username
                            st.success("✅ Login successful!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Invalid password")
                    else:
                        st.error("❌ User not found")
            
            if register:
                st.info("👉 Registration form will appear below")
        
        st.markdown("---")
        
        # REGISTRATION SECTION
        st.subheader("📝 Create New Account")
        
        with st.form("register_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input("Username", key="reg_username")
                new_email = st.text_input("Email", key="reg_email")
            
            with col2:
                new_password = st.text_input("Password", type="password", key="reg_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            role = st.selectbox("Role", ["user", "admin"])
            
            register_submit = st.form_submit_button("📝 Create Account", type="primary")
            
            if register_submit:
                # Validation
                errors = []
                
                if not new_username or not new_password or not new_email:
                    errors.append("All fields are required")
                
                if new_username in st.session_state.users_db:
                    errors.append("Username already exists")
                
                if len(new_password) < 6:
                    errors.append("Password must be at least 6 characters")
                
                if new_password != confirm_password:
                    errors.append("Passwords don't match")
                
                if '@' not in new_email:
                    errors.append("Invalid email format")
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    # Register user
                    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                    
                    st.session_state.users_db[new_username] = {
                        'password': hashed_password,
                        'email': new_email,
                        'role': role,
                        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    st.success(f"✅ Account created successfully! You can now login with username: {new_username}")
                    st.balloons()
    
    else:
        # LOGGED IN - Show user dashboard
        st.subheader(f"👋 Welcome, {st.session_state.current_user}!")
        
        user_data = st.session_state.users_db[st.session_state.current_user]
        
        # User info card
        with st.container(border=True):
            st.markdown("### 👤 Profile Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Username:** {st.session_state.current_user}")
                st.write(f"**Email:** {user_data['email']}")
            
            with col2:
                st.write(f"**Role:** {user_data['role'].title()}")
                st.write(f"**Member since:** {user_data['created']}")
        
        st.markdown("---")
        
        # Role-specific content
        st.subheader("📊 Your Dashboard")
        
        if user_data['role'] == 'admin':
            with st.container(border=True):
                st.markdown("### 👑 Admin Panel")
                st.success("You have admin privileges!")
                
                st.write("**Admin Features:**")
                st.write("- View all users")
                st.write("- Manage permissions")
                st.write("- System settings")
                st.write("- Analytics dashboard")
                
                if st.button("👥 View All Users", use_container_width=True):
                    st.subheader("📋 All Users")
                    for username, data in st.session_state.users_db.items():
                        st.write(f"- **{username}** ({data['role']}) - {data['email']}")
        
        else:
            with st.container(border=True):
                st.markdown("### 👤 User Dashboard")
                st.info("Standard user access")
                
                st.write("**Available Features:**")
                st.write("- View your profile")
                st.write("- Edit settings")
                st.write("- Access standard features")
        
        st.markdown("---")
        
        # Logout button
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("🚪 Logout", type="secondary", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.current_user = None
                st.success("✅ Logged out successfully!")
                st.rerun()

# ============ TAB 3: PROTECTED CONTENT ============
with tab3:
    st.header("🛡️ Protected Content Demo")
    
    st.info("This section demonstrates how to protect content with authentication")
    
    # Check authentication
    if not st.session_state.authenticated:
        # NOT LOGGED IN
        st.warning("🔒 **Access Denied**")
        st.write("You must be logged in to view this content.")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("🔑 Go to Login", type="primary", use_container_width=True):
                st.info("👈 Please use the 'Login Demo' tab to login")
        
        st.markdown("---")
        
        # Show what's behind the lock
        with st.container(border=True):
            st.markdown("### 🔒 Locked Content Preview")
            st.write("*This is what you'll see after logging in:*")
            
            st.code("""
            🎯 Exclusive Features
            📊 Advanced Analytics
            💼 Business Reports  
            🎨 Premium Templates
            📈 Real-time Data
            """)
    
    else:
        # LOGGED IN - Show protected content
        st.success(f"✅ Access granted for **{st.session_state.current_user}**")
        
        user_data = st.session_state.users_db[st.session_state.current_user]
        
        st.markdown("---")
        
        # Protected content
        with st.container(border=True):
            st.markdown("### 🎯 Exclusive Content")
            st.write("Welcome to the members-only area!")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Premium Features", "10+")
            with col2:
                st.metric("Data Access", "Unlimited")
            with col3:
                st.metric("Support", "24/7")
        
        st.markdown("---")
        
        # Role-based protected content
        st.subheader("🔐 Role-Based Access")
        
        if user_data['role'] == 'admin':
            # ADMIN ONLY
            with st.container(border=True):
                st.markdown("### 👑 Admin-Only Section")
                st.error("⚠️ This section is only visible to administrators!")
                
                st.write("**Admin Tools:**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("👥 User Management", use_container_width=True):
                        st.info("Opening user management...")
                    
                    if st.button("📊 System Analytics", use_container_width=True):
                        st.info("Loading analytics...")
                
                with col2:
                    if st.button("⚙️ System Settings", use_container_width=True):
                        st.info("Opening settings...")
                    
                    if st.button("🔐 Security Logs", use_container_width=True):
                        st.info("Loading security logs...")
        
        else:
            # REGULAR USER
            with st.container(border=True):
                st.markdown("### 👤 User Content")
                st.info("Standard user features available")
                
                st.write("**Your Features:**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📊 My Dashboard", use_container_width=True):
                        st.info("Loading your dashboard...")
                    
                    if st.button("📁 My Files", use_container_width=True):
                        st.info("Opening your files...")
                
                with col2:
                    if st.button("⚙️ My Settings", use_container_width=True):
                        st.info("Opening your settings...")
                    
                    if st.button("📞 Support", use_container_width=True):
                        st.info("Contacting support...")
        
        st.markdown("---")
        
        # Code example
        with st.expander("💻 Protection Code Example"):
            st.code("""
# Protect entire page
if not st.session_state.get('authenticated', False):
    st.warning("🔒 Login required")
    st.stop()

# Your protected content here
st.title("Protected Page")

# Role-based protection
user_role = st.session_state.users_db[st.session_state.current_user]['role']

if user_role == 'admin':
    st.write("Admin-only content")
elif user_role == 'user':
    st.write("User content")
            """, language="python")

# ============ TAB 4: QUIZ ============
with tab4:
    st.header("🧪 Knowledge Check")
    
    q1 = st.radio(
        "Q1: Why should passwords be hashed?",
        [
            "To make them longer",
            "To prevent storing plain text passwords",
            "To make login faster"
        ]
    )
    
    q2 = st.radio(
        "Q2: Where should authentication state be stored?",
        ["Local variables", "st.session_state", "URL parameters"]
    )
    
    q3 = st.radio(
        "Q3: How to stop page execution if not authenticated?",
        ["return", "st.stop()", "break"]
    )
    
    q4 = st.checkbox("Q4: st.session_state.authenticated persists across pages")
    
    q5 = st.radio(
        "Q5: What library is recommended for password hashing in production?",
        ["hashlib", "bcrypt", "base64"]
    )
    
    if st.button("✅ Check Answers", type="primary"):
        score = 0
        feedback = []
        
        if q1 == "To prevent storing plain text passwords":
            score += 1
            feedback.append("✅ Q1: Correct! Never store plain text passwords")
        else:
            feedback.append("❌ Q1: Hashing prevents storing plain text")
        
        if q2 == "st.session_state":
            score += 1
            feedback.append("✅ Q2: Correct!")
        else:
            feedback.append("❌ Q2: Use st.session_state")
        
        if q3 == "st.stop()":
            score += 1
            feedback.append("✅ Q3: Correct!")
        else:
            feedback.append("❌ Q3: Use st.stop() to halt execution")
        
        if q4:
            score += 1
            feedback.append("✅ Q4: Correct! Session state is shared")
        else:
            feedback.append("❌ Q4: Session state persists across pages")
        
        if q5 == "bcrypt":
            score += 1
            feedback.append("✅ Q5: Correct! bcrypt is production-ready")
        else:
            feedback.append("❌ Q5: bcrypt is recommended for production")
        
        st.markdown("---")
        st.write(f"### 🎯 Score: {score}/5")
        
        for fb in feedback:
            st.write(fb)
        
        if score == 5:
            st.success("🎉 Excellent! You understand authentication!")
            st.balloons()
        elif score >= 3:
            st.info("👍 Good! Review security concepts.")
        else:
            st.warning("📖 Please review authentication concepts.")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 7 - Custom Navigation")
with col2:
    st.info("➡️ **Next:** Chapter 9 - Role-Based Access Control")