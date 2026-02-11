import streamlit as st
from functools import wraps
import hashlib

st.set_page_config(
    page_title="Chapter 9: Access Control",
    page_icon="🛡️",
    layout="wide"
)

# Initialize RBAC system
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'user_role' not in st.session_state:
    st.session_state.user_role = None

if 'users_db' not in st.session_state:
    # Enhanced user database with roles
    st.session_state.users_db = {
        'admin': {
            'password': hashlib.sha256('admin123'.encode()).hexdigest(),
            'role': 'admin',
            'email': 'admin@company.com',
            'permissions': ['read', 'write', 'delete', 'manage_users', 'view_analytics']
        },
        'manager': {
            'password': hashlib.sha256('manager123'.encode()).hexdigest(),
            'role': 'manager',
            'email': 'manager@company.com',
            'permissions': ['read', 'write', 'view_analytics']
        },
        'user': {
            'password': hashlib.sha256('user123'.encode()).hexdigest(),
            'role': 'user',
            'email': 'user@company.com',
            'permissions': ['read', 'write']
        },
        'viewer': {
            'password': hashlib.sha256('viewer123'.encode()).hexdigest(),
            'role': 'viewer',
            'email': 'viewer@company.com',
            'permissions': ['read']
        }
    }

# Define role hierarchy and permissions
ROLE_PERMISSIONS = {
    'admin': ['read', 'write', 'delete', 'manage_users', 'view_analytics', 'system_settings'],
    'manager': ['read', 'write', 'view_analytics', 'manage_team'],
    'user': ['read', 'write', 'edit_profile'],
    'viewer': ['read']
}

# Page access control
PAGE_ACCESS = {
    'home': ['admin', 'manager', 'user', 'viewer'],
    'dashboard': ['admin', 'manager', 'user'],
    'analytics': ['admin', 'manager'],
    'users': ['admin'],
    'settings': ['admin']
}

st.title("🛡️ Chapter 9: Role-Based Access Control")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📖 Learn",
    "🔑 RBAC Demo",
    "🎯 Permissions Test",
    "🧪 Quiz"
])

# ============ TAB 1: LEARN ============
with tab1:
    st.header("RBAC Concepts")
    
    with st.expander("🏗️ 1. What is RBAC?", expanded=True):
        st.markdown("""
        **Role-Based Access Control (RBAC)** restricts system access based on user roles.
        
        **Key Concepts:**
        - **Users** have **Roles**
        - **Roles** have **Permissions**
        - **Permissions** control **Access to Features/Pages**
        
        **Example:**
```
        User: John Doe
          ↓
        Role: Manager
          ↓
        Permissions: [read, write, view_analytics]
          ↓
        Can Access: Home, Dashboard, Analytics
        Cannot Access: User Management, System Settings
```
        """)
        
        st.info("💡 **Benefit:** Centralized permission management - change role permissions to affect all users with that role!")
    
    with st.expander("👥 2. Role Hierarchy"):
        st.markdown("""
        **Common Role Structure:**
```
        Admin (Full Access)
          ↓
        Manager (Department Access)
          ↓
        User (Standard Access)
          ↓
        Viewer (Read-Only Access)
```
        
        **Permission Inheritance:**
        - Admin can do everything Manager can do + more
        - Manager can do everything User can do + more
        - User can do everything Viewer can do + more
        """)
        
        st.code("""
ROLE_HIERARCHY = {
    'admin': 4,      # Highest
    'manager': 3,
    'user': 2,
    'viewer': 1      # Lowest
}

def can_access(user_role, required_role):
    return ROLE_HIERARCHY[user_role] >= ROLE_HIERARCHY[required_role]
        """, language="python")
    
    with st.expander("🔐 3. Implementing RBAC"):
        st.markdown("**Step 1: Define Permissions**")
        
        st.code("""
# Define what each role can do
ROLE_PERMISSIONS = {
    'admin': ['read', 'write', 'delete', 'manage_users', 'settings'],
    'manager': ['read', 'write', 'view_reports'],
    'user': ['read', 'write'],
    'viewer': ['read']
}
        """, language="python")
        
        st.markdown("**Step 2: Check Permissions**")
        
        st.code("""
def has_permission(user, permission):
    user_role = st.session_state.user_role
    return permission in ROLE_PERMISSIONS.get(user_role, [])

# Usage
if has_permission(user, 'delete'):
    st.button("🗑️ Delete")
        """, language="python")
        
        st.markdown("**Step 3: Protect Pages**")
        
        st.code("""
def require_role(allowed_roles):
    user_role = st.session_state.get('user_role')
    
    if not st.session_state.get('authenticated', False):
        st.error("🔒 Login required")
        st.stop()
    
    if user_role not in allowed_roles:
        st.error(f"🚫 Access denied. Required roles: {', '.join(allowed_roles)}")
        st.stop()

# Usage at top of page
require_role(['admin', 'manager'])
        """, language="python")
    
    with st.expander("🎨 4. Dynamic UI Based on Role"):
        st.code("""
import streamlit as st

user_role = st.session_state.get('user_role')

# Show different navigation based on role
if user_role == 'admin':
    # Admin sees everything
    st.button("👥 Users")
    st.button("📊 Analytics")
    st.button("⚙️ Settings")
    st.button("🏠 Home")

elif user_role == 'manager':
    # Manager sees limited options
    st.button("📊 Analytics")
    st.button("👥 My Team")
    st.button("🏠 Home")

elif user_role == 'user':
    # Regular user sees basic options
    st.button("📊 Dashboard")
    st.button("👤 Profile")
    st.button("🏠 Home")

else:  # viewer
    # Viewer sees minimal options
    st.button("📖 View Only")
    st.button("🏠 Home")
        """, language="python")
    
    with st.expander("🔧 5. Permission Decorator Pattern"):
        st.code("""
from functools import wraps
import streamlit as st

def require_permission(permission):
    '''Decorator to check if user has specific permission'''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = st.session_state.get('user_role')
            
            if not user_role:
                st.error("🔒 Authentication required")
                return None
            
            user_permissions = ROLE_PERMISSIONS.get(user_role, [])
            
            if permission not in user_permissions:
                st.error(f"🚫 Permission denied: {permission}")
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@require_permission('delete')
def delete_user(user_id):
    st.success(f"Deleted user {user_id}")

@require_permission('manage_users')
def show_user_management():
    st.title("User Management")
    # ... management UI
        """, language="python")
    
    with st.expander("💡 6. Best Practices"):
        st.markdown("""
        **✅ DO:**
        - Define clear role hierarchy
        - Use principle of least privilege (minimal permissions by default)
        - Check permissions on both frontend AND backend
        - Log permission checks and denials
        - Make roles configurable (not hardcoded)
        - Test with each role regularly
        - Document what each role can do
        
        **❌ DON'T:**
        - Rely only on UI hiding (always check on backend too)
        - Give users more permissions than needed
        - Hardcode role checks everywhere (use decorators/functions)
        - Forget to check permissions on API endpoints
        - Allow users to change their own roles
        - Expose sensitive error messages
        """)

# ============ TAB 2: RBAC DEMO ============
with tab2:
    st.header("🔑 RBAC System Demo")
    
    # Show authentication status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.authenticated:
            st.success(f"✅ User: **{st.session_state.current_user}**")
        else:
            st.warning("🔒 Not logged in")
    
    with col2:
        if st.session_state.user_role:
            st.info(f"👤 Role: **{st.session_state.user_role.title()}**")
        else:
            st.info("👤 Role: None")
    
    with col3:
        if st.session_state.user_role:
            permissions = ROLE_PERMISSIONS.get(st.session_state.user_role, [])
            st.info(f"🔑 Permissions: **{len(permissions)}**")
    
    st.markdown("---")
    
    # Login section if not authenticated
    if not st.session_state.authenticated:
        st.subheader("🔐 Login to Test RBAC")
        
        # Test accounts info
        with st.expander("ℹ️ Test Accounts", expanded=True):
            st.markdown("""
            | Username | Password | Role | Permissions |
            |----------|----------|------|-------------|
            | admin | admin123 | Admin | Full access |
            | manager | manager123 | Manager | Limited management |
            | user | user123 | User | Standard features |
            | viewer | viewer123 | Viewer | Read-only |
            """)
        
        # Login form
        with st.form("rbac_login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            submit = st.form_submit_button("🔑 Login", type="primary", use_container_width=True)
            
            if submit:
                if username in st.session_state.users_db:
                    hashed_input = hashlib.sha256(password.encode()).hexdigest()
                    stored_hash = st.session_state.users_db[username]['password']
                    
                    if hashed_input == stored_hash:
                        st.session_state.authenticated = True
                        st.session_state.current_user = username
                        st.session_state.user_role = st.session_state.users_db[username]['role']
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid password")
                else:
                    st.error("❌ User not found")
    
    else:
        # Show role-based dashboard
        st.subheader(f"👋 Welcome, {st.session_state.current_user}!")
        
        user_data = st.session_state.users_db[st.session_state.current_user]
        role = user_data['role']
        permissions = user_data['permissions']
        
        # User info card
        with st.container(border=True):
            st.markdown("### 👤 Your Access Level")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Role:** {role.title()}")
                st.write(f"**Email:** {user_data['email']}")
            
            with col2:
                st.write(f"**Permissions:** {len(permissions)}")
                with st.expander("View Permissions"):
                    for perm in permissions:
                        st.write(f"✓ {perm}")
        
        st.markdown("---")
        
        # Role-specific dashboards
        if role == 'admin':
            # ADMIN DASHBOARD
            st.markdown("### 👑 Admin Dashboard")
            st.error("⚠️ FULL ACCESS - ALL FEATURES AVAILABLE")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                with st.container(border=True):
                    st.markdown("**👥 User Management**")
                    if st.button("Manage Users", use_container_width=True):
                        st.info("✅ Access granted")
                        st.write(f"Total users: {len(st.session_state.users_db)}")
            
            with col2:
                with st.container(border=True):
                    st.markdown("**📊 Analytics**")
                    if st.button("View Analytics", use_container_width=True):
                        st.info("✅ Access granted")
                        st.metric("Active Users", len(st.session_state.users_db))
            
            with col3:
                with st.container(border=True):
                    st.markdown("**⚙️ System Settings**")
                    if st.button("Open Settings", use_container_width=True):
                        st.info("✅ Access granted")
                        st.write("System configuration options")
        
        elif role == 'manager':
            # MANAGER DASHBOARD
            st.markdown("### 👔 Manager Dashboard")
            st.warning("⚠️ MANAGER ACCESS - LIMITED FEATURES")
            
            col1, col2 = st.columns(2)
            
            with col1:
                with st.container(border=True):
                    st.markdown("**📊 Team Analytics**")
                    if st.button("View Analytics", key="mgr_analytics", use_container_width=True):
                        st.info("✅ Access granted")
                        st.metric("Team Members", 5)
            
            with col2:
                with st.container(border=True):
                    st.markdown("**👥 My Team**")
                    if st.button("Manage Team", key="mgr_team", use_container_width=True):
                        st.info("✅ Access granted")
                        st.write("Team management tools")
            
            # Show what manager CANNOT access
            with st.container(border=True):
                st.markdown("**🚫 Restricted Access**")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👥 All Users", key="mgr_users_deny", use_container_width=True):
                        st.error("❌ Admin permission required")
                with col2:
                    if st.button("⚙️ System Settings", key="mgr_settings_deny", use_container_width=True):
                        st.error("❌ Admin permission required")
        
        elif role == 'user':
            # USER DASHBOARD
            st.markdown("### 👤 User Dashboard")
            st.info("ℹ️ STANDARD ACCESS")
            
            col1, col2 = st.columns(2)
            
            with col1:
                with st.container(border=True):
                    st.markdown("**📊 My Dashboard**")
                    if st.button("Open Dashboard", key="user_dash", use_container_width=True):
                        st.info("✅ Access granted")
                        st.write("Your personal dashboard")
            
            with col2:
                with st.container(border=True):
                    st.markdown("**👤 My Profile**")
                    if st.button("Edit Profile", key="user_profile", use_container_width=True):
                        st.info("✅ Access granted")
                        st.write("Profile settings")
            
            # Show restrictions
            with st.container(border=True):
                st.markdown("**🚫 Restricted Access**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📊 Analytics", key="user_analytics_deny", use_container_width=True):
                        st.error("❌ Manager+ required")
                with col2:
                    if st.button("👥 Users", key="user_users_deny", use_container_width=True):
                        st.error("❌ Admin required")
                with col3:
                    if st.button("⚙️ Settings", key="user_settings_deny", use_container_width=True):
                        st.error("❌ Admin required")
        
        else:  # viewer
            # VIEWER DASHBOARD
            st.markdown("### 👁️ Viewer Dashboard")
            st.info("ℹ️ READ-ONLY ACCESS")
            
            with st.container(border=True):
                st.markdown("**📖 View Content**")
                st.write("You can view content but cannot make changes")
                
                if st.button("View Reports", use_container_width=True):
                    st.info("✅ Access granted (read-only)")
                    st.write("📄 Report 1 (Read-only)")
                    st.write("📄 Report 2 (Read-only)")
            
            # Show all restrictions
            with st.container(border=True):
                st.markdown("**🚫 All Write Operations Denied**")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("✏️ Edit", key="viewer_edit_deny", use_container_width=True):
                        st.error("❌ Write permission required")
                
                with col2:
                    if st.button("🗑️ Delete", key="viewer_delete_deny", use_container_width=True):
                        st.error("❌ Delete permission required")
                
                with col3:
                    if st.button("➕ Create", key="viewer_create_deny", use_container_width=True):
                        st.error("❌ Write permission required")
        
        st.markdown("---")
        
        # Logout
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🚪 Logout", type="secondary", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.current_user = None
                st.session_state.user_role = None
                st.success("✅ Logged out")
                st.rerun()

# ============ TAB 3: PERMISSIONS TEST ============
with tab3:
    st.header("🎯 Permission Testing Ground")
    
    if not st.session_state.authenticated:
        st.warning("🔒 Please login in the RBAC Demo tab first")
        st.stop()
    
    st.success(f"Testing as: **{st.session_state.current_user}** ({st.session_state.user_role})")
    
    st.markdown("---")
    
    # Test each permission
    st.subheader("🧪 Test Your Permissions")
    
    all_permissions = ['read', 'write', 'delete', 'manage_users', 'view_analytics', 'system_settings']
    user_permissions = ROLE_PERMISSIONS.get(st.session_state.user_role, [])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### ✅ Granted")
        for perm in user_permissions:
            st.success(f"✓ {perm}")
    
    with col2:
        st.markdown("### ❌ Denied")
        denied = [p for p in all_permissions if p not in user_permissions]
        for perm in denied:
            st.error(f"✗ {perm}")
    
    with col3:
        st.markdown("### 📊 Summary")
        st.metric("Granted", len(user_permissions))
        st.metric("Denied", len(denied))
        st.metric("Total", len(all_permissions))
    
    st.markdown("---")
    
    # Interactive permission test
    st.subheader("🔍 Test Specific Permission")
    
    test_perm = st.selectbox(
        "Select permission to test:",
        all_permissions
    )
    
    if st.button("🧪 Test Permission", type="primary"):
        if test_perm in user_permissions:
            st.success(f"✅ You have '{test_perm}' permission!")
            st.balloons()
        else:
            st.error(f"❌ You don't have '{test_perm}' permission")
            st.write(f"Required roles: {[role for role, perms in ROLE_PERMISSIONS.items() if test_perm in perms]}")
    
    st.markdown("---")
    
    # Page access test
    st.subheader("🚪 Page Access Test")
    
    for page, allowed_roles in PAGE_ACCESS.items():
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.write(f"**{page.title()} Page**")
        
        with col2:
            st.caption(f"Allowed: {', '.join(allowed_roles)}")
        
        with col3:
            if st.session_state.user_role in allowed_roles:
                st.success("✓ Access")
            else:
                st.error("✗ Denied")

# ============ TAB 4: QUIZ ============
with tab4:
    st.header("🧪 Knowledge Check")
    
    q1 = st.radio(
        "Q1: What does RBAC stand for?",
        [
            "Read-Based Access Control",
            "Role-Based Access Control",
            "Route-Based Access Control"
        ]
    )
    
    q2 = st.radio(
        "Q2: In RBAC, what do roles have?",
        ["Users", "Permissions", "Pages"]
    )
    
    q3 = st.radio(
        "Q3: Which principle should guide permission assignment?",
        [
            "Give maximum permissions",
            "Least privilege (minimum needed)",
            "Same permissions for everyone"
        ]
    )
    
    q4 = st.checkbox("Q4: Permission checks should be on both frontend AND backend")
    
    q5 = st.radio(
        "Q5: How to check if user has a permission?",
        [
            "Check if user exists",
            "Check if permission is in user's role permissions",
            "Check user's email"
        ]
    )
    
    if st.button("✅ Check Answers", type="primary"):
        score = 0
        feedback = []
        
        if q1 == "Role-Based Access Control":
            score += 1
            feedback.append("✅ Q1: Correct!")
        else:
            feedback.append("❌ Q1: RBAC = Role-Based Access Control")
        
        if q2 == "Permissions":
            score += 1
            feedback.append("✅ Q2: Correct!")
        else:
            feedback.append("❌ Q2: Roles have Permissions")
        
        if q3 == "Least privilege (minimum needed)":
            score += 1
            feedback.append("✅ Q3: Correct! Least privilege principle")
        else:
            feedback.append("❌ Q3: Always use least privilege")
        
        if q4:
            score += 1
            feedback.append("✅ Q4: Correct! Never trust frontend only")
        else:
            feedback.append("❌ Q4: Check on both frontend AND backend")
        
        if q5 == "Check if permission is in user's role permissions":
            score += 1
            feedback.append("✅ Q5: Correct!")
        else:
            feedback.append("❌ Q5: Check role permissions")
        
        st.markdown("---")
        st.write(f"### 🎯 Score: {score}/5")
        
        for fb in feedback:
            st.write(fb)
        
        if score == 5:
            st.success("🎉 Perfect! You understand RBAC!")
            st.balloons()
        elif score >= 3:
            st.info("👍 Good! Review RBAC concepts once more.")
        else:
            st.warning("📖 Please review the Learn tab again.")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 8 - Authentication")
with col2:
    st.info("➡️ **Next:** Chapter 10 - Forms & Validation")