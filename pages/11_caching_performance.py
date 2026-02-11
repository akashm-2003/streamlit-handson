import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

st.set_page_config(
    page_title="Chapter 11: Caching & Performance",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Chapter 11: Caching & Performance")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📖 Learn",
    "🔥 Cache Demo",
    "📊 Performance Comparison",
    "🧪 Quiz"
])

# ============ TAB 1: LEARN ============
with tab1:
    st.header("Caching & Performance Concepts")
    
    with st.expander("⚡ 1. Why Caching Matters", expanded=True):
        st.markdown("""
        **The Problem:**
        - Streamlit reruns your entire script on every interaction
        - Expensive operations (DB queries, ML models, file reading) run repeatedly
        - This makes your app SLOW!
        
        **The Solution: Caching**
        - Cache stores results of expensive operations
        - Subsequent calls return cached result instantly
        - Only recalculates when inputs change
        """)
        
        st.code("""
# WITHOUT CACHING (SLOW! ❌)
def load_data():
    time.sleep(5)  # Simulates slow operation
    return pd.read_csv('large_file.csv')

# Called on EVERY rerun - user clicks button = 5 second wait!
df = load_data()

# WITH CACHING (FAST! ✅)
@st.cache_data
def load_data():
    time.sleep(5)  # Only runs ONCE
    return pd.read_csv('large_file.csv')

# First call: 5 seconds
# All subsequent calls: INSTANT!
df = load_data()
        """, language="python")
    
    with st.expander("💾 2. @st.cache_data - For Data"):
        st.markdown("""
        **Use @st.cache_data for:**
        - Loading dataframes from CSV/Excel/database
        - Data transformations and computations
        - API calls that return data
        - Any function that returns data (serializable objects)
        
        **How it works:**
        - Stores return value
        - Returns cached copy on subsequent calls
        - Recalculates when inputs change
        """)
        
        st.code("""
import streamlit as st
import pandas as pd

@st.cache_data
def load_csv(file_path):
    '''Loads CSV only once, then returns cached version'''
    print("Loading CSV...")  # You'll see this print only ONCE
    return pd.read_csv(file_path)

# First call: loads file
df1 = load_csv('data.csv')

# Second call: returns cached data (instant!)
df2 = load_csv('data.csv')

# Different input: recalculates
df3 = load_csv('other_data.csv')


@st.cache_data
def filter_data(df, min_value):
    '''Cached with parameters'''
    return df[df['value'] > min_value]

# Caches for each unique min_value
filtered_10 = filter_data(df, 10)  # Calculates
filtered_10_again = filter_data(df, 10)  # Cached!
filtered_20 = filter_data(df, 20)  # Calculates (new input)
        """, language="python")
        
        st.info("💡 **Cache Key:** Streamlit creates a cache key from function name + parameters")
    
    with st.expander("🔧 3. @st.cache_resource - For Resources"):
        st.markdown("""
        **Use @st.cache_resource for:**
        - Database connections
        - ML models (TensorFlow, PyTorch)
        - API clients
        - Thread pools
        - Any non-serializable objects
        
        **Difference from cache_data:**
        - Returns the SAME object (not a copy)
        - For objects that can't be pickled
        - For global resources shared across all users
        """)
        
        st.code("""
import streamlit as st
import sqlite3
from transformers import pipeline

@st.cache_resource
def get_database_connection():
    '''Creates DB connection once, reuses it'''
    print("Connecting to database...")
    return sqlite3.connect('app.db', check_same_thread=False)

# All users share this connection
conn = get_database_connection()


@st.cache_resource
def load_ml_model():
    '''Loads ML model once (expensive!)'''
    print("Loading model...")  # Only once!
    return pipeline("sentiment-analysis")

# Model loaded once, shared across all users
model = load_ml_model()

# Use the cached model
result = model("I love Streamlit!")


@st.cache_resource
def get_api_client():
    '''Initialize API client once'''
    import openai
    return openai.OpenAI(api_key=st.secrets["OPENAI_KEY"])

client = get_api_client()
        """, language="python")
        
        st.warning("⚠️ **Important:** Use cache_resource for connections and models that should be shared!")
    
    with st.expander("🔑 4. Cache Parameters"):
        st.code("""
# TTL (Time To Live) - Cache expires after time
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_live_data():
    return requests.get('api.com/data').json()


# Max entries - Limit cache size
@st.cache_data(max_entries=100)  # Keep only 100 cached results
def process_query(query):
    return expensive_operation(query)


# Show spinner - Display loading message
@st.cache_data(show_spinner=False)  # Hide default spinner
def silent_load():
    return load_data()

# Custom spinner
@st.cache_data(show_spinner="Loading data... ⏳")
def custom_spinner_load():
    return load_data()


# Persist - Save cache to disk
@st.cache_data(persist="disk")
def persistent_load():
    return expensive_calculation()
        """, language="python")
    
    with st.expander("🗑️ 5. Cache Invalidation"):
        st.code("""
# Clear specific function cache
load_data.clear()

# Clear all cache_data caches
st.cache_data.clear()

# Clear all cache_resource caches  
st.cache_resource.clear()

# Clear everything
st.cache_data.clear()
st.cache_resource.clear()


# Example: Manual refresh button
if st.button("🔄 Refresh Data"):
    load_data.clear()  # Clear cache
    st.rerun()  # Reload
        """, language="python")
    
    with st.expander("⚡ 6. Performance Best Practices"):
        st.markdown("""
        **✅ DO:**
        - Cache expensive operations (DB queries, file loading, ML inference)
        - Use cache_data for data operations
        - Use cache_resource for connections and models
        - Set reasonable TTL for time-sensitive data
        - Limit cache size with max_entries
        - Profile your app to find bottlenecks
        - Minimize widget reruns with forms
        - Lazy load data (only when needed)
        
        **❌ DON'T:**
        - Cache everything (wastes memory)
        - Cache fast operations (overhead not worth it)
        - Cache user-specific data without parameters
        - Forget to handle cache misses
        - Cache random or time-dependent functions
        - Use cache_data for database connections
        - Cache secrets or sensitive data
        """)
    
    with st.expander("📊 7. When NOT to Cache"):
        st.code("""
# ❌ DON'T cache time-dependent functions
@st.cache_data  # BAD!
def get_current_time():
    return datetime.now()  # Always returns first cached time!

# ✅ Just call directly (no cache)
def get_current_time():
    return datetime.now()


# ❌ DON'T cache random functions
@st.cache_data  # BAD!
def roll_dice():
    return random.randint(1, 6)  # Always returns same number!

# ✅ Don't cache randomness
def roll_dice():
    return random.randint(1, 6)


# ❌ DON'T cache user-specific data globally
@st.cache_data  # BAD! All users see same data
def get_user_profile():
    return load_profile(st.session_state.user_id)

# ✅ Cache with user_id as parameter
@st.cache_data
def get_user_profile(user_id):
    return load_profile(user_id)
        """, language="python")

# ============ TAB 2: CACHE DEMO ============
with tab2:
    st.header("🔥 Interactive Cache Demo")
    
    # Demo 1: cache_data
    st.subheader("1️⃣ @st.cache_data Demo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ❌ WITHOUT Cache")
        
        def slow_calculation_no_cache(n):
            time.sleep(2)  # Simulate slow operation
            return sum(range(n))
        
        if st.button("Calculate (No Cache)", use_container_width=True):
            start = time.time()
            result = slow_calculation_no_cache(1000000)
            elapsed = time.time() - start
            
            st.success(f"Result: {result:,}")
            st.error(f"⏱️ Time: {elapsed:.2f}s (EVERY TIME!)")
    
    with col2:
        st.markdown("### ✅ WITH Cache")
        
        @st.cache_data
        def slow_calculation_with_cache(n):
            time.sleep(2)  # Only slow first time
            return sum(range(n))
        
        if st.button("Calculate (Cached)", use_container_width=True):
            start = time.time()
            result = slow_calculation_with_cache(1000000)
            elapsed = time.time() - start
            
            st.success(f"Result: {result:,}")
            if elapsed < 0.1:
                st.success(f"⚡ Time: {elapsed:.4f}s (CACHED!)")
            else:
                st.info(f"⏱️ Time: {elapsed:.2f}s (First call)")
    
    st.info("💡 **Try it:** Click both buttons multiple times. Cached version is instant after first call!")
    
    st.markdown("---")
    
    # Demo 2: Parameters
    st.subheader("2️⃣ Cache with Parameters")
    
    @st.cache_data
    def generate_data(rows, seed):
        '''Cached per unique combination of rows and seed'''
        np.random.seed(seed)
        time.sleep(1)  # Simulate slow operation
        return pd.DataFrame({
            'A': np.random.randn(rows),
            'B': np.random.randn(rows)
        })
    
    col1, col2 = st.columns(2)
    
    with col1:
        rows = st.slider("Rows", 10, 1000, 100, key="cache_rows")
    
    with col2:
        seed = st.selectbox("Seed", [1, 2, 3], key="cache_seed")
    
    if st.button("Generate Data", type="primary"):
        start = time.time()
        df = generate_data(rows, seed)
        elapsed = time.time() - start
        
        st.dataframe(df.head())
        
        if elapsed < 0.1:
            st.success(f"⚡ Loaded from cache: {elapsed:.4f}s")
        else:
            st.info(f"⏱️ Generated new data: {elapsed:.2f}s")
    
    st.info("💡 **Try it:** Same rows+seed = cached. Different values = recalculates.")
    
    st.markdown("---")
    
    # Demo 3: TTL
    st.subheader("3️⃣ Cache with TTL (Time To Live)")
    
    @st.cache_data(ttl=10)  # Cache expires after 10 seconds
    def get_timestamp():
        return datetime.now().strftime('%H:%M:%S')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Cached timestamp (10s TTL):**")
        cached_time = get_timestamp()
        st.success(f"🕐 {cached_time}")
        st.caption("This will update every 10 seconds")
    
    with col2:
        st.write("**Live timestamp (no cache):**")
        live_time = datetime.now().strftime('%H:%M:%S')
        st.info(f"🕐 {live_time}")
        st.caption("This updates every rerun")
    
    if st.button("🔄 Refresh to see difference"):
        st.rerun()
    
    st.markdown("---")
    
    # Demo 4: Clear cache
    st.subheader("4️⃣ Manual Cache Clearing")
    
    @st.cache_data
    def expensive_operation():
        time.sleep(1)
        return f"Result computed at {datetime.now().strftime('%H:%M:%S')}"
    
    result = expensive_operation()
    st.success(f"📊 {result}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear This Function Cache", use_container_width=True):
            expensive_operation.clear()
            st.success("Cache cleared!")
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear All Data Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("All data cache cleared!")
            st.rerun()

# ============ TAB 3: PERFORMANCE COMPARISON ============
with tab3:
    st.header("📊 Performance Comparison")
    
    st.subheader("Real-World Scenario: Loading & Processing Data")
    
    # Create sample "slow" operations
    def load_data_slow():
        time.sleep(2)
        return pd.DataFrame({
            'Date': pd.date_range('2024-01-01', periods=1000),
            'Value': np.random.randn(1000).cumsum()
        })
    
    def process_data_slow(df):
        time.sleep(1)
        return df.rolling(window=7).mean()
    
    @st.cache_data
    def load_data_fast():
        time.sleep(2)
        return pd.DataFrame({
            'Date': pd.date_range('2024-01-01', periods=1000),
            'Value': np.random.randn(1000).cumsum()
        })
    
    @st.cache_data
    def process_data_fast(df):
        time.sleep(1)
        return df.rolling(window=7).mean()
    
    # Comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ❌ Without Caching")
        
        if st.button("Run Without Cache", use_container_width=True):
            with st.spinner("Loading..."):
                start = time.time()
                
                # Load
                df = load_data_slow()
                load_time = time.time() - start
                
                # Process
                processed = process_data_slow(df)
                process_time = time.time() - start - load_time
                
                total = time.time() - start
            
            st.error(f"⏱️ Load: {load_time:.2f}s")
            st.error(f"⏱️ Process: {process_time:.2f}s")
            st.error(f"⏱️ **Total: {total:.2f}s**")
            
            st.line_chart(processed['Value'])
    
    with col2:
        st.markdown("### ✅ With Caching")
        
        if st.button("Run With Cache", use_container_width=True):
            with st.spinner("Loading..."):
                start = time.time()
                
                # Load (cached)
                df = load_data_fast()
                load_time = time.time() - start
                
                # Process (cached)
                processed = process_data_fast(df)
                process_time = time.time() - start - load_time
                
                total = time.time() - start
            
            if total < 0.5:
                st.success(f"⚡ Load: {load_time:.4f}s (cached)")
                st.success(f"⚡ Process: {process_time:.4f}s (cached)")
                st.success(f"⚡ **Total: {total:.4f}s**")
            else:
                st.info(f"⏱️ Load: {load_time:.2f}s (first time)")
                st.info(f"⏱️ Process: {process_time:.2f}s (first time)")
                st.info(f"⏱️ **Total: {total:.2f}s**")
            
            st.line_chart(processed['Value'])
    
    st.markdown("---")
    
    # Performance tips
    st.subheader("⚡ Performance Optimization Tips")
    
    tips = {
        "1. Cache Expensive Operations": "DB queries, file loading, ML inference",
        "2. Use Forms": "Batch multiple inputs to reduce reruns",
        "3. Lazy Loading": "Load data only when needed",
        "4. Minimize Widgets": "Each widget triggers a rerun",
        "5. Pagination": "Don't display 10,000 rows at once",
        "6. Optimize Data": "Filter before visualizing",
        "7. Use Appropriate Cache": "cache_data for data, cache_resource for connections",
        "8. Set TTL": "For time-sensitive data",
    }
    
    for tip, desc in tips.items():
        with st.expander(tip):
            st.write(desc)

# ============ TAB 4: QUIZ ============
with tab4:
    st.header("🧪 Knowledge Check")
    
    q1 = st.radio(
        "Q1: What decorator should you use for loading a CSV file?",
        ["@st.cache_data", "@st.cache_resource", "No caching needed"]
    )
    
    q2 = st.radio(
        "Q2: What decorator should you use for a database connection?",
        ["@st.cache_data", "@st.cache_resource", "Both work the same"]
    )
    
    q3 = st.radio(
        "Q3: When should you NOT use caching?",
        [
            "Loading large files",
            "Getting current time/random numbers",
            "ML model inference"
        ]
    )
    
    q4 = st.radio(
        "Q4: How to set cache to expire after 1 hour?",
        ["ttl=60", "ttl=3600", "expire=3600"]
    )
    
    q5 = st.checkbox("Q5: Cache keys are based on function name + parameters")
    
    if st.button("✅ Check Answers", type="primary"):
        score = 0
        feedback = []
        
        if q1 == "@st.cache_data":
            score += 1
            feedback.append("✅ Q1: Correct! Use cache_data for data")
        else:
            feedback.append("❌ Q1: Use @st.cache_data for data operations")
        
        if q2 == "@st.cache_resource":
            score += 1
            feedback.append("✅ Q2: Correct! Use cache_resource for connections")
        else:
            feedback.append("❌ Q2: Use @st.cache_resource for connections")
        
        if q3 == "Getting current time/random numbers":
            score += 1
            feedback.append("✅ Q3: Correct! Don't cache time/random")
        else:
            feedback.append("❌ Q3: Don't cache time-dependent functions")
        
        if q4 == "ttl=3600":
            score += 1
            feedback.append("✅ Q4: Correct! TTL in seconds")
        else:
            feedback.append("❌ Q4: ttl=3600 (3600 seconds = 1 hour)")
        
        if q5:
            score += 1
            feedback.append("✅ Q5: Correct!")
        else:
            feedback.append("❌ Q5: Cache key = function + parameters")
        
        st.markdown("---")
        st.write(f"### 🎯 Score: {score}/5")
        
        for fb in feedback:
            st.write(fb)
        
        if score == 5:
            st.success("🎉 Perfect! You understand caching!")
            st.balloons()
        elif score >= 3:
            st.info("👍 Good! Review cache types.")
        else:
            st.warning("📖 Please review caching concepts.")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 10 - Forms & Validation")
with col2:
    st.info("➡️ **Next:** Chapter 12 - Advanced Security")