import json
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io

st.set_page_config(
    page_title="Chapter 16: Databricks",
    page_icon="🧱",
    layout="wide"
)

st.title("🧱 Chapter 16: Databricks Integration (Hands-On)")
st.markdown("---")

# Check if Databricks credentials are configured
def check_databricks_config():
    """Check if Databricks secrets are configured"""
    try:
        required_keys = ["server_hostname", "http_path", "access_token"]
        for key in required_keys:
            if key not in st.secrets.get("databricks", {}):
                return False
        return True
    except:
        return False

has_databricks = check_databricks_config()

if not has_databricks:
    st.error("⚠️ Databricks credentials not configured!")
    st.info("""
    **To use Databricks features, add to `.streamlit/secrets.toml`:**
```toml
    [databricks]
    server_hostname = "your-workspace.cloud.databricks.com"
    http_path = "/sql/1.0/warehouses/your-warehouse-id"
    access_token = "dapi..."
    catalog = "main"
    schema = "default"
    volume_path = "/Volumes/main/default/my_volume"
```
    """)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 Setup Guide",
    "🗄️ Table Operations",
    "📁 Volume Operations",
    "🔗 Full Demo",
    "💻 Code Examples"
])

# ============ TAB 1: SETUP GUIDE ============
with tab1:
    st.header("📖 Complete Setup Guide")
    
    st.markdown("""
    ## 🎯 Step-by-Step Setup
    
    Follow these steps to connect your Streamlit app to Databricks.
    """)
    
    # Step 1
    with st.expander("1️⃣ Get Databricks Workspace Credentials", expanded=True):
        st.markdown("""
        ### A. Get SQL Warehouse Connection Details
        
        1. Open your Databricks workspace
        2. Go to **SQL Warehouses** (in left sidebar)
        3. Click on your SQL Warehouse (or create one if none exists)
        4. Click **"Connection Details"** tab
        5. Copy these values:
           - **Server hostname**: `adb-123456789.azuredatabricks.net` (or similar)
           - **HTTP path**: `/sql/1.0/warehouses/abc123xyz`
        
        ### B. Generate Access Token
        
        1. Click your profile icon (top right)
        2. Go to **Settings** → **Developer**
        3. Click **"Manage"** next to "Access tokens"
        4. Click **"Generate new token"**
        5. Give it a name: "Streamlit App Token"
        6. Set expiration (e.g., 90 days)
        7. Click **"Generate"**
        8. **Copy the token immediately** (you won't see it again!)
        
        ⚠️ **Important:** Keep this token secure! Treat it like a password.
        """)
        
        st.image("https://docs.databricks.com/_images/sql-warehouse-connection-details.png", 
                caption="Example: SQL Warehouse Connection Details", width=600)
    
    # Step 2
    with st.expander("2️⃣ Install Required Package"):
        st.markdown("""
        ### Install Databricks SQL Connector
        
        Add to your `requirements.txt`:
```
        databricks-sql-connector>=3.0.0
```
        
        Or install locally:
```bash
        pip install databricks-sql-connector
```
        """)
        
        st.code("""
# requirements.txt
streamlit>=1.31.0
pandas>=2.1.0
plotly>=5.18.0
databricks-sql-connector>=3.0.0
        """, language="text")
    
    # Step 3
    with st.expander("3️⃣ Configure Secrets"):
        st.markdown("""
        ### Create `.streamlit/secrets.toml`
        
        Create this file in your project root:
```
        your_project/
        ├── .streamlit/
        │   └── secrets.toml    ← Create this file
        ├── pages/
        ├── app.py
        └── requirements.txt
```
        """)
        
        st.code("""
# .streamlit/secrets.toml

[databricks]
# SQL Warehouse connection
server_hostname = "adb-123456789.azuredatabricks.net"
http_path = "/sql/1.0/warehouses/abc123xyz"
access_token = "dapi1234567890abcdef..."

# Unity Catalog settings
catalog = "main"
schema = "default"

# Volume path (optional, if using volumes)
volume_path = "/Volumes/main/default/my_volume"
        """, language="toml")
        
        st.warning("""
        ⚠️ **Security:**
        - Add `secrets.toml` to `.gitignore`
        - Never commit tokens to Git
        - Rotate tokens regularly
        """)
    
    # Step 4
    with st.expander("4️⃣ Create Test Table and Volume"):
        st.markdown("""
        ### A. Create a Test Table
        
        Run this in a Databricks SQL notebook:
        """)
        
        st.code("""
-- Create catalog and schema (if not exists)
CREATE CATALOG IF NOT EXISTS main;
CREATE SCHEMA IF NOT EXISTS main.default;

-- Create test table
CREATE TABLE IF NOT EXISTS main.default.streamlit_test (
    id INT,
    name STRING,
    value DOUBLE,
    created_at TIMESTAMP
) USING DELTA;

-- Insert sample data
INSERT INTO main.default.streamlit_test VALUES
(1, 'Test A', 100.5, current_timestamp()),
(2, 'Test B', 200.3, current_timestamp()),
(3, 'Test C', 150.7, current_timestamp());

-- Verify
SELECT * FROM main.default.streamlit_test;
        """, language="sql")
        
        st.markdown("""
        ### B. Create a Test Volume
        
        Run this in Databricks SQL:
        """)
        
        st.code("""
-- Create volume for file storage
CREATE VOLUME IF NOT EXISTS main.default.streamlit_volume;

-- Grant permissions (if needed)
GRANT READ_VOLUME ON VOLUME main.default.streamlit_volume TO `your_user@email.com`;
GRANT WRITE_VOLUME ON VOLUME main.default.streamlit_volume TO `your_user@email.com`;
        """, language="sql")
    
    # Step 5
    with st.expander("5️⃣ Test Connection"):
        st.markdown("""
        ### Test Your Connection
        
        Use the button below to verify everything is working!
        """)
        
        if st.button("🧪 Test Connection Now", type="primary"):
            if not has_databricks:
                st.error("❌ Please configure secrets first (see Step 3)")
            else:
                with st.spinner("Testing connection..."):
                    try:
                        from databricks import sql
                        
                        # Test connection
                        connection = sql.connect(
                            server_hostname=st.secrets["databricks"]["server_hostname"],
                            http_path=st.secrets["databricks"]["http_path"],
                            access_token=st.secrets["databricks"]["access_token"]
                        )
                        
                        cursor = connection.cursor()
                        cursor.execute("SELECT 1 as test")
                        result = cursor.fetchone()
                        
                        if result[0] == 1:
                            st.success("✅ Connection successful!")
                            st.balloons()
                            
                            # Show connection details (without sensitive info)
                            st.info(f"""
                            **Connected to:**
                            - Server: {st.secrets["databricks"]["server_hostname"]}
                            - Catalog: {st.secrets["databricks"].get("catalog", "N/A")}
                            - Schema: {st.secrets["databricks"].get("schema", "N/A")}
                            """)
                        
                        cursor.close()
                        connection.close()
                        
                    except Exception as e:
                        st.error(f"❌ Connection failed: {str(e)}")
                        st.info("""
                        **Troubleshooting:**
                        - Verify SQL Warehouse is running
                        - Check credentials are correct
                        - Ensure token hasn't expired
                        - Check network/firewall settings
                        """)

# ============ TAB 2: TABLE OPERATIONS ============
with tab2:
    st.header("🗄️ Databricks Table Operations")
    
    if not has_databricks:
        st.warning("⚠️ Configure Databricks credentials first (see Setup Guide tab)")
        st.stop()
    
    # Connection helper
    @st.cache_resource
    def get_databricks_connection():
        """Create cached Databricks SQL connection"""
        from databricks import sql
        return sql.connect(
            server_hostname=st.secrets["databricks"]["server_hostname"],
            http_path=st.secrets["databricks"]["http_path"],
            access_token=st.secrets["databricks"]["access_token"]
        )
    
    # Read table function
    @st.cache_data(ttl=300)
    def read_table(table_name, limit=100):
        """Read data from Databricks table"""
        try:
            connection = get_databricks_connection()
            cursor = connection.cursor()
            
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
            cursor.execute(query)
            
            # Fetch as Arrow table and convert to pandas
            result = cursor.fetchall_arrow().to_pandas()
            
            cursor.close()
            return result, None
        except Exception as e:
            return None, str(e)
    
    # Operation tabs
    op_tab1, op_tab2, op_tab3, op_tab4 = st.tabs([
        "📖 Read (SELECT)",
        "➕ Create (INSERT)",
        "✏️ Update",
        "🗑️ Delete"
    ])
    
    # READ Operation
    with op_tab1:
        st.subheader("📖 Read Data from Table")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            table_name = st.text_input(
                "Table Name",
                value=f"{st.secrets['databricks'].get('catalog', 'main')}.{st.secrets['databricks'].get('schema', 'default')}.streamlit_test",
                help="Format: catalog.schema.table"
            )
        
        with col2:
            limit = st.number_input("Limit", min_value=1, max_value=10000, value=100)
        
        if st.button("📊 Load Table", type="primary"):
            with st.spinner(f"Loading {table_name}..."):
                df, error = read_table(table_name, limit)
                
                if error:
                    st.error(f"❌ Error: {error}")
                    
                    with st.expander("💡 Common Issues"):
                        st.markdown("""
                        **Table not found:**
                        - Check table exists: Run `SHOW TABLES IN catalog.schema`
                        - Verify spelling and catalog.schema.table format
                        
                        **Permission denied:**
                        - Grant access: `GRANT SELECT ON TABLE catalog.schema.table TO user`
                        
                        **SQL Warehouse not running:**
                        - Start warehouse in Databricks UI
                        """)
                else:
                    st.success(f"✅ Loaded {len(df)} rows from {table_name}")
                    
                    # Show metrics
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
                        f"{table_name.split('.')[-1]}.csv",
                        "text/csv"
                    )
        
        # Custom SQL query
        st.markdown("---")
        st.subheader("🔍 Custom SQL Query")
        
        custom_query = st.text_area(
            "SQL Query",
            value=f"SELECT * FROM {table_name} WHERE id > 1",
            height=100
        )
        
        if st.button("▶️ Execute Query"):
            try:
                connection = get_databricks_connection()
                cursor = connection.cursor()
                
                cursor.execute(custom_query)
                result_df = cursor.fetchall_arrow().to_pandas()
                
                st.success(f"✅ Query executed successfully! Got {len(result_df)} rows")
                st.dataframe(result_df, use_container_width=True)
                
                cursor.close()
                
            except Exception as e:
                st.error(f"❌ Query failed: {str(e)}")
    
    # CREATE Operation
    with op_tab2:
        st.subheader("➕ Insert Data into Table")
        
        insert_table = st.text_input(
            "Target Table",
            value=f"{st.secrets['databricks'].get('catalog', 'main')}.{st.secrets['databricks'].get('schema', 'default')}.streamlit_test",
            key="insert_table"
        )
        
        st.markdown("**Enter values to insert:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            insert_id = st.number_input("ID", min_value=1, value=10)
        
        with col2:
            insert_name = st.text_input("Name", value="New Entry")
        
        with col3:
            insert_value = st.number_input("Value", value=100.0)
        
        if st.button("➕ Insert Row", type="primary"):
            try:
                connection = get_databricks_connection()
                cursor = connection.cursor()
                
                query = f"""
                INSERT INTO {insert_table} (id, name, value, created_at)
                VALUES ({insert_id}, '{insert_name}', {insert_value}, current_timestamp())
                """
                
                cursor.execute(query)
                
                st.success(f"✅ Inserted row into {insert_table}")
                st.code(query, language="sql")
                
                # Clear cache to see new data
                read_table.clear()
                
                cursor.close()
                
            except Exception as e:
                st.error(f"❌ Insert failed: {str(e)}")
    
    # UPDATE Operation
    with op_tab3:
        st.subheader("✏️ Update Table Data")
        
        update_table = st.text_input(
            "Target Table",
            value=f"{st.secrets['databricks'].get('catalog', 'main')}.{st.secrets['databricks'].get('schema', 'default')}.streamlit_test",
            key="update_table"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            update_id = st.number_input("Update ID", min_value=1, value=1)
            new_value = st.number_input("New Value", value=999.9)
        
        with col2:
            new_name = st.text_input("New Name", value="Updated Entry")
        
        if st.button("✏️ Update Row", type="primary"):
            try:
                connection = get_databricks_connection()
                cursor = connection.cursor()
                
                query = f"""
                UPDATE {update_table}
                SET name = '{new_name}', value = {new_value}
                WHERE id = {update_id}
                """
                
                cursor.execute(query)
                
                st.success(f"✅ Updated row in {update_table}")
                st.code(query, language="sql")
                
                # Clear cache
                read_table.clear()
                
                cursor.close()
                
            except Exception as e:
                st.error(f"❌ Update failed: {str(e)}")
    
    # DELETE Operation
    with op_tab4:
        st.subheader("🗑️ Delete Data from Table")
        
        st.warning("⚠️ This will permanently delete data!")
        
        delete_table = st.text_input(
            "Target Table",
            value=f"{st.secrets['databricks'].get('catalog', 'main')}.{st.secrets['databricks'].get('schema', 'default')}.streamlit_test",
            key="delete_table"
        )
        
        delete_id = st.number_input("Delete ID", min_value=1, value=1)
        
        confirm = st.checkbox("I understand this will delete data permanently")
        
        if st.button("🗑️ Delete Row", type="secondary", disabled=not confirm):
            try:
                connection = get_databricks_connection()
                cursor = connection.cursor()
                
                query = f"DELETE FROM {delete_table} WHERE id = {delete_id}"
                
                cursor.execute(query)
                
                st.success(f"✅ Deleted row from {delete_table}")
                st.code(query, language="sql")
                
                # Clear cache
                read_table.clear()
                
                cursor.close()
                
            except Exception as e:
                st.error(f"❌ Delete failed: {str(e)}")
# # ============ TAB 3: VOLUME OPERATIONS ============
# with tab3:
#     st.header("📁 Databricks Volume Operations (Working Demo)")
    
#     if not has_databricks:
#         st.warning("⚠️ Configure Databricks credentials first")
#         st.stop()
    
#     # Volume helper functions

#     import requests
#     import urllib3

#     # Disable SSL warnings (optional - for development only)
#     urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#     def get_volume_api_url(file_path):
#         """Construct Databricks Files API URL"""
#         server = st.secrets["databricks"]["server_hostname"]
#         # Remove leading slash if present
#         clean_path = file_path.lstrip('/')
#         return f"https://{server}/api/2.0/fs/files/{clean_path}"

#     def get_auth_headers():
#         """Get authentication headers"""
#         return {
#             "Authorization": f"Bearer {st.secrets['databricks']['access_token']}"
#         }

#     def upload_file_to_volume(file_obj, volume_path, filename):
#         """Upload file to Databricks Volume via REST API"""
#         try:
#             # Construct full path
#             full_path = f"{volume_path}/{filename}"
#             url = get_volume_api_url(full_path)
            
#             # Prepare file data
#             files = {'file': (filename, file_obj, 'application/octet-stream')}
            
#             # Upload via PUT request (with SSL verification disabled for problematic certs)
#             response = requests.put(
#                 url,
#                 headers=get_auth_headers(),
#                 files=files,
#                 verify=False  # Disable SSL verification (use True in production with proper certs)
#             )
            
#             if response.status_code in [200, 201]:
#                 return True, f"File uploaded to {full_path}"
#             else:
#                 return False, f"Upload failed: {response.status_code} - {response.text}"
                
#         except Exception as e:
#             return False, f"Error: {str(e)}"

#     def read_file_from_volume(volume_path, filename):
#         """Read file from Databricks Volume via REST API"""
#         try:
#             full_path = f"{volume_path}/{filename}"
#             url = get_volume_api_url(full_path)
            
#             response = requests.get(
#                 url, 
#                 headers=get_auth_headers(),
#                 verify=False  # Disable SSL verification
#             )
            
#             if response.status_code == 200:
#                 return response.content, None
#             else:
#                 return None, f"Read failed: {response.status_code} - {response.text}"
                
#         except Exception as e:
#             return None, f"Error: {str(e)}"

#     def list_volume_files(volume_path):
#         """List files in Databricks Volume"""
#         try:
#             # Use directory listing API
#             server = st.secrets["databricks"]["server_hostname"]
#             url = f"https://{server}/api/2.0/fs/directory{volume_path}"
            
#             response = requests.get(
#                 url, 
#                 headers=get_auth_headers(),
#                 verify=False  # Disable SSL verification
#             )
            
#             if response.status_code == 200:
#                 data = response.json()
#                 return data.get('contents', []), None
#             else:
#                 return [], f"List failed: {response.status_code} - {response.text}"
                
#         except Exception as e:
#             return [], f"Error: {str(e)}"

#     def delete_file_from_volume(volume_path, filename):
#         """Delete file from Databricks Volume"""
#         try:
#             full_path = f"{volume_path}/{filename}"
#             url = get_volume_api_url(full_path)
            
#             response = requests.delete(
#                 url, 
#                 headers=get_auth_headers(),
#                 verify=False  # Disable SSL verification
#             )
            
#             if response.status_code in [200, 204]:
#                 return True, f"File deleted: {filename}"
#             else:
#                 return False, f"Delete failed: {response.status_code} - {response.text}"
                
#         except Exception as e:
#             return False, f"Error: {str(e)}"
    
#     # Volume configuration
#     st.subheader("📂 Volume Configuration")
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         vol_catalog = st.text_input("Catalog", value=st.secrets["databricks"].get("catalog", "main"))
    
#     with col2:
#         vol_schema = st.text_input("Schema", value=st.secrets["databricks"].get("schema", "default"))
    
#     with col3:
#         vol_name = st.text_input("Volume Name", value="streamlit_volume")
    
#     volume_path = f"/Volumes/{vol_catalog}/{vol_schema}/{vol_name}"
    
#     st.info(f"📍 **Working with volume:** `{volume_path}`")
    
#     st.markdown("---")
    
#     # Volume operations tabs
#     vol_tab1, vol_tab2, vol_tab3, vol_tab4 = st.tabs([
#         "📥 Upload File",
#         "📖 Read File",
#         "📋 List Files",
#         "🗑️ Delete File"
#     ])
    
#     # ========== UPLOAD FILE ==========
#     with vol_tab1:
#         st.subheader("📥 Upload File to Databricks Volume")
        
#         uploaded_file = st.file_uploader(
#             "Choose a file to upload",
#             type=['csv', 'txt', 'json', 'xlsx', 'pdf', 'png', 'jpg'],
#             help="Upload any file type - CSV, Excel, JSON, images, PDFs, etc."
#         )
        
#         if uploaded_file is not None:
#             # Show file info
#             col1, col2, col3 = st.columns(3)
            
#             with col1:
#                 st.metric("Filename", uploaded_file.name)
#             with col2:
#                 st.metric("Size", f"{uploaded_file.size / 1024:.2f} KB")
#             with col3:
#                 st.metric("Type", uploaded_file.type)
            
#             # Preview file content
#             st.write("**File Preview:**")
            
#             if uploaded_file.name.endswith('.csv'):
#                 try:
#                     df_preview = pd.read_csv(uploaded_file)
#                     st.dataframe(df_preview.head(10), use_container_width=True)
#                     uploaded_file.seek(0)  # Reset pointer
#                 except:
#                     st.warning("Could not preview CSV")
            
#             elif uploaded_file.name.endswith(('.xlsx', '.xls')):
#                 try:
#                     df_preview = pd.read_excel(uploaded_file)
#                     st.dataframe(df_preview.head(10), use_container_width=True)
#                     uploaded_file.seek(0)
#                 except:
#                     st.warning("Could not preview Excel")
            
#             elif uploaded_file.name.endswith('.json'):
#                 try:
#                     json_data = json.loads(uploaded_file.getvalue())
#                     st.json(json_data)
#                     uploaded_file.seek(0)
#                 except:
#                     st.warning("Could not preview JSON")
            
#             elif uploaded_file.name.endswith(('.png', '.jpg', '.jpeg')):
#                 from PIL import Image
#                 try:
#                     image = Image.open(uploaded_file)
#                     st.image(image, width=300)
#                     uploaded_file.seek(0)
#                 except:
#                     st.warning("Could not preview image")
            
#             else:
#                 st.info(f"Preview not available for {uploaded_file.type}")
            
#             st.markdown("---")
            
#             # Upload options
#             col1, col2 = st.columns([3, 1])
            
#             with col1:
#                 target_filename = st.text_input(
#                     "Save as (filename in volume)",
#                     value=uploaded_file.name
#                 )
            
#             with col2:
#                 st.write("")
#                 st.write("")
#                 upload_button = st.button("📤 Upload to Volume", type="primary", use_container_width=True)
            
#             if upload_button:
#                 with st.spinner(f"Uploading {target_filename} to Databricks Volume..."):
#                     # Reset file pointer
#                     uploaded_file.seek(0)
                    
#                     # Upload file
#                     success, message = upload_file_to_volume(
#                         uploaded_file,
#                         volume_path,
#                         target_filename
#                     )
                    
#                     if success:
#                         st.success(f"✅ {message}")
#                         st.balloons()
                        
#                         st.info(f"""
#                         **File uploaded successfully!**
                        
#                         - **Path:** `{volume_path}/{target_filename}`
#                         - **Size:** {uploaded_file.size / 1024:.2f} KB
                        
#                         You can now read this file using the "Read File" tab!
#                         """)
#                     else:
#                         st.error(f"❌ {message}")
                        
#                         with st.expander("💡 Troubleshooting"):
#                             st.markdown("""
#                             **Common issues:**
                            
#                             1. **Volume doesn't exist:**
#                                - Create volume in Databricks SQL:
# ```sql
#                                CREATE VOLUME IF NOT EXISTS main.default.streamlit_volume;
# ```
                            
#                             2. **Permission denied:**
#                                - Grant permissions:
# ```sql
#                                GRANT WRITE_VOLUME ON VOLUME main.default.streamlit_volume TO `your_email@domain.com`;
# ```
                            
#                             3. **Invalid token:**
#                                - Generate new token in Databricks
#                                - Update secrets.toml
                            
#                             4. **Network/firewall issues:**
#                                - Check if you can access Databricks URL
#                                - Verify no VPN blocking
#                             """)
    
#     # ========== READ FILE ==========
#     with vol_tab2:
#         st.subheader("📖 Read File from Databricks Volume")
        
#         read_filename = st.text_input(
#             "Filename to read",
#             value="sample.csv",
#             key="read_filename",
#             help="Enter the name of the file you uploaded"
#         )
        
#         if st.button("📖 Read File from Volume", type="primary"):
#             with st.spinner(f"Reading {read_filename} from volume..."):
#                 content, error = read_file_from_volume(volume_path, read_filename)
                
#                 if error:
#                     st.error(f"❌ {error}")
                    
#                     st.info("""
#                     **Make sure:**
#                     1. File exists in the volume (check "List Files" tab)
#                     2. Filename is correct (case-sensitive)
#                     3. You have READ_VOLUME permission
#                     """)
                
#                 else:
#                     st.success(f"✅ File read successfully!")
                    
#                     # Parse based on file type
#                     if read_filename.endswith('.csv'):
#                         try:
#                             df = pd.read_csv(io.BytesIO(content))
                            
#                             st.write(f"**Data Preview ({len(df)} rows):**")
#                             st.dataframe(df, use_container_width=True)
                            
#                             # Statistics
#                             col1, col2, col3 = st.columns(3)
#                             with col1:
#                                 st.metric("Rows", len(df))
#                             with col2:
#                                 st.metric("Columns", len(df.columns))
#                             with col3:
#                                 st.metric("Size", f"{len(content) / 1024:.2f} KB")
                            
#                             # Download option
#                             st.download_button(
#                                 "📥 Download File",
#                                 content,
#                                 read_filename,
#                                 "text/csv"
#                             )
                            
#                         except Exception as e:
#                             st.error(f"Error parsing CSV: {e}")
#                             st.write("**Raw content:**")
#                             st.text(content.decode('utf-8')[:1000])
                    
#                     elif read_filename.endswith('.json'):
#                         try:
#                             json_data = json.loads(content.decode('utf-8'))
#                             st.json(json_data)
                            
#                             st.download_button(
#                                 "📥 Download File",
#                                 content,
#                                 read_filename,
#                                 "application/json"
#                             )
#                         except Exception as e:
#                             st.error(f"Error parsing JSON: {e}")
                    
#                     elif read_filename.endswith(('.xlsx', '.xls')):
#                         try:
#                             df = pd.read_excel(io.BytesIO(content))
#                             st.dataframe(df, use_container_width=True)
                            
#                             st.download_button(
#                                 "📥 Download File",
#                                 content,
#                                 read_filename,
#                                 "application/vnd.ms-excel"
#                             )
#                         except Exception as e:
#                             st.error(f"Error parsing Excel: {e}")
                    
#                     elif read_filename.endswith(('.png', '.jpg', '.jpeg')):
#                         try:
#                             from PIL import Image
#                             image = Image.open(io.BytesIO(content))
#                             st.image(image, caption=read_filename)
                            
#                             st.download_button(
#                                 "📥 Download File",
#                                 content,
#                                 read_filename,
#                                 "image/png"
#                             )
#                         except Exception as e:
#                             st.error(f"Error displaying image: {e}")
                    
#                     elif read_filename.endswith('.txt'):
#                         st.text_area("File Content", content.decode('utf-8'), height=300)
                        
#                         st.download_button(
#                             "📥 Download File",
#                             content,
#                             read_filename,
#                             "text/plain"
#                         )
                    
#                     else:
#                         st.info(f"File type: {read_filename.split('.')[-1]}")
#                         st.write(f"**File size:** {len(content) / 1024:.2f} KB")
                        
#                         st.download_button(
#                             "📥 Download File",
#                             content,
#                             read_filename,
#                             "application/octet-stream"
#                         )
    
#     # ========== LIST FILES ==========
#     with vol_tab3:
#         st.subheader("📋 List Files in Volume")
        
#         st.write(f"**Volume Path:** `{volume_path}`")
        
#         col1, col2 = st.columns([3, 1])
        
#         with col1:
#             subfolder = st.text_input(
#                 "Subfolder (optional)",
#                 value="",
#                 placeholder="Leave empty for root or enter subfolder name",
#                 help="e.g., 'data' or 'reports/2024'"
#             )
        
#         with col2:
#             st.write("")
#             st.write("")
#             list_button = st.button("📂 List Files", use_container_width=True, type="primary")
        
#         if list_button:
#             search_path = f"{volume_path}/{subfolder}" if subfolder else volume_path
            
#             with st.spinner(f"Listing files in {search_path}..."):
#                 files, error = list_volume_files(search_path)
                
#                 if error:
#                     st.error(f"❌ {error}")
                    
#                     with st.expander("💡 How to create volume"):
#                         st.code(f"""
# -- Run this in Databricks SQL to create volume:

# CREATE VOLUME IF NOT EXISTS {vol_catalog}.{vol_schema}.{vol_name};

# -- Grant permissions:
# GRANT READ_VOLUME, WRITE_VOLUME ON VOLUME {vol_catalog}.{vol_schema}.{vol_name} 
# TO `your_email@domain.com`;
#                         """, language="sql")
                
#                 elif len(files) == 0:
#                     st.info("📭 Volume is empty. Upload some files!")
                
#                 else:
#                     st.success(f"✅ Found {len(files)} files/folders")
                    
#                     # Create dataframe from files
#                     file_data = []
#                     for item in files:
#                         file_data.append({
#                             'Name': item.get('name', 'Unknown'),
#                             'Type': '📁 Folder' if item.get('is_directory', False) else '📄 File',
#                             'Size': f"{item.get('size', 0) / 1024:.2f} KB" if not item.get('is_directory', False) else '-',
#                             'Modified': item.get('modification_time', 'Unknown')
#                         })
                    
#                     files_df = pd.DataFrame(file_data)
#                     st.dataframe(files_df, use_container_width=True)
                    
#                     # Quick actions
#                     st.markdown("---")
#                     st.write("**Quick Actions:**")
                    
#                     file_names = [f['Name'] for f in file_data if f['Type'] == '📄 File']
                    
#                     if file_names:
#                         selected_file = st.selectbox("Select file for action:", file_names)
                        
#                         col1, col2 = st.columns(2)
                        
#                         with col1:
#                             if st.button("📖 Read Selected File", use_container_width=True):
#                                 with st.spinner(f"Reading {selected_file}..."):
#                                     content, error = read_file_from_volume(search_path, selected_file)
                                    
#                                     if error:
#                                         st.error(error)
#                                     else:
#                                         st.success("✅ File read successfully!")
                                        
#                                         # Try to display based on type
#                                         if selected_file.endswith('.csv'):
#                                             df = pd.read_csv(io.BytesIO(content))
#                                             st.dataframe(df.head(20), use_container_width=True)
#                                         elif selected_file.endswith('.txt'):
#                                             st.text_area("Content", content.decode('utf-8'), height=200)
#                                         else:
#                                             st.download_button(
#                                                 "📥 Download",
#                                                 content,
#                                                 selected_file
#                                             )
                        
#                         with col2:
#                             if st.button("🗑️ Delete Selected File", type="secondary", use_container_width=True):
#                                 st.warning(f"⚠️ Delete {selected_file}?")
                                
#                                 col_a, col_b = st.columns(2)
                                
#                                 with col_a:
#                                     if st.button("✅ Confirm Delete", key="confirm_delete"):
#                                         success, message = delete_file_from_volume(search_path, selected_file)
#                                         if success:
#                                             st.success(message)
#                                             st.rerun()
#                                         else:
#                                             st.error(message)
                                
#                                 with col_b:
#                                     if st.button("❌ Cancel", key="cancel_delete"):
#                                         st.info("Cancelled")
    
#     # ========== DELETE FILE ==========
#     with vol_tab4:
#         st.subheader("🗑️ Delete File from Volume")
        
#         st.warning("⚠️ This will permanently delete the file from Databricks Volume!")
        
#         delete_filename = st.text_input(
#             "Filename to delete",
#             value="",
#             placeholder="Enter filename to delete"
#         )
        
#         confirm_delete = st.checkbox("I understand this action is permanent")
        
#         if st.button("🗑️ Delete File", type="secondary", disabled=not confirm_delete):
#             if not delete_filename:
#                 st.error("Please enter a filename")
#             else:
#                 with st.spinner(f"Deleting {delete_filename}..."):
#                     success, message = delete_file_from_volume(volume_path, delete_filename)
                    
#                     if success:
#                         st.success(f"✅ {message}")
#                         st.info("Refresh the 'List Files' tab to see updated list")
#                     else:
#                         st.error(f"❌ {message}")
    
#     st.markdown("---")
    
#     # Helper section
#     with st.expander("💡 Volume Operations Tips"):
#         st.markdown("""
#         **Best Practices:**
        
#         1. **Organize with folders:**
#            - Create structure: `/raw_data`, `/processed_data`, `/exports`
#            - Upload to: `{volume_path}/raw_data/file.csv`
        
#         2. **File naming conventions:**
#            - Use timestamps: `sales_2024_01_15.csv`
#            - Use prefixes: `raw_`, `processed_`, `final_`
#            - Avoid spaces and special characters
        
#         3. **Supported file types:**
#            - ✅ CSV, Excel, JSON (structured data)
#            - ✅ TXT, MD (text files)
#            - ✅ PNG, JPG, PDF (binary files)
#            - ✅ Parquet (optimized format)
        
#         4. **Size limits:**
#            - API uploads: Up to 5MB recommended
#            - For larger files: Use Databricks CLI or notebooks
        
#         5. **Performance:**
#            - Cache reads with `@st.cache_data(ttl=300)`
#            - Batch operations when possible
#            - Use appropriate file formats (Parquet for large data)
#         """)

# ============ TAB 4: FULL DEMO ============
with tab4:
    st.header("🔗 Complete End-to-End Demo")
    
    if not has_databricks:
        st.warning("⚠️ Configure Databricks credentials first")
        st.stop()
    
    st.info("""
    **This demo shows a complete workflow:**
    1. Upload CSV to Volume
    2. Read CSV from Volume
    3. Process data
    4. Write results to Delta Table
    5. Query table and display analytics
    """)
    
    if st.button("▶️ Run Complete Pipeline", type="primary"):
        progress = st.progress(0)
        status = st.empty()
        
        try:
            # Step 1: Create sample data
            status.text("Step 1/6: Creating sample sales data...")
            progress.progress(16)
            
            sample_df = pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=50),
                'product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Watch'], 50),
                'sales': np.random.randint(1000, 5000, 50),
                'quantity': np.random.randint(1, 10, 50),
                'region': np.random.choice(['North', 'South', 'East', 'West'], 50)
            })
            
            st.success("✅ Generated 50 sample sales records")
            with st.expander("View Sample Data"):
                st.dataframe(sample_df.head(10), use_container_width=True)
            
            # Step 2: Upload to Volume
            status.text("Step 2/6: Uploading CSV to Databricks Volume...")
            progress.progress(33)
            
            csv_buffer = io.StringIO()
            sample_df.to_csv(csv_buffer, index=False)
            csv_bytes = csv_buffer.getvalue().encode('utf-8')
            
            csv_file = io.BytesIO(csv_bytes)
            filename = f"sales_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            success, message = upload_file_to_volume(csv_file, volume_path, filename)
            
            if success:
                st.success(f"✅ Uploaded to {volume_path}/{filename}")
            else:
                st.error(f"❌ Upload failed: {message}")
                st.stop()
            
            # Step 3: Read from Volume
            status.text("Step 3/6: Reading CSV from Volume...")
            progress.progress(50)
            
            content, error = read_file_from_volume(volume_path, filename)
            
            if error:
                st.error(f"❌ Read failed: {error}")
                st.stop()
            else:
                df_from_volume = pd.read_csv(io.BytesIO(content))
                st.success(f"✅ Read {len(df_from_volume)} rows from volume")
            
            # Step 4: Process data
            status.text("Step 4/6: Processing data...")
            progress.progress(66)
            
            # Aggregate by product
            summary_df = df_from_volume.groupby('product').agg({
                'sales': ['sum', 'mean', 'count'],
                'quantity': 'sum'
            }).reset_index()
            
            summary_df.columns = ['product', 'total_sales', 'avg_sales', 'num_transactions', 'total_quantity']
            
            st.success("✅ Aggregated data by product")
            with st.expander("View Processed Data"):
                st.dataframe(summary_df, use_container_width=True)
            
            # Step 5: Write to Delta Table
            status.text("Step 5/6: Writing to Delta Table...")
            progress.progress(83)
            
            connection = get_databricks_connection()
            cursor = connection.cursor()
            
            # Create table
            table_name = f"{st.secrets['databricks'].get('catalog', 'main')}.{st.secrets['databricks'].get('schema', 'default')}.sales_summary"
            
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    product STRING,
                    total_sales BIGINT,
                    avg_sales DOUBLE,
                    num_transactions BIGINT,
                    total_quantity BIGINT,
                    updated_at TIMESTAMP
                ) USING DELTA
            """)
            
            # Insert data
            for _, row in summary_df.iterrows():
                cursor.execute(f"""
                    INSERT INTO {table_name} VALUES
                    ('{row['product']}', {row['total_sales']}, {row['avg_sales']}, 
                     {row['num_transactions']}, {row['total_quantity']}, current_timestamp())
                """)
            
            st.success(f"✅ Wrote {len(summary_df)} rows to {table_name}")
            
            # Step 6: Query and visualize
            status.text("Step 6/6: Querying table and creating visualization...")
            progress.progress(100)
            
            cursor.execute(f"SELECT * FROM {table_name}")
            final_df = cursor.fetchall_arrow().to_pandas()
            
            st.success("✅ Pipeline completed successfully!")
            
            # Display results
            st.markdown("---")
            st.subheader("📊 Final Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Sales Summary Table:**")
                st.dataframe(final_df[['product', 'total_sales', 'avg_sales', 'num_transactions']], 
                           use_container_width=True)
            
            with col2:
                st.markdown("**Total Sales by Product:**")
                
                import plotly.express as px
                fig = px.bar(
                    summary_df,
                    x='product',
                    y='total_sales',
                    title='Total Sales by Product',
                    color='total_sales',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            cursor.close()
            status.text("✅ All steps completed!")
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Pipeline failed: {str(e)}")
            status.text("❌ Pipeline failed")
            
            import traceback
            with st.expander("🔍 Error Details"):
                st.code(traceback.format_exc())

# ============ TAB 5: CODE EXAMPLES ============
with tab5:
    st.header("💻 Complete Working Code")
    
    code_example = st.selectbox(
        "Select Code Example",
        [
            "Volume Upload (REST API)",
            "Volume Read (REST API)",
            "Volume List (REST API)",
            "Table Read",
            "Table Write",
            "Complete Integration"
        ]
    )
    
    if code_example == "Volume Upload (REST API)":
        st.code("""
import streamlit as st
import requests

def upload_to_volume(file_obj, volume_path, filename):
    '''Upload file to Databricks Volume using REST API'''
    
    # Construct API URL
    server = st.secrets["databricks"]["server_hostname"]
    full_path = f"{volume_path}/{filename}"
    url = f"https://{server}/api/2.0/fs/files{full_path}"
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {st.secrets['databricks']['access_token']}"
    }
    
    # Prepare file
    files = {'file': (filename, file_obj, 'application/octet-stream')}
    
    # Upload via PUT
    response = requests.put(url, headers=headers, files=files)
    
    if response.status_code in [200, 201]:
        return True, f"Uploaded to {full_path}"
    else:
        return False, f"Error: {response.status_code} - {response.text}"

# Usage
uploaded_file = st.file_uploader("Choose file")

if uploaded_file:
    success, message = upload_to_volume(
        uploaded_file,
        "/Volumes/main/default/my_volume",
        uploaded_file.name
    )
    
    if success:
        st.success(message)
    else:
        st.error(message)
        """, language="python")
    
    elif code_example == "Volume Read (REST API)":
        st.code("""
import streamlit as st
import requests
import pandas as pd
import io

def read_from_volume(volume_path, filename):
    '''Read file from Databricks Volume using REST API'''
    
    # Construct API URL
    server = st.secrets["databricks"]["server_hostname"]
    full_path = f"{volume_path}/{filename}"
    url = f"https://{server}/api/2.0/fs/files{full_path}"
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {st.secrets['databricks']['access_token']}"
    }
    
    # Read via GET
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.content, None
    else:
        return None, f"Error: {response.status_code}"

# Usage for CSV
content, error = read_from_volume("/Volumes/main/default/my_volume", "data.csv")

if not error:
    df = pd.read_csv(io.BytesIO(content))
    st.dataframe(df)
else:
    st.error(error)

# Usage for JSON
content, error = read_from_volume("/Volumes/main/default/my_volume", "data.json")

if not error:
    import json
    data = json.loads(content.decode('utf-8'))
    st.json(data)

# Usage for Images
content, error = read_from_volume("/Volumes/main/default/my_volume", "image.png")

if not error:
    from PIL import Image
    image = Image.open(io.BytesIO(content))
    st.image(image)
        """, language="python")
    
    elif code_example == "Volume List (REST API)":
        st.code("""
import streamlit as st
import requests

def list_volume(volume_path):
    '''List files in Databricks Volume'''
    
    # Construct API URL
    server = st.secrets["databricks"]["server_hostname"]
    url = f"https://{server}/api/2.0/fs/directory{volume_path}"
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {st.secrets['databricks']['access_token']}"
    }
    
    # List via GET
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('contents', []), None
    else:
        return [], f"Error: {response.status_code}"

# Usage
files, error = list_volume("/Volumes/main/default/my_volume")

if not error:
    for file in files:
        name = file['name']
        is_dir = file.get('is_directory', False)
        size = file.get('size', 0)
        
        if is_dir:
            st.write(f"📁 {name}/")
        else:
            st.write(f"📄 {name} ({size / 1024:.2f} KB)")
else:
    st.error(error)
        """, language="python")
    
    elif code_example == "Table Read":
        st.code("""
import streamlit as st
from databricks import sql
import pandas as pd

@st.cache_resource
def get_connection():
    return sql.connect(
        server_hostname=st.secrets["databricks"]["server_hostname"],
        http_path=st.secrets["databricks"]["http_path"],
        access_token=st.secrets["databricks"]["access_token"]
    )

@st.cache_data(ttl=300)
def read_table(table_name, where_clause="", limit=1000):
    '''Read from Databricks table with optional filter'''
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Build query
    query = f"SELECT * FROM {table_name}"
    if where_clause:
        query += f" WHERE {where_clause}"
    query += f" LIMIT {limit}"
    
    # Execute and fetch
    cursor.execute(query)
    df = cursor.fetchall_arrow().to_pandas()
    
    cursor.close()
    return df

# Usage
df = read_table('main.default.sales', where_clause="date >= '2024-01-01'", limit=500)
st.dataframe(df)

# Get specific columns
cursor = conn.cursor()
cursor.execute("SELECT product, SUM(sales) as total FROM main.default.sales GROUP BY product")
summary = cursor.fetchall_arrow().to_pandas()
cursor.close()
        """, language="python")
    
    elif code_example == "Table Write":
        st.code("""
from databricks import sql

def write_dataframe_to_table(df, table_name, mode='append'):
    '''Write pandas DataFrame to Databricks table'''
    
    conn = sql.connect(
        server_hostname=st.secrets["databricks"]["server_hostname"],
        http_path=st.secrets["databricks"]["http_path"],
        access_token=st.secrets["databricks"]["access_token"]
    )
    
    cursor = conn.cursor()
    
    # Create table if not exists
    if mode == 'overwrite':
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    # Infer schema from dataframe
    columns = []
    for col, dtype in df.dtypes.items():
        if dtype == 'int64':
            sql_type = 'BIGINT'
        elif dtype == 'float64':
            sql_type = 'DOUBLE'
        elif dtype == 'datetime64[ns]':
            sql_type = 'TIMESTAMP'
        else:
            sql_type = 'STRING'
        
        columns.append(f"{col} {sql_type}")
    
    create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)}) USING DELTA"
    cursor.execute(create_sql)
    
    # Insert data in batches
    batch_size = 100
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        
        values = []
        for _, row in batch.iterrows():
            row_values = []
            for val in row:
                if pd.isna(val):
                    row_values.append('NULL')
                elif isinstance(val, str):
                    row_values.append(f"'{val}'")
                else:
                    row_values.append(str(val))
            
            values.append(f"({', '.join(row_values)})")
        
        insert_sql = f"INSERT INTO {table_name} VALUES {', '.join(values)}"
        cursor.execute(insert_sql)
    
    cursor.close()
    conn.close()
    
    return True

# Usage
df = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['A', 'B', 'C'],
    'value': [100.5, 200.3, 150.7]
})

write_dataframe_to_table(df, 'main.default.my_data', mode='append')
        """, language="python")
    
    elif code_example == "Complete Integration":
        st.code("""
import streamlit as st
import pandas as pd
import requests
import io
from databricks import sql

# ==== CONFIGURATION ====
VOLUME_PATH = st.secrets["databricks"]["volume_path"]
CATALOG = st.secrets["databricks"]["catalog"]
SCHEMA = st.secrets["databricks"]["schema"]

# ==== CONNECTION ====
@st.cache_resource
def get_db_connection():
    return sql.connect(
        server_hostname=st.secrets["databricks"]["server_hostname"],
        http_path=st.secrets["databricks"]["http_path"],
        access_token=st.secrets["databricks"]["access_token"]
    )

# ==== VOLUME OPERATIONS ====
def upload_to_volume(file_obj, filename):
    server = st.secrets["databricks"]["server_hostname"]
    url = f"https://{server}/api/2.0/fs/files{VOLUME_PATH}/{filename}"
    headers = {"Authorization": f"Bearer {st.secrets['databricks']['access_token']}"}
    files = {'file': (filename, file_obj, 'application/octet-stream')}
    
    response = requests.put(url, headers=headers, files=files)
    return response.status_code in [200, 201]

def read_from_volume(filename):
    server = st.secrets["databricks"]["server_hostname"]
    url = f"https://{server}/api/2.0/fs/files{VOLUME_PATH}/{filename}"
    headers = {"Authorization": f"Bearer {st.secrets['databricks']['access_token']}"}
    
    response = requests.get(url, headers=headers)
    return response.content if response.status_code == 200 else None

# ==== TABLE OPERATIONS ====
@st.cache_data(ttl=300)
def read_table(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    df = cursor.fetchall_arrow().to_pandas()
    cursor.close()
    return df

def write_to_table(df, table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        values = ', '.join([f"'{v}'" if isinstance(v, str) else str(v) for v in row])
        cursor.execute(f"INSERT INTO {table_name} VALUES ({values})")
    
    cursor.close()
    return True

# ==== MAIN APP ====
st.title("My Databricks App")

# File upload
uploaded = st.file_uploader("Upload CSV")

if uploaded:
    # Upload to volume
    if upload_to_volume(uploaded, uploaded.name):
        st.success("✅ Uploaded to volume")
        
        # Read from volume
        content = read_from_volume(uploaded.name)
        df = pd.read_csv(io.BytesIO(content))
        
        # Write to table
        write_to_table(df, f"{CATALOG}.{SCHEMA}.my_data")
        st.success("✅ Written to table")
        
        # Display
        st.dataframe(df)
        """, language="python")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 15 - Advanced Dashboard")
with col2:
    st.success("✅ **Databricks Integration Complete!**")