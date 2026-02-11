import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Chapter 2: Layouts",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Chapter 2: Layouts & Organization")
st.markdown("---")

# Tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs([
    "📖 Learn", 
    "🎮 Practice", 
    "🏗️ Dashboard Demo",
    "🧪 Quiz"
])

# ============ TAB 1: LEARN ============
with tab1:
    st.header("Layout Components")
    
    # Columns explanation
    with st.expander("📊 Columns", expanded=True):
        st.code("""
col1, col2 = st.columns(2)  # Equal width
col1, col2, col3 = st.columns([1, 2, 1])  # Custom width

with col1:
    st.write("Left")
with col2:
    st.write("Right")
        """, language="python")
        
        st.info("**Use for:** Side-by-side content, forms, dashboards")
    
    # Tabs explanation
    with st.expander("📑 Tabs"):
        st.code("""
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])

with tab1:
    st.write("Content 1")
with tab2:
    st.write("Content 2")
        """, language="python")
        
        st.info("**Use for:** Organizing different sections, settings")
    
    # Expanders explanation
    with st.expander("📦 Expanders"):
        st.code("""
with st.expander("Click to see more"):
    st.write("Hidden content")
    
with st.expander("Open by default", expanded=True):
    st.write("Visible content")
        """, language="python")
        
        st.info("**Use for:** FAQs, optional details, help text")
    
    # Containers explanation
    with st.expander("🎁 Containers"):
        st.code("""
# Create container
container = st.container(border=True)
container.write("Inside container")

# Empty placeholder
placeholder = st.empty()
placeholder.write("Can be updated later!")
        """, language="python")
        
        st.info("**Use for:** Dynamic updates, loading states")

# ============ TAB 2: PRACTICE ============
with tab2:
    st.header("🎮 Interactive Practice")
    
    # Columns demo
    st.subheader("1. Columns Example")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Users", "1,234", "+12%")
    with col2:
        st.metric("Revenue", "$45K", "+8%")
    with col3:
        st.metric("Active", "856", "-3%")
    
    st.divider()
    
    # Form with columns
    st.subheader("2. Form with Columns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name")
        email = st.text_input("Email")
        country = st.selectbox("Country", ["USA", "UK", "India"])
    
    with col2:
        last_name = st.text_input("Last Name")
        phone = st.text_input("Phone")
        city = st.text_input("City")
    
    if st.button("Submit Form", type="primary"):
        if first_name and last_name:
            st.success(f"✅ Form submitted for {first_name} {last_name}!")
        else:
            st.error("Please fill required fields")
    
    st.divider()
    
    # Expanders with content
    st.subheader("3. FAQ Section")
    
    with st.expander("❓ What is Streamlit?"):
        st.write("Streamlit is a Python framework for building data apps quickly.")
    
    with st.expander("❓ How does layout work?"):
        st.write("Streamlit provides columns, tabs, expanders, and containers.")
    
    with st.expander("❓ Can I customize styling?"):
        st.write("Yes! Use st.markdown with CSS (we'll learn in Chapter 8)")

# ============ TAB 3: DASHBOARD DEMO ============
with tab3:
    st.header("🏗️ Complete Dashboard Example")
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Revenue", "$125K", "+15%", delta_color="normal")
    with col2:
        st.metric("Orders", "3,542", "+8%", delta_color="normal")
    with col3:
        st.metric("Customers", "892", "-2%", delta_color="inverse")
    with col4:
        st.metric("Avg Order", "$35", "+3%", delta_color="normal")
    
    st.divider()
    
    # Main content area with columns
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Chart area
        with st.container(border=True):
            st.subheader("📈 Sales Trend")
            
            # Generate sample data
            dates = pd.date_range('2024-01-01', periods=30)
            sales = np.random.randint(100, 500, size=30)
            df = pd.DataFrame({'Date': dates, 'Sales': sales})
            
            st.line_chart(df.set_index('Date'))
        
        # Data table
        with st.container(border=True):
            st.subheader("📊 Recent Orders")
            
            orders_df = pd.DataFrame({
                'Order ID': [f'ORD-{i:04d}' for i in range(1, 6)],
                'Customer': ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown', 'Charlie Davis'],
                'Amount': ['$120', '$85', '$200', '$150', '$95'],
                'Status': ['Delivered', 'Shipped', 'Processing', 'Delivered', 'Shipped']
            })
            
            st.dataframe(orders_df, use_container_width=True)
    
    with col_right:
        # Filters
        with st.container(border=True):
            st.subheader("🔍 Filters")
            
            date_range = st.date_input(
                "Date Range",
                value=(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-01-30'))
            )
            
            status_filter = st.multiselect(
                "Status",
                ["Processing", "Shipped", "Delivered", "Cancelled"],
                default=["Delivered", "Shipped"]
            )
            
            min_amount = st.slider("Min Amount ($)", 0, 500, 11, 10)
            
            if st.button("Apply Filters", use_container_width=True):
                st.success("Filters applied!")
        
        # Quick stats
        with st.container(border=True):
            st.subheader("📌 Quick Stats")
            
            st.write("**Today's Performance**")
            st.progress(0.75)
            st.caption("75% of daily goal")
            
            st.write("**Top Product**")
            st.info("Laptop Pro X")
            
            st.write("**New Customers**")
            st.success("+23 today")

# ============ TAB 4: QUIZ ============
with tab4:
    st.header("🧪 Knowledge Check")
    
    q1 = st.radio(
        "Q1: Which creates side-by-side content?",
        ["st.tabs()", "st.columns()", "st.expander()"]
    )
    
    q2 = st.radio(
        "Q2: What's best for collapsible content?",
        ["st.columns()", "st.expander()", "st.container()"]
    )
    
    q3 = st.radio(
        "Q3: How to create 3 columns with custom widths?",
        [
            "st.columns(3)",
            "st.columns([1, 2, 1])",
            "st.columns([3])"
        ]
    )
    
    q4 = st.checkbox("Q4: Containers can have borders (border=True)")
    
    if st.button("Check Answers", type="primary"):
        score = 0
        
        if q1 == "st.columns()":
            score += 1
        if q2 == "st.expander()":
            score += 1
        if q3 == "st.columns([1, 2, 1])":
            score += 1
        if q4:
            score += 1
        
        st.write(f"### Score: {score}/4")
        
        if score == 4:
            st.success("🎉 Perfect! You mastered layouts!")
            st.balloons()
        elif score >= 3:
            st.info("👍 Great! Just review the concepts once more.")
        else:
            st.warning("📖 Please review the chapter again.")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 1 - Fundamentals")
with col2:
    st.info("➡️ **Next:** Chapter 3 - Working with Data")

