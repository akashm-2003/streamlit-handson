import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import json

st.set_page_config(
    page_title="Chapter 3: Data Handling",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Chapter 3: Working with Data")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📖 Learn",
    "🎮 Data Explorer",
    "🖼️ Image Handler",
    "🧪 Quiz"
])

# ============ TAB 1: LEARN ============
with tab1:
    st.header("Data Handling Concepts")
    
    with st.expander("📤 File Upload", expanded=True):
        st.code("""
# Basic upload
uploaded_file = st.file_uploader("Choose file")

# Specific types
uploaded_file = st.file_uploader(
    "Upload CSV",
    type=['csv', 'xlsx']
)

# Multiple files
files = st.file_uploader(
    "Upload files",
    accept_multiple_files=True
)
        """, language="python")
    
    with st.expander("📊 Reading Data"):
        st.code("""
# CSV
df = pd.read_csv(uploaded_file)

# Excel
df = pd.read_excel(uploaded_file, sheet_name='Sheet1')

# JSON
data = json.load(uploaded_file)
df = pd.DataFrame(data)
        """, language="python")
    
    with st.expander("🔍 Displaying Data"):
        st.code("""
# Interactive table (scrollable)
st.dataframe(df)

# Static table
st.table(df)

# Editable table
edited_df = st.data_editor(df)

# Metrics
st.metric("Total Rows", len(df))
        """, language="python")
    
    with st.expander("📥 Downloading Data"):
        st.code("""
# CSV download
csv = df.to_csv(index=False)
st.download_button(
    "Download CSV",
    data=csv,
    file_name='data.csv',
    mime='text/csv'
)
        """, language="python")

# ============ TAB 2: DATA EXPLORER ============
with tab2:
    st.header("🎮 Interactive Data Explorer")
    
    # File upload section
    uploaded_file = st.file_uploader(
        "📤 Upload your data (CSV or Excel)",
        type=['csv', 'xlsx', 'xls']
    )
    
    # Sample data option
    use_sample = st.checkbox("Or use sample data")
    
    df = None
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ Loaded {uploaded_file.name}")
        except Exception as e:
            st.error(f"Error loading file: {e}")
    
    elif use_sample:
        # Generate sample data
        np.random.seed(42)
        df = pd.DataFrame({
            'Name': [f'Person {i}' for i in range(1, 51)],
            'Age': np.random.randint(20, 60, 50),
            'City': np.random.choice(['NYC', 'LA', 'Chicago', 'Houston', 'Phoenix'], 50),
            'Salary': np.random.randint(40000, 120000, 50),
            'Department': np.random.choice(['Sales', 'Engineering', 'Marketing', 'HR'], 50)
        })
        st.info("📊 Using sample data with 50 rows")
    
    # If data is loaded
    if df is not None:
        st.markdown("---")
        
        # Data overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total Rows", len(df))
        with col2:
            st.metric("📋 Columns", len(df.columns))
        with col3:
            st.metric("🔢 Numeric Cols", len(df.select_dtypes(include=[np.number]).columns))
        with col4:
            st.metric("❌ Missing", df.isnull().sum().sum())
        
        st.markdown("---")
        
        # Sidebar filters
        st.sidebar.header("🔍 Filters")
        
        # Text search
        if len(df.select_dtypes(include=['object']).columns) > 0:
            text_col = st.sidebar.selectbox(
                "Search in column",
                df.select_dtypes(include=['object']).columns
            )
            search_term = st.sidebar.text_input("Search term")
            
            if search_term:
                df = df[df[text_col].astype(str).str.contains(search_term, case=False, na=False)]
        
        # Numeric filters
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            filter_col = st.sidebar.selectbox("Filter numeric column", numeric_cols)
            min_val = float(df[filter_col].min())
            max_val = float(df[filter_col].max())
            
            filter_range = st.sidebar.slider(
                f"{filter_col} range",
                min_val, max_val,
                (min_val, max_val)
            )
            
            df = df[(df[filter_col] >= filter_range[0]) & (df[filter_col] <= filter_range[1])]
        
        # Display options
        st.sidebar.markdown("---")
        st.sidebar.header("⚙️ Display Options")
        
        show_rows = st.sidebar.slider("Rows to display", 5, len(df), min(20, len(df)))
        
        # Main display
        col_left, col_right = st.columns([3, 1])
        
        with col_left:
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(show_rows), use_container_width=True)
            
            # Editable version
            if st.checkbox("🖊️ Make data editable"):
                st.info("Edit the data below. Changes are temporary.")
                edited_df = st.data_editor(df, num_rows="dynamic")
                
                if not df.equals(edited_df):
                    st.warning("⚠️ Data has been modified!")
                    df = edited_df
        
        with col_right:
            st.subheader("📊 Statistics")
            
            if len(numeric_cols) > 0:
                stat_col = st.selectbox("Select column", numeric_cols)
                
                st.metric("Mean", f"{df[stat_col].mean():.2f}")
                st.metric("Median", f"{df[stat_col].median():.2f}")
                st.metric("Std Dev", f"{df[stat_col].std():.2f}")
                st.metric("Min", f"{df[stat_col].min():.2f}")
                st.metric("Max", f"{df[stat_col].max():.2f}")
        
        st.markdown("---")
        
        # Data types and missing values
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("🔤 Data Types"):
                st.write(df.dtypes)
        
        with col2:
            with st.expander("❌ Missing Values"):
                missing = df.isnull().sum()
                if missing.sum() > 0:
                    st.write(missing[missing > 0])
                else:
                    st.success("No missing values!")
        
        # Statistical summary
        with st.expander("📈 Statistical Summary"):
            st.write(df.describe())
        
        st.markdown("---")
        
        # Download section
        st.subheader("📥 Download Processed Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # CSV download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📄 Download CSV",
                data=csv,
                file_name='processed_data.csv',
                mime='text/csv',
                use_container_width=True
            )
        
        with col2:
            # Excel download
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Data')
            
            st.download_button(
                "📊 Download Excel",
                data=buffer.getvalue(),
                file_name='processed_data.xlsx',
                mime='application/vnd.ms-excel',
                use_container_width=True
            )
        
        with col3:
            # JSON download
            json_str = df.to_json(orient='records', indent=2)
            st.download_button(
                "📋 Download JSON",
                data=json_str,
                file_name='processed_data.json',
                mime='application/json',
                use_container_width=True
            )

# ============ TAB 3: IMAGE HANDLER ============
with tab3:
    st.header("🖼️ Image Handler")
    
    uploaded_image = st.file_uploader(
        "Upload an image",
        type=['png', 'jpg', 'jpeg'],
        key="image_uploader"
    )
    
    if uploaded_image is not None:
        from PIL import Image, ImageFilter, ImageEnhance
        
        image = Image.open(uploaded_image)
        
        st.subheader("Original Image")
        st.image(image, use_column_width=True)
        
        # Image info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Width", image.size[0])
        with col2:
            st.metric("Height", image.size[1])
        with col3:
            st.metric("Format", image.format)
        
        st.markdown("---")
        
        # Image operations
        st.subheader("🎨 Image Operations")
        
        operation = st.selectbox(
            "Choose operation",
            ["Original", "Grayscale", "Blur", "Brightness", "Rotate", "Resize"]
        )
        
        processed_image = image.copy()
        
        if operation == "Grayscale":
            processed_image = image.convert('L')
        
        elif operation == "Blur":
            blur_amount = st.slider("Blur amount", 0, 10, 2)
            processed_image = image.filter(ImageFilter.GaussianBlur(blur_amount))
        
        elif operation == "Brightness":
            brightness = st.slider("Brightness", 0.5, 2.0, 1.0, 0.1)
            enhancer = ImageEnhance.Brightness(image)
            processed_image = enhancer.enhance(brightness)
        
        elif operation == "Rotate":
            angle = st.slider("Rotation angle", 0, 360, 0)
            processed_image = image.rotate(angle, expand=True)
        
        elif operation == "Resize":
            scale = st.slider("Scale %", 10, 200, 100)
            new_width = int(image.size[0] * scale / 100)
            new_height = int(image.size[1] * scale / 100)
            processed_image = image.resize((new_width, new_height))
        
        # Display processed image
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Before")
            st.image(image, use_column_width=True)
        
        with col2:
            st.subheader("After")
            st.image(processed_image, use_column_width=True)
        
        # Download processed image
        buf = BytesIO()
        processed_image.save(buf, format='PNG')
        
        st.download_button(
            "📥 Download Processed Image",
            data=buf.getvalue(),
            file_name='processed_image.png',
            mime='image/png'
        )

# ============ TAB 4: QUIZ ============
with tab4:
    st.header("🧪 Knowledge Check")
    
    q1 = st.radio(
        "Q1: Which function reads CSV files?",
        ["pd.load_csv()", "pd.read_csv()", "pd.import_csv()"]
    )
    
    q2 = st.radio(
        "Q2: What does st.dataframe() provide?",
        ["Static table", "Interactive scrollable table", "Editable table"]
    )
    
    q3 = st.radio(
        "Q3: Which function makes data editable?",
        ["st.table()", "st.dataframe()", "st.data_editor()"]
    )
    
    q4 = st.radio(
        "Q4: How to allow multiple file uploads?",
        [
            "type='multiple'",
            "accept_multiple_files=True",
            "multi=True"
        ]
    )
    
    q5 = st.checkbox("Q5: st.download_button() allows users to download data")
    
    if st.button("Check Answers", type="primary"):
        score = 0
        
        if q1 == "pd.read_csv()":
            score += 1
        if q2 == "Interactive scrollable table":
            score += 1
        if q3 == "st.data_editor()":
            score += 1
        if q4 == "accept_multiple_files=True":
            score += 1
        if q5:
            score += 1
        
        st.write(f"### Score: {score}/5")
        
        if score == 5:
            st.success("🎉 Perfect! You're a data handling expert!")
            st.balloons()
        elif score >= 3:
            st.info("👍 Good job! Review a few concepts.")
        else:
            st.warning("📖 Please review the chapter again.")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 2 - Layouts")
with col2:
    st.info("➡️ **Next:** Chapter 4 - Session State (Critical!)")