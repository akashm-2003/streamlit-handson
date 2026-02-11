import requests
import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime
import sqlite3
from contextlib import contextmanager

st.set_page_config(
    page_title="Chapter 13: Database & API",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ Chapter 13: Database & API Integration")
st.markdown("---")

# Initialize database state
if 'db_data' not in st.session_state:
    st.session_state.db_data = []

if 'api_history' not in st.session_state:
    st.session_state.api_history = []

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 Learn",
    "🗄️ SQLite Demo",
    "🌐 API Integration",
    "⚡ Real-time Data",
    "🧪 Quiz"
])

# ============ TAB 1: LEARN ============
with tab1:
    st.header("Database & API Concepts")
    
    with st.expander("🗄️ 1. Database Connection Basics", expanded=True):
        st.markdown("""
        **Why databases?**
        - Persistent storage (data survives app restarts)
        - Handle large datasets
        - Multi-user access
        - Query and filter efficiently
        - ACID transactions (Atomic, Consistent, Isolated, Durable)
        
        **Common databases for Streamlit:**
        - **SQLite**: File-based, no server, perfect for small apps
        - **PostgreSQL**: Full-featured, production-ready
        - **MySQL**: Popular, widely supported
        - **MongoDB**: NoSQL, document-based
        - **Supabase/Firebase**: Managed backends
        """)
        
        st.code("""
# SQLite (easiest to start)
import sqlite3

conn = sqlite3.connect('myapp.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Insert data
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
               ("Alice", "alice@example.com"))
conn.commit()

# Query data
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

# Close connection
conn.close()
        """, language="python")
    
    with st.expander("🔐 2. Connection Pooling & Caching"):
        st.markdown("""
        **Problem:** Creating new DB connection on every rerun is SLOW!
        
        **Solution:** Cache the connection with @st.cache_resource
        """)
        
        st.code("""
import streamlit as st
import sqlite3

# ❌ WRONG: New connection every rerun
def get_data():
    conn = sqlite3.connect('app.db')  # Slow!
    df = pd.read_sql("SELECT * FROM users", conn)
    conn.close()
    return df


# ✅ CORRECT: Cached connection
@st.cache_resource
def get_connection():
    '''Create connection once, reuse it'''
    return sqlite3.connect('app.db', check_same_thread=False)

def get_data():
    conn = get_connection()  # Reuses cached connection!
    df = pd.read_sql("SELECT * FROM users", conn)
    return df


# ✅ EVEN BETTER: Context manager
@contextmanager
def get_db_connection():
    conn = get_connection()
    try:
        yield conn
    finally:
        pass  # Don't close cached connection

# Usage
with get_db_connection() as conn:
    df = pd.read_sql("SELECT * FROM users", conn)
        """, language="python")
    
    with st.expander("💾 3. CRUD Operations"):
        st.markdown("""
        **CRUD = Create, Read, Update, Delete**
        
        Standard operations for any database.
        """)
        
        st.code("""
import sqlite3
import streamlit as st

@st.cache_resource
def get_connection():
    return sqlite3.connect('app.db', check_same_thread=False)

# CREATE
def create_user(name, email):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )
        conn.commit()
        return True, "User created"
    except sqlite3.IntegrityError:
        return False, "Email already exists"

# READ
def get_all_users():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM users", conn)
    return df

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# UPDATE
def update_user(user_id, name, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET name = ?, email = ? WHERE id = ?",
        (name, email, user_id)
    )
    conn.commit()
    return cursor.rowcount > 0  # True if updated

# DELETE
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    return cursor.rowcount > 0  # True if deleted

# SEARCH
def search_users(query):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM users WHERE name LIKE ? OR email LIKE ?",
        conn,
        params=(f'%{query}%', f'%{query}%')
    )
    return df
        """, language="python")
    
    with st.expander("🌐 4. API Integration Basics"):
        st.markdown("""
        **Why APIs?**
        - Fetch external data (weather, stocks, news)
        - Integrate with services (OpenAI, Stripe, SendGrid)
        - Build microservices
        - Real-time data updates
        """)
        
        st.code("""
import requests
import streamlit as st

# Basic GET request
response = requests.get('https://api.example.com/data')

if response.status_code == 200:
    data = response.json()
    st.write(data)
else:
    st.error(f"Error: {response.status_code}")


# With parameters
params = {
    'city': 'London',
    'units': 'metric'
}
response = requests.get('https://api.weather.com/current', params=params)


# With headers (API key)
headers = {
    'Authorization': f'Bearer {st.secrets["API_KEY"]}',
    'Content-Type': 'application/json'
}
response = requests.get('https://api.example.com/data', headers=headers)


# POST request (send data)
data = {
    'name': 'Alice',
    'email': 'alice@example.com'
}
response = requests.post('https://api.example.com/users', json=data, headers=headers)


# Error handling
try:
    response = requests.get('https://api.example.com/data', timeout=5)
    response.raise_for_status()  # Raises exception for 4xx/5xx
    data = response.json()
except requests.exceptions.Timeout:
    st.error("Request timed out")
except requests.exceptions.RequestException as e:
    st.error(f"API error: {e}")
        """, language="python")
    
    with st.expander("⚡ 5. Caching API Calls"):
        st.code("""
import streamlit as st
import requests

# ❌ WRONG: API call on every rerun
def get_weather(city):
    response = requests.get(f'https://api.weather.com/{city}')
    return response.json()  # Called repeatedly = slow + expensive!


# ✅ CORRECT: Cache API response
@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_weather(city):
    '''API call cached per city for 10 minutes'''
    response = requests.get(f'https://api.weather.com/{city}')
    return response.json()

# First call: hits API
data = get_weather('London')

# Subsequent calls within 10 min: returns cached data
data = get_weather('London')  # Instant!


# ✅ Conditional caching
@st.cache_data(ttl=3600)
def get_static_data():
    '''Cache for 1 hour (data doesn't change often)'''
    return requests.get('https://api.example.com/countries').json()

@st.cache_data(ttl=60)
def get_live_data():
    '''Cache for 1 minute (data updates frequently)'''
    return requests.get('https://api.example.com/stock/AAPL').json()

@st.cache_data(ttl=None)  # Cache forever
def get_historical_data(date):
    '''Historical data never changes'''
    return requests.get(f'https://api.example.com/history/{date}').json()
        """, language="python")
    
    with st.expander("🔄 6. Real-time Data Updates"):
        st.code("""
import streamlit as st
import time

# Auto-refresh pattern
def show_live_data():
    # Placeholder for data
    placeholder = st.empty()
    
    # Update loop
    for i in range(100):
        # Fetch new data
        data = fetch_latest_data()
        
        # Update display
        with placeholder.container():
            st.metric("Live Value", data['value'], data['change'])
            st.line_chart(data['history'])
        
        # Wait before next update
        time.sleep(5)  # Update every 5 seconds


# Manual refresh button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()


# Auto-refresh with rerun
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# Check if 30 seconds passed
if time.time() - st.session_state.last_update > 30:
    st.session_state.last_update = time.time()
    st.rerun()

st.write(f"Last update: {time.ctime(st.session_state.last_update)}")
        """, language="python")
    
    with st.expander("🔐 7. Securing API Keys"):
        st.code("""
# ❌ NEVER do this
API_KEY = "sk-abc123xyz"  # Visible in code!

# ✅ Use Streamlit secrets
# .streamlit/secrets.toml:
# [api]
# key = "sk-abc123xyz"
# url = "https://api.example.com"

import streamlit as st

api_key = st.secrets["api"]["key"]
api_url = st.secrets["api"]["url"]


# ✅ Or environment variables
import os

api_key = os.getenv("API_KEY")


# Usage with requests
headers = {
    'Authorization': f'Bearer {st.secrets["api"]["key"]}'
}

response = requests.get(
    st.secrets["api"]["url"],
    headers=headers
)
        """, language="python")

# ============ TAB 2: SQLITE DEMO ============
with tab2:
    st.header("🗄️ SQLite Database Demo")
    
    # Initialize SQLite database
    @st.cache_resource
    def init_database():
        conn = sqlite3.connect('demo_app.db', check_same_thread=False)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        return conn
    
    conn = init_database()
    
    # CRUD Interface
    st.subheader("📝 User Management")
    
    crud_tab1, crud_tab2, crud_tab3, crud_tab4 = st.tabs([
        "➕ Create",
        "📋 Read",
        "✏️ Update",
        "🗑️ Delete"
    ])
    
    # CREATE
    with crud_tab1:
        st.markdown("### ➕ Add New User")
        
        with st.form("create_user"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Name*")
                email = st.text_input("Email*")
            
            with col2:
                role = st.selectbox("Role", ["user", "admin", "manager"])
            
            if st.form_submit_button("➕ Create User", type="primary"):
                if not name or not email:
                    st.error("Name and email are required")
                else:
                    try:
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO users (name, email, role) VALUES (?, ?, ?)",
                            (name, email, role)
                        )
                        conn.commit()
                        st.success(f"✅ User '{name}' created successfully!")
                        st.balloons()
                    except sqlite3.IntegrityError:
                        st.error("❌ Email already exists!")
    
    # READ
    with crud_tab2:
        st.markdown("### 📋 View All Users")
        
        # Search
        search_query = st.text_input("🔍 Search users", placeholder="Name or email...")
        
        # Fetch data
        cursor = conn.cursor()
        
        if search_query:
            cursor.execute(
                "SELECT * FROM users WHERE name LIKE ? OR email LIKE ?",
                (f'%{search_query}%', f'%{search_query}%')
            )
        else:
            cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        
        users = cursor.fetchall()
        
        if users:
            # Display as dataframe
            df = pd.DataFrame(users, columns=['ID', 'Name', 'Email', 'Role', 'Created'])
            st.dataframe(df, use_container_width=True)
            
            st.metric("Total Users", len(users))
        else:
            st.info("No users found")
    
    # UPDATE
    with crud_tab3:
        st.markdown("### ✏️ Update User")
        
        # Get all users for selection
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users")
        users = cursor.fetchall()
        
        if users:
            user_options = {f"{name} (ID: {id})": id for id, name in users}
            selected = st.selectbox("Select User", list(user_options.keys()))
            user_id = user_options[selected]
            
            # Get current user data
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            current = cursor.fetchone()
            
            with st.form("update_user"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_name = st.text_input("Name", value=current[1])
                    new_email = st.text_input("Email", value=current[2])
                
                with col2:
                    new_role = st.selectbox("Role", ["user", "admin", "manager"], 
                                           index=["user", "admin", "manager"].index(current[3]))
                
                if st.form_submit_button("💾 Update User", type="primary"):
                    try:
                        cursor.execute(
                            "UPDATE users SET name = ?, email = ?, role = ? WHERE id = ?",
                            (new_name, new_email, new_role, user_id)
                        )
                        conn.commit()
                        st.success(f"✅ User updated successfully!")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("❌ Email already exists!")
        else:
            st.info("No users to update")
    
    # DELETE
    with crud_tab4:
        st.markdown("### 🗑️ Delete User")
        
        # Get all users
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()
        
        if users:
            user_options = {f"{name} ({email})": id for id, name, email in users}
            selected = st.selectbox("Select User to Delete", list(user_options.keys()))
            user_id = user_options[selected]
            
            st.warning("⚠️ This action cannot be undone!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Delete User", type="secondary", use_container_width=True):
                    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                    conn.commit()
                    st.success("✅ User deleted")
                    st.rerun()
            
            with col2:
                if st.button("Cancel", use_container_width=True):
                    st.info("Cancelled")
        else:
            st.info("No users to delete")

# ============ TAB 3: API INTEGRATION ============
with tab3:
    st.header("🌐 API Integration Examples")
    
    st.info("💡 These demos use free public APIs (no key required)")
    
    # API Demo 1: Random User
    st.subheader("1️⃣ Random User Generator API")
    
    @st.cache_data(ttl=300)
    def fetch_random_users(count=5):
        try:
            response = requests.get(f'https://randomuser.me/api/?results={count}')
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_count = st.slider("Number of users", 1, 10, 5)
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🔄 Fetch Users", use_container_width=True):
            fetch_random_users.clear()
    
    data = fetch_random_users(user_count)
    
    if 'error' in data:
        st.error(f"API Error: {data['error']}")
    else:
        users = data['results']
        
        for user in users:
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.image(user['picture']['large'], width=100)
            
            with col2:
                name = f"{user['name']['first']} {user['name']['last']}"
                st.markdown(f"**{name}**")
                st.write(f"📧 {user['email']}")
                st.write(f"📍 {user['location']['city']}, {user['location']['country']}")
            
            st.markdown("---")
    
    st.markdown("---")
    
    # API Demo 2: JSON Placeholder (Posts)
    st.subheader("2️⃣ Posts API (JSONPlaceholder)")
    
    @st.cache_data(ttl=600)
    def fetch_posts():
        try:
            response = requests.get('https://jsonplaceholder.typicode.com/posts')
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return []
    
    if st.button("📥 Load Posts"):
        with st.spinner("Fetching posts..."):
            posts = fetch_posts()
            
            if posts:
                st.success(f"✅ Loaded {len(posts)} posts")
                
                # Display sample
                for post in posts[:5]:
                    with st.expander(f"📝 {post['title'].title()}"):
                        st.write(post['body'])
                        st.caption(f"Post ID: {post['id']} | User ID: {post['userId']}")
            else:
                st.error("Failed to load posts")
    
    st.markdown("---")
    
    # API Demo 3: Create Post (POST request)
    st.subheader("3️⃣ Create Post (POST Request)")
    
    with st.form("create_post"):
        post_title = st.text_input("Title")
        post_body = st.text_area("Content")
        
        if st.form_submit_button("📤 Submit Post", type="primary"):
            if post_title and post_body:
                try:
                    response = requests.post(
                        'https://jsonplaceholder.typicode.com/posts',
                        json={
                            'title': post_title,
                            'body': post_body,
                            'userId': 1
                        }
                    )
                    response.raise_for_status()
                    result = response.json()
                    
                    st.success("✅ Post created!")
                    st.json(result)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Please fill all fields")
    
    st.markdown("---")
    
    # API History
    st.subheader("📜 API Call History")
    
    if st.session_state.api_history:
        for call in reversed(st.session_state.api_history[-5:]):
            st.write(f"**{call['timestamp']}** - {call['endpoint']} ({call['status']})")
    else:
        st.info("No API calls yet")

# ============ TAB 4: REAL-TIME DATA ============
with tab4:
    st.header("⚡ Real-time Data Updates")
    
    st.subheader("1️⃣ Auto-Refresh Demo")
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Enable Auto-Refresh (every 5 seconds)")
    
    # Display container
    placeholder = st.empty()
    
    if auto_refresh:
        # Initialize or update timestamp
        if 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = time.time()
        
        # Check if 5 seconds passed
        elapsed = time.time() - st.session_state.last_refresh
        
        if elapsed >= 5:
            st.session_state.last_refresh = time.time()
            st.rerun()
        
        # Display countdown
        remaining = 5 - int(elapsed)
        
        with placeholder.container():
            st.info(f"⏱️ Next refresh in: {remaining} seconds")
            
            # Simulate live data
            current_time = datetime.now().strftime('%H:%M:%S')
            value = time.time() % 100
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Time", current_time)
            
            with col2:
                st.metric("Random Value", f"{value:.2f}")
            
            with col3:
                delta = value - 50
                st.metric("Delta", f"{delta:.2f}", f"{delta:.2f}")
    else:
        with placeholder.container():
            st.info("Enable auto-refresh to see live updates")
    
    st.markdown("---")
    
    # Manual refresh
    st.subheader("2️⃣ Manual Refresh")
    
    if 'refresh_count' not in st.session_state:
        st.session_state.refresh_count = 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.session_state.refresh_count += 1
            st.rerun()
    
    with col2:
        st.metric("Refresh Count", st.session_state.refresh_count)
    
    with col3:
        st.metric("Last Update", datetime.now().strftime('%H:%M:%S'))
    
    st.markdown("---")
    
    # Progress tracking
    st.subheader("3️⃣ Progress Tracking")
    
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    
    progress_bar = st.progress(st.session_state.progress / 100)
    st.write(f"Progress: {st.session_state.progress}%")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add 10%", use_container_width=True):
            st.session_state.progress = min(100, st.session_state.progress + 10)
            st.rerun()
    
    with col2:
        if st.button("➖ Subtract 10%", use_container_width=True):
            st.session_state.progress = max(0, st.session_state.progress - 10)
            st.rerun()
    
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.progress = 0
            st.rerun()

# ============ TAB 5: QUIZ ============
with tab5:
    st.header("🧪 Knowledge Check")
    
    q1 = st.radio(
        "Q1: Which decorator should cache database connections?",
        ["@st.cache_data", "@st.cache_resource", "No caching needed"]
    )
    
    q2 = st.radio(
        "Q2: How to prevent SQL injection?",
        [
            "Use string formatting",
            "Use parameterized queries with ?",
            "Validate on frontend only"
        ]
    )
    
    q3 = st.checkbox("Q3: API keys should be stored in st.secrets, not hardcoded")
    
    q4 = st.radio(
        "Q4: What's the benefit of caching API calls?",
        [
            "Makes code shorter",
            "Reduces API calls and improves speed",
            "No benefit"
        ]
    )
    
    q5 = st.radio(
        "Q5: For frequently changing data, set TTL to:",
        ["Short duration (minutes)", "Long duration (hours)", "No TTL"]
    )
    
    if st.button("✅ Check Answers", type="primary"):
        score = 0
        feedback = []
        
        if q1 == "@st.cache_resource":
            score += 1
            feedback.append("✅ Q1: Correct! cache_resource for connections")
        else:
            feedback.append("❌ Q1: Use @st.cache_resource for connections")
        
        if q2 == "Use parameterized queries with ?":
            score += 1
            feedback.append("✅ Q2: Correct! Parameterized queries prevent injection")
        else:
            feedback.append("❌ Q2: Use parameterized queries (?)")
        
        if q3:
            score += 1
            feedback.append("✅ Q3: Correct! Never hardcode secrets")
        else:
            feedback.append("❌ Q3: Use st.secrets for API keys")
        
        if q4 == "Reduces API calls and improves speed":
            score += 1
            feedback.append("✅ Q4: Correct!")
        else:
            feedback.append("❌ Q4: Caching reduces API calls")
        
        if q5 == "Short duration (minutes)":
            score += 1
            feedback.append("✅ Q5: Correct! Short TTL for live data")
        else:
            feedback.append("❌ Q5: Short TTL for frequently changing data")
        
        st.markdown("---")
        st.write(f"### 🎯 Score: {score}/5")
        
        for fb in feedback:
            st.write(fb)
        
        if score == 5:
            st.success("🎉 Perfect! You understand databases & APIs!")
            st.balloons()
        elif score >= 3:
            st.info("👍 Good! Review caching strategies.")
        else:
            st.warning("📖 Please review database concepts.")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 12 - Advanced Security")
with col2:
    st.info("➡️ **Next:** Chapter 14 - Deployment & Final Project")