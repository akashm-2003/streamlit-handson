import streamlit as st

st.set_page_config(
    page_title="Chapter 7: Navigation",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start with sidebar collapsed
)

# Initialize navigation state
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'home'

if 'user_role' not in st.session_state:
    st.session_state.user_role = 'guest'  # guest, user, admin

st.title("🧭 Chapter 7: Custom Navigation & Routing")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📖 Learn",
    "🎨 Navigation Styles",
    "🔐 Role-Based Navigation",
    "🧪 Quiz"
])

# ============ TAB 1: LEARN ============
with tab1:
    st.header("Custom Navigation Concepts")
    
    with st.expander("🚫 1. Hiding the Default Sidebar", expanded=True):
        st.markdown("""
        **Method 1: Page Config (Collapsed)**
        """)
        
        st.code("""
import streamlit as st

st.set_page_config(
    initial_sidebar_state="collapsed"  # Starts collapsed
)
        """, language="python")
        
        st.markdown("**Method 2: CSS (Completely Hidden)**")
        
        st.code("""
import streamlit as st

# Hide sidebar completely
st.markdown('''
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="collapsedControl"] {
        display: none;
    }
</style>
''', unsafe_allow_html=True)
        """, language="python")
        
        st.info("💡 **Note:** Method 2 completely removes sidebar, users can't access it")
    
    with st.expander("🎨 2. Creating Custom Navbars"):
        st.markdown("**Horizontal Button Navbar**")
        
        st.code("""
import streamlit as st

# Simple horizontal navbar
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

with col2:
    if st.button("📊 Data", use_container_width=True):
        st.session_state.page = 'data'
        st.rerun()

with col3:
    if st.button("📈 Charts", use_container_width=True):
        st.session_state.page = 'charts'
        st.rerun()

with col4:
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.page = 'settings'
        st.rerun()
        """, language="python")
        
        st.markdown("**Using streamlit-option-menu (Third-party)**")
        
        st.code("""
# Install: pip install streamlit-option-menu
from streamlit_option_menu import option_menu

selected = option_menu(
    menu_title=None,  # No title
    options=["Home", "Data", "Charts", "Settings"],
    icons=["house", "database", "graph-up", "gear"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected == "Home":
    st.write("Home content")
elif selected == "Data":
    st.write("Data content")
        """, language="python")
    
    with st.expander("🎯 3. Active State Highlighting"):
        st.code("""
# Highlight active button
current_page = st.session_state.get('page', 'home')

col1, col2, col3 = st.columns(3)

with col1:
    btn_type = "primary" if current_page == 'home' else "secondary"
    if st.button("🏠 Home", type=btn_type, use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

with col2:
    btn_type = "primary" if current_page == 'data' else "secondary"
    if st.button("📊 Data", type=btn_type, use_container_width=True):
        st.session_state.page = 'data'
        st.rerun()
        """, language="python")
    
    with st.expander("🔗 4. URL Parameters (Query Params)"):
        st.markdown("""
        **Reading URL Parameters**
        """)
        
        st.code("""
import streamlit as st

# Read query params from URL
# Example: http://localhost:8501/?page=data&id=123

params = st.query_params

# Get specific parameter
page = params.get("page", "home")  # Default to 'home'
item_id = params.get("id", None)

st.write(f"Page: {page}")
st.write(f"ID: {item_id}")
        """, language="python")
        
        st.markdown("**Setting URL Parameters**")
        
        st.code("""
# Set query params
st.query_params["page"] = "data"
st.query_params["id"] = "123"

# Result: URL becomes /?page=data&id=123

# Clear query params
st.query_params.clear()
        """, language="python")
    
    with st.expander("🔐 5. Conditional Navigation"):
        st.code("""
# Show different nav based on authentication
if st.session_state.get('authenticated', False):
    # Authenticated users see full nav
    options = ["Home", "Data", "Charts", "Profile", "Logout"]
else:
    # Guests see limited nav
    options = ["Home", "About", "Login"]

# Show appropriate navigation
selected = st.selectbox("Navigate", options)
        """, language="python")

# ============ TAB 2: NAVIGATION STYLES ============
with tab2:
    st.header("🎨 Navigation Style Examples")
    
    st.subheader("Style 1: Simple Horizontal Buttons")
    
    # Style 1: Basic buttons
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)
        
        current = st.session_state.current_view
        
        with col1:
            if st.button("🏠 Home", 
                        type="primary" if current == 'home' else "secondary",
                        use_container_width=True,
                        key="nav1_home"):
                st.session_state.current_view = 'home'
                st.rerun()
        
        with col2:
            if st.button("📊 Data", 
                        type="primary" if current == 'data' else "secondary",
                        use_container_width=True,
                        key="nav1_data"):
                st.session_state.current_view = 'data'
                st.rerun()
        
        with col3:
            if st.button("📈 Charts", 
                        type="primary" if current == 'charts' else "secondary",
                        use_container_width=True,
                        key="nav1_charts"):
                st.session_state.current_view = 'charts'
                st.rerun()
        
        with col4:
            if st.button("⚙️ Settings", 
                        type="primary" if current == 'settings' else "secondary",
                        use_container_width=True,
                        key="nav1_settings"):
                st.session_state.current_view = 'settings'
                st.rerun()
    
    st.markdown("---")
    
    # Style 2: With CSS styling
    st.subheader("Style 2: Custom CSS Navbar")
    
    st.markdown("""
    <style>
        .custom-navbar {
            background-color: #2c3e50;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .nav-button {
            background-color: transparent;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            cursor: pointer;
            font-size: 16px;
        }
        .nav-button:hover {
            background-color: #34495e;
            border-radius: 5px;
        }
    </style>
    
    <div class="custom-navbar">
        <span style="color: white; font-size: 20px; font-weight: bold;">🚀 My App</span>
        <span style="float: right; color: white;">
            🏠 Home | 📊 Data | 📈 Charts | ⚙️ Settings
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 This is a visual example. Real buttons would be integrated below.")
    
    st.markdown("---")
    
    # Style 3: Radio buttons as navigation
    st.subheader("Style 3: Radio Button Navigation")
    
    with st.container(border=True):
        nav_choice = st.radio(
            "Navigate to:",
            ["🏠 Home", "📊 Data", "📈 Charts", "⚙️ Settings"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.session_state.current_view = nav_choice.split()[1].lower()
    
    st.markdown("---")
    
    # Style 4: Selectbox navigation
    st.subheader("Style 4: Dropdown Navigation")
    
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            nav_select = st.selectbox(
                "Go to page:",
                ["Home", "Data", "Charts", "Settings"],
                index=["home", "data", "charts", "settings"].index(st.session_state.current_view),
                label_visibility="collapsed"
            )
            st.session_state.current_view = nav_select.lower()
        
        with col2:
            st.metric("Current Page", st.session_state.current_view.title())
    
    st.markdown("---")
    
    # Display current view content
    st.subheader(f"📄 Current View: {st.session_state.current_view.title()}")
    
    with st.container(border=True):
        if st.session_state.current_view == 'home':
            st.write("🏠 **Home Page Content**")
            st.write("Welcome to the home page!")
        
        elif st.session_state.current_view == 'data':
            st.write("📊 **Data Page Content**")
            st.write("This is where data analysis happens.")
        
        elif st.session_state.current_view == 'charts':
            st.write("📈 **Charts Page Content**")
            st.write("Visualizations and graphs appear here.")
        
        elif st.session_state.current_view == 'settings':
            st.write("⚙️ **Settings Page Content**")
            st.write("Configure your preferences here.")

# ============ TAB 3: ROLE-BASED NAVIGATION ============
with tab3:
    st.header("🔐 Role-Based Navigation")
    
    st.info("This demonstrates conditional navigation based on user roles")
    
    # Role selector
    st.subheader("👤 Select Your Role")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔓 Guest", use_container_width=True):
            st.session_state.user_role = 'guest'
            st.rerun()
    
    with col2:
        if st.button("👤 User", use_container_width=True):
            st.session_state.user_role = 'user'
            st.rerun()
    
    with col3:
        if st.button("👑 Admin", use_container_width=True):
            st.session_state.user_role = 'admin'
            st.rerun()
    
    st.markdown("---")
    
    # Show current role
    role_emoji = {"guest": "🔓", "user": "👤", "admin": "👑"}
    st.success(f"Current Role: {role_emoji[st.session_state.user_role]} **{st.session_state.user_role.title()}**")
    
    st.markdown("---")
    
    # Conditional navigation based on role
    st.subheader("🧭 Available Navigation")
    
    # Define pages for each role
    pages = {
        'guest': ['Home', 'About', 'Login'],
        'user': ['Home', 'Dashboard', 'Profile', 'Logout'],
        'admin': ['Home', 'Dashboard', 'Users', 'Analytics', 'Settings', 'Logout']
    }
    
    available_pages = pages[st.session_state.user_role]
    
    # Display navigation
    cols = st.columns(len(available_pages))
    
    for idx, page in enumerate(available_pages):
        with cols[idx]:
            # Assign icons
            icons = {
                'Home': '🏠', 'About': 'ℹ️', 'Login': '🔑',
                'Dashboard': '📊', 'Profile': '👤', 'Logout': '🚪',
                'Users': '👥', 'Analytics': '📈', 'Settings': '⚙️'
            }
            
            icon = icons.get(page, '📄')
            
            if st.button(f"{icon} {page}", use_container_width=True, key=f"role_nav_{page}"):
                st.success(f"Navigated to {page}")
    
    st.markdown("---")
    
    # Show role comparison
    st.subheader("📋 Role Permissions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🔓 Guest**")
        st.write("- Home")
        st.write("- About")
        st.write("- Login")
    
    with col2:
        st.markdown("**👤 User**")
        st.write("- Home")
        st.write("- Dashboard")
        st.write("- Profile")
        st.write("- Logout")
    
    with col3:
        st.markdown("**👑 Admin**")
        st.write("- Home")
        st.write("- Dashboard")
        st.write("- Users (Admin only!)")
        st.write("- Analytics (Admin only!)")
        st.write("- Settings (Admin only!)")
        st.write("- Logout")
    
    st.markdown("---")
    
    # Code example
    with st.expander("💻 Implementation Code"):
        st.code("""
import streamlit as st

# Check user role
user_role = st.session_state.get('user_role', 'guest')

# Define navigation based on role
if user_role == 'admin':
    # Admin sees everything
    if st.button("👥 Manage Users"):
        st.switch_page("pages/admin_users.py")
    
    if st.button("📈 Analytics"):
        st.switch_page("pages/analytics.py")

elif user_role == 'user':
    # Regular users see limited nav
    if st.button("📊 Dashboard"):
        st.switch_page("pages/dashboard.py")
    
    if st.button("👤 Profile"):
        st.switch_page("pages/profile.py")

else:  # guest
    # Guests see minimal nav
    if st.button("🔑 Login"):
        st.switch_page("pages/login.py")
        """, language="python")

# ============ TAB 4: QUIZ ============
with tab4:
    st.header("🧪 Knowledge Check")
    
    q1 = st.radio(
        "Q1: How to hide sidebar completely with CSS?",
        [
            "sidebar_visible=False",
            '[data-testid="stSidebar"] {display: none;}',
            "st.hide_sidebar()"
        ]
    )
    
    q2 = st.radio(
        "Q2: What triggers a page rerun after navigation?",
        ["st.rerun()", "st.refresh()", "st.reload()"]
    )
    
    q3 = st.radio(
        "Q3: How to highlight the active navigation button?",
        [
            "Use different color",
            "Use type='primary' for active",
            "Add a border"
        ]
    )
    
    q4 = st.checkbox("Q4: URL query params can be used for navigation state")
    
    q5 = st.radio(
        "Q5: For role-based navigation, what should you check?",
        [
            "User's browser",
            "st.session_state role",
            "URL path"
        ]
    )
    
    if st.button("✅ Check Answers", type="primary"):
        score = 0
        feedback = []
        
        if '[data-testid="stSidebar"] {display: none;}' in q1:
            score += 1
            feedback.append("✅ Q1: Correct! CSS hides sidebar completely")
        else:
            feedback.append("❌ Q1: Use CSS [data-testid='stSidebar']")
        
        if q2 == "st.rerun()":
            score += 1
            feedback.append("✅ Q2: Correct!")
        else:
            feedback.append("❌ Q2: Use st.rerun()")
        
        if q3 == "Use type='primary' for active":
            score += 1
            feedback.append("✅ Q3: Correct! Primary buttons stand out")
        else:
            feedback.append("❌ Q3: Use type='primary' for active button")
        
        if q4:
            score += 1
            feedback.append("✅ Q4: Correct! Query params are useful")
        else:
            feedback.append("❌ Q4: Query params work for navigation")
        
        if q5 == "st.session_state role":
            score += 1
            feedback.append("✅ Q5: Correct! Check session state")
        else:
            feedback.append("❌ Q5: Check st.session_state for role")
        
        st.markdown("---")
        st.write(f"### 🎯 Score: {score}/5")
        
        for fb in feedback:
            st.write(fb)
        
        if score == 5:
            st.success("🎉 Perfect! You mastered custom navigation!")
            st.balloons()
        elif score >= 3:
            st.info("👍 Good! Review a few concepts.")
        else:
            st.warning("📖 Please review the Learn tab.")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 6 - Multi-Page Architecture")
with col2:
    st.info("➡️ **Next:** Chapter 8 - Authentication")