import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Chapter 5: Visualization",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Chapter 5: Data Visualization")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📖 Learn",
    "📈 Interactive Dashboard",
    "🎨 Chart Gallery",
    "🧪 Quiz"
])

# ============ TAB 1: LEARN ============
with tab1:
    st.header("Visualization in Streamlit")
    
    with st.expander("🎯 Built-in Charts (Simple)", expanded=True):
        st.markdown("""
        Streamlit provides simple, built-in charts - perfect for quick visualizations!
        """)
        
        st.code("""
# Line chart
st.line_chart(data)

# Bar chart
st.bar_chart(data)

# Area chart
st.area_chart(data)

# Scatter chart (with lat/lon)
st.map(data)
        """, language="python")
        
        # Demo
        demo_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['A', 'B', 'C']
        )
        
        st.write("**Example:**")
        st.line_chart(demo_data)
    
    with st.expander("🚀 Plotly (Professional)"):
        st.markdown("""
        Plotly provides interactive, professional-grade charts!
        """)
        
        st.code("""
import plotly.express as px

# Create chart
fig = px.line(df, x='x', y='y', title='My Chart')

# Display
st.plotly_chart(fig, width='stretch')
        """, language="python")
        
        st.info("**Features:** Zoom, pan, hover tooltips, export, animations")
    
    with st.expander("📊 Common Chart Types"):
        st.markdown("""
        - **Line Chart**: Time series, trends
        - **Bar Chart**: Comparisons, categorical data
        - **Scatter Plot**: Correlations, relationships
        - **Pie Chart**: Proportions, distributions
        - **Histogram**: Frequency distributions
        - **Box Plot**: Statistical distributions
        - **Heatmap**: 2D data, correlations
        """)
    
    with st.expander("💡 Best Practices"):
        st.markdown("""
        1. **Choose the right chart** for your data type
        2. **Use clear titles** and axis labels
        3. **Add interactivity** with Plotly
        4. **Use colors** meaningfully (not just decoration)
        5. **Keep it simple** - don't overcomplicate
        6. **width='stretch'** for responsive charts
        7. **width='content'** for natural width
        """)

# ============ TAB 2: INTERACTIVE DASHBOARD ============
with tab2:
    st.header("📈 Sales Dashboard")
    
    # Generate sample data
    @st.cache_data
    def generate_sales_data():
        np.random.seed(42)
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
        
        df = pd.DataFrame({
            'Date': dates,
            'Sales': np.random.randint(1000, 5000, len(dates)) + 
                     np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 1000,
            'Customers': np.random.randint(50, 200, len(dates)),
            'Region': np.random.choice(['North', 'South', 'East', 'West'], len(dates)),
            'Product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Watch'], len(dates))
        })
        
        df['Revenue'] = df['Sales'] * np.random.uniform(10, 100, len(dates))
        
        return df
    
    df = generate_sales_data()
    
    # Filters in sidebar
    st.sidebar.header("🔍 Filters")
    
    # Date range
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(df['Date'].min(), df['Date'].max()),
        min_value=df['Date'].min(),
        max_value=df['Date'].max()
    )
    
    # Region filter
    regions = st.sidebar.multiselect(
        "Regions",
        options=df['Region'].unique(),
        default=df['Region'].unique()
    )
    
    # Product filter
    products = st.sidebar.multiselect(
        "Products",
        options=df['Product'].unique(),
        default=df['Product'].unique()
    )
    
    # Apply filters
    mask = (
        (df['Date'] >= pd.to_datetime(date_range[0])) &
        (df['Date'] <= pd.to_datetime(date_range[1])) &
        (df['Region'].isin(regions)) &
        (df['Product'].isin(products))
    )
    
    filtered_df = df[mask]
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = filtered_df['Sales'].sum()
        st.metric("Total Sales", f"{total_sales:,.0f}", "+12%")
    
    with col2:
        avg_sales = filtered_df['Sales'].mean()
        st.metric("Avg Daily Sales", f"{avg_sales:,.0f}", "+5%")
    
    with col3:
        total_customers = filtered_df['Customers'].sum()
        st.metric("Total Customers", f"{total_customers:,.0f}", "+8%")
    
    with col4:
        total_revenue = filtered_df['Revenue'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.0f}", "+15%")
    
    st.markdown("---")
    
    # Main charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales trend
        st.subheader("📈 Sales Trend")
        
        daily_sales = filtered_df.groupby('Date')['Sales'].sum().reset_index()
        
        fig = px.line(
            daily_sales, 
            x='Date', 
            y='Sales',
            title='Daily Sales Over Time'
        )
        
        fig.update_traces(line_color='#1f77b4', line_width=2)
        fig.update_layout(hovermode='x unified')
        
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Sales by region
        st.subheader("🗺️ Sales by Region")
        
        region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
        
        fig = px.bar(
            region_sales,
            x='Region',
            y='Sales',
            title='Sales by Region',
            color='Sales',
            color_continuous_scale='Blues'
        )
        
        st.plotly_chart(fig, width='stretch')
    
    # Second row
    col1, col2 = st.columns(2)
    
    with col1:
        # Product distribution
        st.subheader("🛍️ Product Distribution")
        
        product_sales = filtered_df.groupby('Product')['Sales'].sum().reset_index()
        
        fig = px.pie(
            product_sales,
            names='Product',
            values='Sales',
            title='Sales by Product',
            hole=0.4
        )
        
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Sales vs Customers scatter
        st.subheader("📊 Sales vs Customers")
        
        fig = px.scatter(
            filtered_df,
            x='Customers',
            y='Sales',
            color='Region',
            size='Revenue',
            title='Sales vs Customers Correlation',
            trendline='ols'
        )
        
        st.plotly_chart(fig, width='stretch')
    
    # Detailed data table
    with st.expander("📋 View Detailed Data"):
        st.dataframe(
            filtered_df.head(100),
            width='stretch'
        )

# ============ TAB 3: CHART GALLERY ============
with tab3:
    st.header("🎨 Chart Gallery")
    
    # Generate sample data
    sample_df = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D', 'E'],
        'Value1': [23, 45, 56, 78, 32],
        'Value2': [35, 28, 49, 63, 41]
    })
    
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart", 
         "Area Chart", "Box Plot", "Histogram", "Heatmap"]
    )
    
    st.markdown("---")
    
    if chart_type == "Line Chart":
        fig = px.line(
            sample_df, 
            x='Category', 
            y=['Value1', 'Value2'],
            title='Line Chart Example',
            markers=True
        )
    
    elif chart_type == "Bar Chart":
        fig = px.bar(
            sample_df,
            x='Category',
            y=['Value1', 'Value2'],
            title='Bar Chart Example',
            barmode='group'
        )
    
    elif chart_type == "Scatter Plot":
        fig = px.scatter(
            sample_df,
            x='Value1',
            y='Value2',
            size='Value1',
            color='Category',
            title='Scatter Plot Example'
        )
    
    elif chart_type == "Pie Chart":
        fig = px.pie(
            sample_df,
            names='Category',
            values='Value1',
            title='Pie Chart Example',
            hole=0.3
        )
    
    elif chart_type == "Area Chart":
        fig = px.area(
            sample_df,
            x='Category',
            y='Value1',
            title='Area Chart Example'
        )
    
    elif chart_type == "Box Plot":
        # Generate distribution data
        box_data = pd.DataFrame({
            'Category': np.repeat(['A', 'B', 'C'], 50),
            'Value': np.concatenate([
                np.random.normal(50, 10, 50),
                np.random.normal(60, 15, 50),
                np.random.normal(55, 12, 50)
            ])
        })
        
        fig = px.box(
            box_data,
            x='Category',
            y='Value',
            title='Box Plot Example'
        )
    
    elif chart_type == "Histogram":
        hist_data = np.random.normal(100, 15, 1000)
        
        fig = px.histogram(
            x=hist_data,
            title='Histogram Example',
            nbins=30,
            labels={'x': 'Value'}
        )
    
    elif chart_type == "Heatmap":
        # Generate correlation matrix
        corr_data = np.random.randn(5, 5)
        
        fig = px.imshow(
            corr_data,
            title='Heatmap Example',
            labels=dict(x="X Axis", y="Y Axis", color="Value"),
            x=['A', 'B', 'C', 'D', 'E'],
            y=['A', 'B', 'C', 'D', 'E'],
            color_continuous_scale='RdBu'
        )
    
    st.plotly_chart(fig, width='stretch')
    
    # Show code
    with st.expander("📝 View Code"):
        st.code(f"""
import plotly.express as px

fig = px.{chart_type.lower().replace(' ', '_')}(...)
st.plotly_chart(fig, width='stretch')
        """, language="python")

# ============ TAB 4: QUIZ ============
with tab4:
    st.header("🧪 Knowledge Check")
    
    q1 = st.radio(
        "Q1: Which is faster for simple charts?",
        ["st.line_chart()", "plotly.express", "matplotlib"]
    )
    
    q2 = st.radio(
        "Q2: What does width='stretch' do?",
        [
            "Makes chart taller",
            "Makes chart responsive to container width",
            "Adds a border"
        ]
    )
    
    q3 = st.radio(
        "Q3: Which chart type shows correlation?",
        ["Pie chart", "Bar chart", "Scatter plot"]
    )
    
    q4 = st.radio(
        "Q4: How to make Plotly charts interactive?",
        [
            "Add interactive=True",
            "They're interactive by default",
            "Use st.interactive()"
        ]
    )
    
    q5 = st.checkbox("Q5: Plotly charts support zoom, pan, and hover tooltips")
    
    if st.button("Check Answers", type="primary"):
        score = 0
        
        if q1 == "st.line_chart()":
            score += 1
        if q2 == "Makes chart responsive to container width":
            score += 1
        if q3 == "Scatter plot":
            score += 1
        if q4 == "They're interactive by default":
            score += 1
        if q5:
            score += 1
        
        st.write(f"### Score: {score}/5")
        
        if score == 5:
            st.success("🎉 Excellent! You're a visualization pro!")
            st.balloons()
        elif score >= 3:
            st.info("👍 Good work! Review chart types.")
        else:
            st.warning("📖 Please review visualization concepts.")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 4 - Session State")
with col2:
    st.info("➡️ **Next:** Chapter 6 - Multi-Page Architecture")