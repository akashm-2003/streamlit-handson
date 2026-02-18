import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime

st.set_page_config(
    page_title="Chapter 18: Databricks Native",
    page_icon="🧱",
    layout="wide"
)

st.title("🧱 Chapter 18: Databricks Native Integration")
st.markdown("---")

# Check if running in Databricks
def is_databricks():
    return 'DATABRICKS_RUNTIME_VERSION' in os.environ

# Initialize state
if 'db_data' not in st.session_state:
    st.session_state.db_data = []

if 'operation_history' not in st.session_state:
    st.session_state.operation_history = []

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 Learn",
    "🗄️ Table Operations",
    "📁 Volume Operations",
    "⚡ Real-time Data",
    "🧪 Quiz"
])

# ============ TAB 1: LEARN ============
with tab1:
    st.header("Databricks Native Integration")
    
    # Environment check
    if is_databricks():
        st.success("✅ Running inside Databricks - Direct access available!")
        st.write(f"**Runtime Version:** {os.environ.get('DATABRICKS_RUNTIME_VERSION', 'Unknown')}")
    else:
        st.warning("⚠️ Running locally - Some features require Databricks environment")
    
    with st.expander("🎯 1. Direct Catalog Access (No Secrets!)", expanded=True):
        st.markdown("""
        **Inside Databricks, you get automatic authentication!**
        
        - ✅ No tokens needed
        - ✅ No secrets.toml needed
        - ✅ Direct Spark SQL access
        - ✅ Identity inherited from workspace
        """)
        
        st.code("""
from pyspark.sql import SparkSession

# Get Spark session (authenticated automatically)
spark = SparkSession.builder.getOrCreate()

# Read from catalog - NO SECRETS!
df = spark.sql("SELECT * FROM main.default.users").toPandas()

# Write to catalog - NO SECRETS!
spark.createDataFrame(df).write.mode('overwrite').saveAsTable('main.default.output')

# That's it! No connection strings, no tokens!
        """, language="python")
    
    with st.expander("📁 2. Direct Volume Access"):
        st.markdown("""
        **Volumes are mounted as file system paths**
        
        Access them like regular files!
        """)
        
        st.code("""
import pandas as pd

# Read CSV from volume - just use the path!
df = pd.read_csv('/Volumes/main/default/my_volume/data.csv')

# Write CSV to volume
df.to_csv('/Volumes/main/default/my_volume/output.csv', index=False)

# Read Excel
df = pd.read_excel('/Volumes/main/default/my_volume/report.xlsx')

# Read JSON
import json
with open('/Volumes/main/default/my_volume/config.json', 'r') as f:
    data = json.load(f)

# List files
import os
files = os.listdir('/Volumes/main/default/my_volume')
        """, language="python")
    
    with st.expander("⚡ 3. Optimized Patterns"):
        st.code("""
import streamlit as st
from pyspark.sql import SparkSession

# Cache Spark session
@st.cache_resource
def get_spark():
    return SparkSession.builder.getOrCreate()

spark = get_spark()

# Cache table reads
@st.cache_data(ttl=600)
def read_table(table_name):
    '''Cached for 10 minutes'''
    return spark.sql(f"SELECT * FROM {table_name}").toPandas()

# Cache with parameters
@st.cache_data(ttl=300)
def query_filtered(table_name, filter_condition):
    '''Cached per unique filter'''
    query = f"SELECT * FROM {table_name} WHERE {filter_condition}"
    return spark.sql(query).toPandas()

# Usage
df = read_table('main.default.sales')  # First call: queries DB
df = read_table('main.default.sales')  # Second call: cached!
        """, language="python")

# ============ TAB 2: TABLE OPERATIONS ============
with tab2:
    st.header("🗄️ Unity Catalog Table Operations")
    
    if not is_databricks():
        st.warning("⚠️ These operations work best inside Databricks environment")
        st.info("Deploy to Databricks Apps to use direct catalog access")
    
    # Get Spark session
    try:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.getOrCreate()
        has_spark = True
    except:
        has_spark = False
        st.error("❌ Spark not available - Deploy to Databricks to use this feature")
    
    if has_spark:
        # CRUD Interface
        st.subheader("📝 Table Management")
        
        crud_tab1, crud_tab2, crud_tab3, crud_tab4 = st.tabs([
            "➕ Create",
            "📋 Read",
            "✏️ Update",
            "🗑️ Delete"
        ])
        
        # CREATE
        with crud_tab1:
            st.markdown("### ➕ Insert Data into Table")
            
            table_name = st.text_input("Table Name", value="main.default.streamlit_demo")
            
            with st.form("create_record"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Name*")
                    email = st.text_input("Email*")
                
                with col2:
                    value = st.number_input("Value", value=0.0)
                    category = st.selectbox("Category", ["A", "B", "C"])
                
                if st.form_submit_button("➕ Insert Record", type="primary"):
                    if not name or not email:
                        st.error("Name and email are required")
                    else:
                        try:
                            # Create DataFrame
                            new_data = pd.DataFrame([{
                                'name': name,
                                'email': email,
                                'value': value,
                                'category': category,
                                'created_at': datetime.now()
                            }])
                            
                            # Convert to Spark DataFrame
                            spark_df = spark.createDataFrame(new_data)
                            
                            # Append to table
                            spark_df.write.mode('append').saveAsTable(table_name)
                            
                            st.success(f"✅ Record inserted into {table_name}")
                            st.balloons()
                            
                            # Log operation
                            st.session_state.operation_history.append({
                                'timestamp': datetime.now().strftime('%H:%M:%S'),
                                'operation': 'INSERT',
                                'table': table_name
                            })
                            
                        except Exception as e:
                            st.error(f"❌ Insert failed: {str(e)}")
        
        # READ
        with crud_tab2:
            st.markdown("### 📋 Read Data from Table")
            
            read_table = st.text_input("Table Name", value="main.default.streamlit_demo", key="read_table")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                filter_clause = st.text_input("Filter (WHERE clause)", placeholder="e.g., value > 100")
            
            with col2:
                limit = st.number_input("Limit", min_value=1, max_value=10000, value=100)
            
            if st.button("📊 Load Data", type="primary"):
                try:
                    # Build query
                    query = f"SELECT * FROM {read_table}"
                    if filter_clause:
                        query += f" WHERE {filter_clause}"
                    query += f" LIMIT {limit}"
                    
                    # Execute query
                    df = spark.sql(query).toPandas()
                    
                    st.success(f"✅ Loaded {len(df)} rows from {read_table}")
                    
                    # Metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Rows", len(df))
                    with col2:
                        st.metric("Columns", len(df.columns))
                    with col3:
                        st.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
                    
                    # Display data
                    st.dataframe(df, use_container_width=True)
                    
                    # Download option
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "📥 Download CSV",
                        csv,
                        f"{read_table.split('.')[-1]}.csv",
                        "text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Query failed: {str(e)}")
            
            st.markdown("---")
            
            # Quick queries
            st.markdown("**📋 Quick Queries:**")
            
            quick_col1, quick_col2 = st.columns(2)
            
            with quick_col1:
                if st.button("Show Catalogs", use_container_width=True):
                    catalogs = spark.sql("SHOW CATALOGS").toPandas()
                    st.dataframe(catalogs)
                
                if st.button("Show Schemas", use_container_width=True):
                    schemas = spark.sql("SHOW SCHEMAS IN main").toPandas()
                    st.dataframe(schemas)
            
            with quick_col2:
                if st.button("Show Tables", use_container_width=True):
                    tables = spark.sql("SHOW TABLES IN main.default").toPandas()
                    st.dataframe(tables)
                
                if st.button("Table Count", use_container_width=True):
                    try:
                        count = spark.sql(f"SELECT COUNT(*) as count FROM {read_table}").toPandas()
                        st.metric("Total Rows", count.iloc[0]['count'])
                    except:
                        st.error("Table not found")
        
        # UPDATE
        with crud_tab3:
            st.markdown("### ✏️ Update Table Data")
            
            update_table = st.text_input("Table Name", value="main.default.streamlit_demo", key="update_table")
            
            col1, col2 = st.columns(2)
            
            with col1:
                set_clause = st.text_input("SET clause", placeholder="e.g., value = 999, category = 'A'")
            
            with col2:
                where_clause = st.text_input("WHERE clause", placeholder="e.g., id = 1")
            
            if st.button("✏️ Update Records", type="primary"):
                if not set_clause or not where_clause:
                    st.error("Both SET and WHERE clauses are required")
                else:
                    try:
                        query = f"UPDATE {update_table} SET {set_clause} WHERE {where_clause}"
                        
                        spark.sql(query)
                        
                        st.success(f"✅ Updated records in {update_table}")
                        st.code(query, language="sql")
                        
                        # Log operation
                        st.session_state.operation_history.append({
                            'timestamp': datetime.now().strftime('%H:%M:%S'),
                            'operation': 'UPDATE',
                            'table': update_table
                        })
                        
                    except Exception as e:
                        st.error(f"❌ Update failed: {str(e)}")
        
        # DELETE
        with crud_tab4:
            st.markdown("### 🗑️ Delete Data from Table")
            
            st.warning("⚠️ This will permanently delete data!")
            
            delete_table = st.text_input("Table Name", value="main.default.streamlit_demo", key="delete_table")
            delete_where = st.text_input("WHERE clause", placeholder="e.g., id = 1 OR value < 0")
            
            confirm = st.checkbox("I understand this will delete data permanently")
            
            if st.button("🗑️ Delete Records", type="secondary", disabled=not confirm):
                if not delete_where:
                    st.error("WHERE clause is required")
                else:
                    try:
                        query = f"DELETE FROM {delete_table} WHERE {delete_where}"
                        
                        spark.sql(query)
                        
                        st.success(f"✅ Deleted records from {delete_table}")
                        st.code(query, language="sql")
                        
                    except Exception as e:
                        st.error(f"❌ Delete failed: {str(e)}")

# ============ TAB 3: VOLUME OPERATIONS ============
with tab3:
    st.header("📁 Databricks Volume Operations (Direct Access)")
    
    st.success("✅ Inside Databricks, volumes are accessible as file system paths!")
    
    # Volume configuration
    st.subheader("📂 Volume Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        vol_catalog = st.text_input("Catalog", value="main")
    
    with col2:
        vol_schema = st.text_input("Schema", value="default")
    
    with col3:
        vol_name = st.text_input("Volume Name", value="streamlit_volume")
    
    volume_path = f"/Volumes/{vol_catalog}/{vol_schema}/{vol_name}"
    st.code(volume_path, language="text")
    
    st.markdown("---")
    
    # Volume operations tabs
    vol_tab1, vol_tab2, vol_tab3, vol_tab4 = st.tabs([
        "📥 Upload File",
        "📖 Read File",
        "📋 List Files",
        "🗑️ Delete File"
    ])
    
    # UPLOAD FILE
    with vol_tab1:
        st.subheader("📥 Upload File to Volume")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'txt', 'json', 'xlsx', 'pdf', 'png', 'jpg']
        )
        
        if uploaded_file is not None:
            # Preview
            st.write("**File Info:**")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Filename", uploaded_file.name)
                st.metric("Size", f"{uploaded_file.size / 1024:.2f} KB")
            
            with col2:
                st.metric("Type", uploaded_file.type)
            
            # Preview content
            if uploaded_file.name.endswith('.csv'):
                try:
                    df_preview = pd.read_csv(uploaded_file)
                    st.write("**Preview:**")
                    st.dataframe(df_preview.head(), use_container_width=True)
                    uploaded_file.seek(0)
                except:
                    pass
            
            st.markdown("---")
            
            target_filename = st.text_input("Save as", value=uploaded_file.name)
            
            if st.button("📤 Upload to Volume", type="primary"):
                try:
                    # Full path
                    file_path = f"{volume_path}/{target_filename}"
                    
                    # Write file directly
                    with open(file_path, 'wb') as f:
                        f.write(uploaded_file.getvalue())
                    
                    st.success(f"✅ File uploaded to {file_path}")
                    st.balloons()
                    
                    st.info(f"""
                    **File saved successfully!**
                    - Path: `{file_path}`
                    - Size: {uploaded_file.size / 1024:.2f} KB
                    """)
                    
                except Exception as e:
                    st.error(f"❌ Upload failed: {str(e)}")
                    
                    with st.expander("💡 Troubleshooting"):
                        st.markdown(f"""
                        **Volume doesn't exist?**
                        
                        Run this in Databricks SQL:
                        ```sql
                        CREATE VOLUME IF NOT EXISTS {vol_catalog}.{vol_schema}.{vol_name};
                        ```
                        
                        **Permission denied?**
                        
                        Grant permissions:
                        ```sql
                        GRANT WRITE_VOLUME ON VOLUME {vol_catalog}.{vol_schema}.{vol_name} 
                        TO `your_email@domain.com`;
                        ```
                        """)
    
    # READ FILE
    with vol_tab2:
        st.subheader("📖 Read File from Volume")
        
        read_filename = st.text_input("Filename", value="sample.csv", key="read_file")
        
        if st.button("📖 Read File", type="primary"):
            try:
                file_path = f"{volume_path}/{read_filename}"
                
                # Check if exists
                if not os.path.exists(file_path):
                    st.error(f"❌ File not found: {file_path}")
                else:
                    # Read based on file type
                    if read_filename.endswith('.csv'):
                        df = pd.read_csv(file_path)
                        
                        st.success(f"✅ Read {len(df)} rows from {file_path}")
                        
                        # Show stats
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Rows", len(df))
                        with col2:
                            st.metric("Columns", len(df.columns))
                        with col3:
                            file_size = os.path.getsize(file_path)
                            st.metric("Size", f"{file_size / 1024:.2f} KB")
                        
                        st.dataframe(df, use_container_width=True)
                        
                        # Download
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button("📥 Download", csv, read_filename, "text/csv")
                    
                    elif read_filename.endswith('.json'):
                        import json
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                        
                        st.success(f"✅ Read JSON from {file_path}")
                        st.json(data)
                    
                    elif read_filename.endswith('.txt'):
                        with open(file_path, 'r') as f:
                            content = f.read()
                        
                        st.success(f"✅ Read text file")
                        st.text_area("Content", content, height=300)
                    
                    elif read_filename.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(file_path)
                        
                        st.success(f"✅ Read Excel file")
                        st.dataframe(df, use_container_width=True)
                    
                    elif read_filename.endswith(('.png', '.jpg', '.jpeg')):
                        from PIL import Image
                        image = Image.open(file_path)
                        
                        st.success(f"✅ Read image file")
                        st.image(image, caption=read_filename, width=400)
                    
                    else:
                        file_size = os.path.getsize(file_path)
                        st.info(f"File exists ({file_size / 1024:.2f} KB)")
                        
                        with open(file_path, 'rb') as f:
                            st.download_button("📥 Download", f.read(), read_filename)
                    
            except Exception as e:
                st.error(f"❌ Read failed: {str(e)}")
    
    # LIST FILES
    with vol_tab3:
        st.subheader("📋 List Files in Volume")
        
        subfolder = st.text_input("Subfolder (optional)", value="", placeholder="Leave empty for root")
        
        if st.button("📂 List Files", type="primary"):
            try:
                search_path = f"{volume_path}/{subfolder}" if subfolder else volume_path
                
                if not os.path.exists(search_path):
                    st.error(f"❌ Path not found: {search_path}")
                else:
                    files = os.listdir(search_path)
                    
                    if not files:
                        st.info("📭 Folder is empty")
                    else:
                        st.success(f"✅ Found {len(files)} items")
                        
                        # Create file list
                        file_data = []
                        for item in files:
                            item_path = os.path.join(search_path, item)
                            
                            is_dir = os.path.isdir(item_path)
                            size = 0 if is_dir else os.path.getsize(item_path)
                            
                            file_data.append({
                                'Name': item,
                                'Type': '📁 Folder' if is_dir else '📄 File',
                                'Size': '-' if is_dir else f"{size / 1024:.2f} KB"
                            })
                        
                        df = pd.DataFrame(file_data)
                        st.dataframe(df, use_container_width=True)
                        
            except Exception as e:
                st.error(f"❌ List failed: {str(e)}")
    
    # DELETE FILE
    with vol_tab4:
        st.subheader("🗑️ Delete File from Volume")
        
        st.warning("⚠️ This will permanently delete the file!")
        
        delete_filename = st.text_input("Filename to delete", value="")
        
        confirm_delete = st.checkbox("I understand this is permanent")
        
        if st.button("🗑️ Delete File", type="secondary", disabled=not confirm_delete):
            if not delete_filename:
                st.error("Please enter a filename")
            else:
                try:
                    file_path = f"{volume_path}/{delete_filename}"
                    
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        st.success(f"✅ Deleted {delete_filename}")
                    else:
                        st.error(f"❌ File not found: {delete_filename}")
                        
                except Exception as e:
                    st.error(f"❌ Delete failed: {str(e)}")

# ============ TAB 4: REAL-TIME DATA ============
with tab4:
    st.header("⚡ Real-time Data Updates")
    
    st.subheader("1️⃣ Auto-Refresh from Catalog")
    
    auto_refresh = st.checkbox("🔄 Enable Auto-Refresh (every 5 seconds)")
    
    placeholder = st.empty()
    
    if auto_refresh and has_spark:
        if 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = time.time()
        
        elapsed = time.time() - st.session_state.last_refresh
        
        if elapsed >= 5:
            st.session_state.last_refresh = time.time()
            st.rerun()
        
        remaining = 5 - int(elapsed)
        
        with placeholder.container():
            st.info(f"⏱️ Next refresh in: {remaining} seconds")
            
            try:
                # Query live data
                current_time = datetime.now().strftime('%H:%M:%S')
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Current Time", current_time)
                
                with col2:
                    # Simulate live value
                    value = time.time() % 100
                    st.metric("Live Value", f"{value:.2f}")
                
                with col3:
                    st.metric("Refresh Count", st.session_state.get('refresh_count', 0))
                
            except Exception as e:
                st.error(f"Query failed: {str(e)}")
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
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        st.metric("Refresh Count", st.session_state.refresh_count)
    
    with col3:
        st.metric("Last Update", datetime.now().strftime('%H:%M:%S'))
    
    st.markdown("---")
    
    # Operation history
    st.subheader("📜 Recent Operations")
    
    if st.session_state.operation_history:
        for op in reversed(st.session_state.operation_history[-10:]):
            st.write(f"**{op['timestamp']}** - {op['operation']} on {op['table']}")
    else:
        st.info("No operations yet")

# ============ TAB 5: QUIZ ============
with tab5:
    st.header("🧪 Knowledge Check")
    
    q1 = st.radio(
        "Q1: Inside Databricks, how do you access catalog tables?",
        ["Use SQL connector with secrets", "Use Spark SQL directly", "Use REST API"]
    )
    
    q2 = st.radio(
        "Q2: How to read CSV from Databricks volume?",
        [
            "Use REST API",
            "pd.read_csv('/Volumes/catalog/schema/volume/file.csv')",
            "Use databricks-sql-connector"
        ]
    )
    
    q3 = st.checkbox("Q3: Spark session is automatically authenticated inside Databricks")
    
    q4 = st.radio(
        "Q4: Best practice for Spark session in Streamlit?",
        [
            "Create new session every time",
            "Cache with @st.cache_resource",
            "Use global variable"
        ]
    )
    
    q5 = st.radio(
        "Q5: To write DataFrame to catalog table:",
        [
            "Use df.to_sql()",
            "spark.createDataFrame(df).write.saveAsTable()",
            "Use INSERT statements manually"
        ]
    )
    
    if st.button("✅ Check Answers", type="primary"):
        score = 0
        feedback = []
        
        if q1 == "Use Spark SQL directly":
            score += 1
            feedback.append("✅ Q1: Correct! Direct Spark SQL access")
        else:
            feedback.append("❌ Q1: Use Spark SQL directly (no secrets needed)")
        
        if q2 == "pd.read_csv('/Volumes/catalog/schema/volume/file.csv')":
            score += 1
            feedback.append("✅ Q2: Correct! Direct file path")
        else:
            feedback.append("❌ Q2: Use pd.read_csv with volume path")
        
        if q3:
            score += 1
            feedback.append("✅ Q3: Correct! Auto-authenticated")
        else:
            feedback.append("❌ Q3: Spark is auto-authenticated in Databricks")
        
        if q4 == "Cache with @st.cache_resource":
            score += 1
            feedback.append("✅ Q4: Correct! Cache Spark session")
        else:
            feedback.append("❌ Q4: Use @st.cache_resource for Spark")
        
        if q5 == "spark.createDataFrame(df).write.saveAsTable()":
            score += 1
            feedback.append("✅ Q5: Correct!")
        else:
            feedback.append("❌ Q5: Use Spark write methods")
        
        st.markdown("---")
        st.write(f"### 🎯 Score: {score}/5")
        
        for fb in feedback:
            st.write(fb)
        
        if score == 5:
            st.success("🎉 Perfect! You understand Databricks native integration!")
            st.balloons()
        elif score >= 3:
            st.info("👍 Good! Review direct access methods.")
        else:
            st.warning("📖 Please review Databricks concepts.")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 17 - Advanced Charts")
with col2:
    st.success("✅ **Databricks Native Integration Complete!**")