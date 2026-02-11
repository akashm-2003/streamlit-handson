import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Chapter 6: Multi-Page",
    page_icon="📑",
    layout="wide"
)

st.title("📑 Chapter 6: Multi-Page Architecture")
st.markdown("---")

# Initialize shared state
if 'shared_message' not in st.session_state:
    st.session_state.shared_message = ""
if 'shared_counter' not in st.session_state:
    st.session_state.shared_counter = 0
if 'shared_dataframe' not in st.session_state:
    st.session_state.shared_dataframe = None

# Tabs
tab1, tab2, tab3 = st.tabs(["📖 Learn", "🎮 Demo", "🧪 Quiz"])

# ============ TAB 1: LEARN ============
with tab1:
    st.header("Multi-Page App Concepts")
    
    with st.expander("📁 1. Folder Structure", expanded=True):
        st.markdown("""
        **Real Multi-Page App Structure:**
```
        your_app/
        ├── Home.py              # Main entry (run this)
        ├── pages/
        │   ├── 1_Data.py       # Auto-discovered
        │   ├── 2_Charts.py     # Auto-discovered
        │   └── 3_Settings.py   # Auto-discovered
        └── requirements.txt
```
        
        **Key Points:**
        - Folder **must** be named `pages/`
        - Streamlit auto-creates sidebar navigation
        - Files run independently but share `st.session_state`
        """)
        
        st.code("""
# To run your multi-page app:
streamlit run Home.py

# Streamlit automatically:
# 1. Detects pages/ folder
# 2. Creates sidebar navigation
# 3. Loads pages on demand
        """, language="bash")
    
    with st.expander("🔄 2. Sharing Data Between Pages"):
        st.markdown("""
        **Session State is Key!**
        
        All pages share the same `st.session_state`.
        """)
        
        st.code("""
# ===== Page 1: Store Data =====
import streamlit as st

st.session_state['user_name'] = 'Alice'
st.session_state['dataframe'] = df

# ===== Page 2: Access Data =====
import streamlit as st

# Always check before accessing!
if 'user_name' in st.session_state:
    name = st.session_state.user_name
    st.write(f"Welcome {name}!")

if 'dataframe' in st.session_state:
    df = st.session_state.dataframe
    st.dataframe(df)
        """, language="python")
        
        st.warning("⚠️ **Critical:** Always check if key exists before accessing!")
    
    with st.expander("🚀 3. Page Navigation"):
        st.markdown("""
        **Method 1: Automatic Sidebar (Default)**
        - Streamlit creates it automatically
        - No code needed!
        
        **Method 2: Programmatic Navigation**
        """)
        
        st.code("""
import streamlit as st

# Navigate to another page
if st.button("Go to Data Page"):
    st.switch_page("pages/1_Data.py")

# Navigate to home
if st.button("Go Home"):
    st.switch_page("Home.py")
        """, language="python")
    
    with st.expander("⚙️ 4. Page Configuration"):
        st.code("""
import streamlit as st

# Each page can have different config
st.set_page_config(
    page_title="My Page",      # Browser tab
    page_icon="🎯",            # Browser icon
    layout="wide",             # or "centered"
    initial_sidebar_state="expanded"  # or "collapsed"
)

# ⚠️ MUST be first Streamlit command!
        """, language="python")
    
    with st.expander("💡 5. Best Practices"):
        st.markdown("""
        **✅ DO:**
```python
        # Initialize state at the start
        if 'data' not in st.session_state:
            st.session_state.data = None
        
        # Check before accessing
        if 'data' in st.session_state:
            data = st.session_state.data
```
        
        **❌ DON'T:**
```python
        # Direct access without checking
        data = st.session_state.data  # Error if not set!
        
        # Setting page config after other commands
        st.title("Page")
        st.set_page_config(...)  # Error!
```
        """)

# ============ TAB 2: DEMO ============
with tab2:
    st.header("🎮 Cross-Page Communication Demo")
    
    st.info("""
    **Try this:** 
    1. Set values here in Chapter 6
    2. Go to Chapter 0 (00_basic) 
    3. See the shared data there!
    4. Come back to see it's still here
    """)
    
    st.markdown("---")
    
    # Section 1: Simple Counter
    st.subheader("1️⃣ Shared Counter")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Increment", use_container_width=True):
            st.session_state.shared_counter += 1
            st.rerun()
    
    with col2:
        if st.button("➖ Decrement", use_container_width=True):
            st.session_state.shared_counter -= 1
            st.rerun()
    
    with col3:
        st.metric("Shared Counter", st.session_state.shared_counter)
    
    st.info(f"💡 **Current value:** {st.session_state.shared_counter} (visible across all pages!)")
    
    st.markdown("---")
    
    # Section 2: Shared Message
    st.subheader("2️⃣ Shared Message")
    
    message = st.text_input(
        "Enter a message (visible on all pages)",
        value=st.session_state.shared_message,
        placeholder="Type something..."
    )
    
    if st.button("💾 Save Message", type="primary"):
        st.session_state.shared_message = message
        st.success("✅ Message saved! Go to Chapter 0 to see it.")
    
    if st.session_state.shared_message:
        st.info(f"📝 **Stored message:** {st.session_state.shared_message}")
    
    st.markdown("---")
    
    # Section 3: Shared DataFrame
    st.subheader("3️⃣ Shared Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Generate Sample Data"):
            # Create sample data
            np.random.seed(42)
            df = pd.DataFrame({
                'Name': [f'Person {i}' for i in range(1, 11)],
                'Age': np.random.randint(20, 60, 10),
                'Salary': np.random.randint(30000, 100000, 10)
            })
            
            st.session_state.shared_dataframe = df
            st.success("✅ Data generated!")
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Data"):
            st.session_state.shared_dataframe = None
            st.success("✅ Data cleared!")
            st.rerun()
    
    # Display data
    if st.session_state.shared_dataframe is not None:
        df = st.session_state.shared_dataframe
        
        st.success(f"📊 **Data loaded:** {len(df)} rows × {len(df.columns)} columns")
        st.dataframe(df, width=None)
        
        st.info("💡 This data is accessible from **all pages** using `st.session_state.shared_dataframe`")
    else:
        st.warning("⚠️ No data stored yet. Click 'Generate Sample Data' above.")
    
    st.markdown("---")
    
    # Section 4: Test Navigation
    st.subheader("4️⃣ Page Navigation Test")
    
    st.write("**Navigate to Chapter 0 to verify shared state:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👉 Go to Chapter 0", type="primary", use_container_width=True):
            st.switch_page("pages/00_basic.py")
    
    with col2:
        st.info("See the shared data on Chapter 0!")
    
    st.markdown("---")
    
    # Section 5: Debug View
    with st.expander("🔍 View All Session State"):
        st.write("**All session state keys:**")
        
        # Filter to show only our shared keys
        shared_keys = {
            'shared_message': st.session_state.shared_message,
            'shared_counter': st.session_state.shared_counter,
            'shared_dataframe': 'DataFrame with {} rows'.format(
                len(st.session_state.shared_dataframe)
            ) if st.session_state.shared_dataframe is not None else None
        }
        
        st.json(shared_keys)

# ============ TAB 3: QUIZ ============
with tab3:
    st.header("🧪 Quick Quiz")
    
    q1 = st.radio(
        "Q1: What folder name is required for pages?",
        ["pages/", "views/", "routes/", "Any name"]
    )
    
    q2 = st.radio(
        "Q2: How is data shared between pages?",
        [
            "Global variables",
            "st.session_state",
            "File writing",
            "URL parameters"
        ]
    )
    
    q3 = st.radio(
        "Q3: What function navigates to another page?",
        ["st.goto()", "st.navigate()", "st.switch_page()"]
    )
    
    q4 = st.checkbox("Q4: st.set_page_config() must be the first Streamlit command")
    
    q5 = st.radio(
        "Q5: Before accessing session state, you should:",
        [
            "Just access it directly",
            "Check if key exists first",
            "Initialize it every time"
        ]
    )
    
    if st.button("✅ Check Answers", type="primary"):
        score = 0
        feedback = []
        
        if q1 == "pages/":
            score += 1
            feedback.append("✅ Q1: Correct!")
        else:
            feedback.append("❌ Q1: Must be 'pages/' exactly")
        
        if q2 == "st.session_state":
            score += 1
            feedback.append("✅ Q2: Correct!")
        else:
            feedback.append("❌ Q2: Use st.session_state")
        
        if q3 == "st.switch_page()":
            score += 1
            feedback.append("✅ Q3: Correct!")
        else:
            feedback.append("❌ Q3: Use st.switch_page()")
        
        if q4:
            score += 1
            feedback.append("✅ Q4: Correct!")
        else:
            feedback.append("❌ Q4: Must be first command")
        
        if q5 == "Check if key exists first":
            score += 1
            feedback.append("✅ Q5: Correct!")
        else:
            feedback.append("❌ Q5: Always check first")
        
        st.markdown("---")
        st.write(f"### 🎯 Score: {score}/5")
        
        for fb in feedback:
            st.write(fb)
        
        if score == 5:
            st.success("🎉 Perfect score! You understand multi-page apps!")
            st.balloons()
        elif score >= 3:
            st.info("👍 Good job! Review the concepts once more.")
        else:
            st.warning("📖 Please review the Learn tab again.")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 5 - Visualization")
with col2:
    st.info("➡️ **Next:** Chapter 7 - Custom Navigation & Authentication")