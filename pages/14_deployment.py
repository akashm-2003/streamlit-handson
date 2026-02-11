import streamlit as st
import os
from datetime import datetime

st.set_page_config(
    page_title="Chapter 14: Deployment",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Chapter 14: Deployment & Secrets Management")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 Learn",
    "🔐 Secrets Management",
    "☁️ Deployment Options",
    "✅ Production Checklist",
    "🎓 Course Complete"
])

# ============ TAB 1: LEARN ============
with tab1:
    st.header("Deployment Concepts")
    
    with st.expander("🚀 1. Deployment Overview", expanded=True):
        st.markdown("""
        **What is deployment?**
        - Making your app accessible on the internet
        - Moving from local development to production
        - Serving your app to real users
        
        **Key differences: Development vs Production**
        
        | Aspect | Development | Production |
        |--------|-------------|------------|
        | **Environment** | Your laptop | Cloud server |
        | **URL** | localhost:8501 | yourdomain.com |
        | **Data** | Test/sample data | Real user data |
        | **Security** | Relaxed | Strict (HTTPS, auth) |
        | **Performance** | Single user | Multiple concurrent users |
        | **Secrets** | In code (bad!) | Environment variables |
        | **Errors** | Show full trace | Hide sensitive info |
        """)
    
    with st.expander("🔐 2. Secrets Management"):
        st.markdown("""
        **What are secrets?**
        - API keys
        - Database passwords
        - Authentication tokens
        - Encryption keys
        - OAuth credentials
        
        **Why secrets management matters:**
        - ❌ Hardcoded secrets = security breach
        - ❌ Secrets in git = public exposure
        - ✅ Proper management = secure app
        """)
        
        st.code("""
# ❌ NEVER DO THIS
DATABASE_PASSWORD = "mypassword123"
API_KEY = "sk-abc123xyz"
SECRET_KEY = "super-secret-key"

# These will be visible in:
# - Your code repository
# - Git history (forever!)
# - Anyone who views your code


# ✅ USE STREAMLIT SECRETS
# Create .streamlit/secrets.toml:

[database]
host = "db.example.com"
port = 5432
username = "myapp"
password = "super-secret-password"

[api]
openai_key = "sk-abc123xyz"
stripe_key = "sk_live_xyz123"

[general]
secret_key = "your-secret-key-here"


# In your app:
import streamlit as st

db_password = st.secrets["database"]["password"]
api_key = st.secrets["api"]["openai_key"]
secret_key = st.secrets["general"]["secret_key"]
        """, language="python")
    
    with st.expander("📂 3. File Structure for Deployment"):
        st.code("""
your-streamlit-app/
├── .streamlit/
│   ├── config.toml           # App configuration
│   └── secrets.toml          # Secrets (DO NOT COMMIT!)
├── pages/
│   ├── 01_page1.py
│   ├── 02_page2.py
│   └── 03_page3.py
├── utils/
│   ├── __init__.py
│   ├── database.py           # DB functions
│   ├── auth.py               # Auth functions
│   └── api.py                # API functions
├── data/
│   └── sample_data.csv
├── .gitignore                # Must include secrets.toml!
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
├── app.py                    # Main app file
└── Dockerfile                # Optional: for Docker
        """, language="text")
        
        st.markdown("**Critical: .gitignore**")
        
        st.code("""
# .gitignore file
.streamlit/secrets.toml
*.pyc
__pycache__/
.env
.venv/
venv/
*.db
*.sqlite
.DS_Store
        """, language="text")
    
    with st.expander("📋 4. requirements.txt"):
        st.markdown("""
        **What is requirements.txt?**
        - Lists all Python packages your app needs
        - Used by deployment platforms to install dependencies
        - Must be in project root directory
        """)
        
        st.code("""
# requirements.txt
streamlit==1.31.0
pandas==2.1.4
plotly==5.18.0
numpy==1.26.3
requests==2.31.0
bcrypt==4.1.2
python-dotenv==1.0.0

# Optional: for specific features
# SQLAlchemy==2.0.25
# psycopg2-binary==2.9.9
# pymongo==4.6.1
        """, language="text")
        
        st.markdown("**Generate requirements.txt:**")
        
        st.code("""
# Option 1: From current environment
pip freeze > requirements.txt

# Option 2: Using pipreqs (only imports actually used)
pip install pipreqs
pipreqs . --force
        """, language="bash")
    
    with st.expander("⚙️ 5. Streamlit Configuration"):
        st.markdown("""
        **config.toml** - Configure app behavior
        
        Create `.streamlit/config.toml`:
        """)
        
        st.code("""
# .streamlit/config.toml

[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"

[runner]
magicEnabled = true
fastReruns = true
        """, language="toml")

# ============ TAB 2: SECRETS MANAGEMENT ============
with tab2:
    st.header("🔐 Secrets Management Guide")
    
    st.subheader("1️⃣ Streamlit Secrets (Recommended)")
    
    st.markdown("""
    **Step-by-step setup:**
    
    1. Create `.streamlit/secrets.toml` in your project
    2. Add secrets in TOML format
    3. Add to `.gitignore`
    4. Access via `st.secrets`
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📄 secrets.toml**")
        st.code("""
# .streamlit/secrets.toml

[database]
host = "localhost"
port = 5432
username = "admin"
password = "super-secret-pwd"

[api]
openai_key = "sk-abc123"
stripe_key = "sk_test_xyz"

[auth]
secret_key = "my-secret-key"
jwt_algorithm = "HS256"

# Simple key-value
debug_mode = false
app_name = "My Streamlit App"
        """, language="toml")
    
    with col2:
        st.markdown("**🐍 Usage in Python**")
        st.code("""
import streamlit as st

# Nested secrets
db_host = st.secrets["database"]["host"]
db_password = st.secrets["database"]["password"]

# Simple secrets
debug = st.secrets["debug_mode"]
app_name = st.secrets["app_name"]

# Check if secret exists
if "api" in st.secrets:
    api_key = st.secrets["api"]["openai_key"]
else:
    st.error("API key not configured")

# Use in connection
import psycopg2

conn = psycopg2.connect(
    host=st.secrets["database"]["host"],
    port=st.secrets["database"]["port"],
    user=st.secrets["database"]["username"],
    password=st.secrets["database"]["password"]
)
        """, language="python")
    
    st.markdown("---")
    
    # Demo secrets access
    st.subheader("2️⃣ Try Accessing Secrets")
    
    st.info("💡 This demo shows how to safely check for secrets")
    
    with st.expander("View Demo Code"):
        st.code("""
import streamlit as st

# Safe secret access pattern
def get_secret(key_path, default=None):
    '''Safely get nested secret with default value'''
    try:
        keys = key_path.split('.')
        value = st.secrets
        for key in keys:
            value = value[key]
        return value
    except (KeyError, AttributeError):
        return default

# Usage
api_key = get_secret('api.openai_key', 'not-configured')
db_password = get_secret('database.password', 'default-pwd')
        """, language="python")
    
    # Check actual secrets
    if st.button("🔍 Check Available Secrets"):
        try:
            # Try to access secrets
            secret_keys = list(st.secrets.keys())
            
            if secret_keys:
                st.success(f"✅ Found {len(secret_keys)} secret sections")
                
                for key in secret_keys:
                    with st.expander(f"Section: {key}"):
                        # Don't show actual values!
                        section = st.secrets[key]
                        if isinstance(section, dict):
                            for sub_key in section.keys():
                                st.write(f"✓ `{sub_key}`: {'*' * 8} (hidden)")
                        else:
                            st.write(f"✓ Value: {'*' * 8} (hidden)")
            else:
                st.warning("⚠️ No secrets configured")
                st.info("Create `.streamlit/secrets.toml` to add secrets")
        
        except FileNotFoundError:
            st.error("❌ secrets.toml not found")
            st.info("Create `.streamlit/secrets.toml` file")
    
    st.markdown("---")
    
    # Production secrets
    st.subheader("3️⃣ Secrets in Production")
    
    deployment_options = {
        "Streamlit Community Cloud": """
**On Streamlit Cloud:**

1. Go to app settings
2. Click "Secrets" section
3. Paste your secrets.toml content
4. Save changes

The secrets will be injected as environment variables.
        """,
        
        "Docker": """
**With Docker:**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

# Don't copy secrets.toml!
# Use environment variables instead

CMD ["streamlit", "run", "app.py"]
```
```bash
# Run with secrets
docker run -e DATABASE_PASSWORD="secret" \\
           -e API_KEY="key" \\
           myapp
```
        """,
        
        "Heroku": """
**On Heroku:**
```bash
# Set config vars (secrets)
heroku config:set DATABASE_PASSWORD="secret"
heroku config:set API_KEY="key"

# In your app
import os
db_password = os.getenv('DATABASE_PASSWORD')
```
        """,
        
        "AWS/GCP/Azure": """
**Cloud Platforms:**

- **AWS**: Use AWS Secrets Manager or Parameter Store
- **GCP**: Use Secret Manager
- **Azure**: Use Key Vault

All provide secure, centralized secret management.
        """
    }
    
    selected_platform = st.selectbox("Select Deployment Platform", list(deployment_options.keys()))
    
    st.markdown(deployment_options[selected_platform])

# ============ TAB 3: DEPLOYMENT OPTIONS ============
with tab3:
    st.header("☁️ Deployment Options")
    
    # Comparison table
    st.subheader("📊 Deployment Platform Comparison")
    
    comparison_df = {
        "Platform": ["Streamlit Cloud", "Heroku", "AWS/GCP/Azure", "Docker", "Render"],
        "Difficulty": ["⭐ Easy", "⭐⭐ Medium", "⭐⭐⭐ Hard", "⭐⭐ Medium", "⭐⭐ Medium"],
        "Cost": ["Free tier", "Free tier", "Pay as you go", "Server cost", "Free tier"],
        "Best For": ["Quick deploy", "Simple apps", "Enterprise", "Flexibility", "Modern apps"],
        "Setup Time": ["5 mins", "15 mins", "1+ hour", "30 mins", "10 mins"]
    }
    
    st.table(comparison_df)
    
    st.markdown("---")
    
    # Detailed guides
    deploy_option = st.selectbox(
        "Select platform for detailed guide:",
        ["Streamlit Community Cloud (Recommended)", "Docker", "Heroku", "AWS EC2"]
    )
    
    if deploy_option == "Streamlit Community Cloud (Recommended)":
        st.markdown("""
        ### 🚀 Streamlit Community Cloud
        
        **Easiest and FREE option for Streamlit apps!**
        
        **Steps:**
        
        1. **Push code to GitHub**
```bash
           git init
           git add .
           git commit -m "Initial commit"
           git remote add origin https://github.com/username/repo.git
           git push -u origin main
```
        
        2. **Go to [share.streamlit.io](https://share.streamlit.io)**
        
        3. **Sign in with GitHub**
        
        4. **Click "New app"**
        
        5. **Select your repository**
           - Repository: `username/repo`
           - Branch: `main`
           - Main file: `app.py`
        
        6. **Add secrets** (if needed)
           - Click "Advanced settings"
           - Paste secrets.toml content
        
        7. **Deploy!**
           - App URL: `https://username-repo-xxx.streamlit.app`
        
        **Features:**
        - ✅ Free hosting
        - ✅ Automatic HTTPS
        - ✅ Auto-deploys on git push
        - ✅ Built-in secrets management
        - ✅ Custom domains (paid plans)
        
        **Limits (Free tier):**
        - 1 GB memory
        - 1 vCPU
        - Public apps only
        """)
        
        st.success("🎉 **Recommended for beginners and demos!**")
    
    elif deploy_option == "Docker":
        st.markdown("""
        ### 🐳 Docker Deployment
        
        **Best for: Production, custom infrastructure**
        
        **1. Create Dockerfile:**
        """)
        
        st.code("""
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
        """, language="dockerfile")
        
        st.markdown("**2. Create .dockerignore:**")
        
        st.code("""
# .dockerignore
__pycache__
*.pyc
.git
.gitignore
.streamlit/secrets.toml
venv/
.env
*.md
        """, language="text")
        
        st.markdown("**3. Build and run:**")
        
        st.code("""
# Build image
docker build -t my-streamlit-app .

# Run container
docker run -p 8501:8501 \\
  -e DATABASE_PASSWORD="secret" \\
  -e API_KEY="key" \\
  my-streamlit-app

# Access at http://localhost:8501
        """, language="bash")
        
        st.markdown("**4. Deploy to cloud:**")
        
        st.code("""
# Push to Docker Hub
docker tag my-streamlit-app username/my-app
docker push username/my-app

# Or deploy to:
# - AWS ECS
# - Google Cloud Run
# - Azure Container Instances
# - DigitalOcean App Platform
        """, language="bash")
    
    elif deploy_option == "Heroku":
        st.markdown("""
        ### 🟣 Heroku Deployment
        
        **Steps:**
        
        **1. Install Heroku CLI**
```bash
        # Download from heroku.com/cli
```
        
        **2. Create Procfile:**
        """)
        
        st.code("""
# Procfile
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
        """, language="text")
        
        st.markdown("**3. Create setup.sh:**")
        
        st.code("""
# setup.sh
mkdir -p ~/.streamlit/

echo "\\
[server]\\n\\
headless = true\\n\\
port = $PORT\\n\\
enableCORS = false\\n\\
\\n\\
" > ~/.streamlit/config.toml
        """, language="bash")
        
        st.markdown("**4. Deploy:**")
        
        st.code("""
# Login to Heroku
heroku login

# Create app
heroku create my-streamlit-app

# Set secrets
heroku config:set DATABASE_PASSWORD="secret"
heroku config:set API_KEY="key"

# Deploy
git push heroku main

# Open app
heroku open
        """, language="bash")
    
    elif deploy_option == "AWS EC2":
        st.markdown("""
        ### ☁️ AWS EC2 Deployment
        
        **For: Full control, scalable production apps**
        
        **Steps:**
        
        1. **Launch EC2 instance**
           - Ubuntu 22.04 LTS
           - t2.micro (free tier eligible)
           - Configure security group (allow 8501)
        
        2. **SSH into instance**
```bash
           ssh -i key.pem ubuntu@ec2-xxx.compute.amazonaws.com
```
        
        3. **Setup environment**
```bash
           sudo apt update
           sudo apt install python3-pip
           pip3 install streamlit
```
        
        4. **Clone your app**
```bash
           git clone https://github.com/username/repo.git
           cd repo
           pip3 install -r requirements.txt
```
        
        5. **Run with screen (stays running)**
```bash
           screen -S streamlit
           streamlit run app.py --server.port=8501
           # Detach: Ctrl+A, then D
```
        
        6. **Access via:**
           - `http://ec2-xxx.compute.amazonaws.com:8501`
        
        **Production setup:**
        - Use Nginx as reverse proxy
        - Setup SSL with Let's Encrypt
        - Use systemd for auto-restart
        - Setup CloudWatch logging
        """)

# ============ TAB 4: PRODUCTION CHECKLIST ============
with tab4:
    st.header("✅ Production Deployment Checklist")
    
    st.markdown("""
    Before deploying to production, ensure ALL items are checked!
    """)
    
    # Checklist categories
    categories = {
        "🔐 Security": [
            "All secrets in st.secrets or environment variables",
            "secrets.toml added to .gitignore",
            "No hardcoded passwords or API keys",
            "Using bcrypt/argon2 for password hashing",
            "HTTPS enabled (SSL certificate)",
            "Input validation on all forms",
            "SQL injection prevention (parameterized queries)",
            "Rate limiting implemented",
            "CORS configured properly",
            "Security headers configured"
        ],
        
        "📦 Code Quality": [
            "requirements.txt up to date",
            "All dependencies pinned to versions",
            "No debug code or print statements",
            "Error handling implemented",
            "Logging configured",
            "Code commented and documented",
            "README.md created",
            ".gitignore configured",
            "Type hints added (optional)",
            "Code linted and formatted"
        ],
        
        "⚡ Performance": [
            "@st.cache_data used for data operations",
            "@st.cache_resource used for connections",
            "Database connections pooled/cached",
            "API calls cached with appropriate TTL",
            "Large datasets paginated",
            "Images optimized",
            "Unnecessary reruns minimized",
            "Forms used for multiple inputs",
            "Heavy computations optimized",
            "Memory usage monitored"
        ],
        
        "🎨 User Experience": [
            "Loading indicators for slow operations",
            "Clear error messages",
            "Success/failure feedback",
            "Responsive layout (mobile-friendly)",
            "Intuitive navigation",
            "Help text and tooltips",
            "Consistent styling",
            "Accessibility considered",
            "Session timeout implemented",
            "Logout functionality working"
        ],
        
        "🧪 Testing": [
            "Tested with different roles",
            "Tested on different browsers",
            "Tested on mobile devices",
            "Error scenarios handled",
            "Edge cases tested",
            "Database operations tested",
            "API integrations tested",
            "Authentication flow tested",
            "File upload/download tested",
            "Multi-user scenarios tested"
        ],
        
        "📊 Monitoring": [
            "Error logging enabled",
            "Usage analytics configured (optional)",
            "Performance monitoring setup",
            "Uptime monitoring configured",
            "Backup strategy in place",
            "Database backup scheduled",
            "Incident response plan created",
            "Health check endpoint working",
            "Resource usage monitored",
            "Alert system configured"
        ]
    }
    
    # Display checklist
    for category, items in categories.items():
        with st.expander(f"{category} ({len(items)} items)"):
            for item in items:
                st.checkbox(item, key=f"check_{category}_{item}")
    
    st.markdown("---")
    
    # Pre-deployment test
    st.subheader("🧪 Pre-Deployment Test")
    
    if st.button("Run Pre-Deployment Check", type="primary"):
        with st.spinner("Running checks..."):
            import time
            time.sleep(1)
            
            checks = {
                "requirements.txt exists": os.path.exists("requirements.txt"),
                ".gitignore exists": os.path.exists(".gitignore"),
                "README.md exists": os.path.exists("README.md"),
                "Secrets configured": True,  # Always true in demo
            }
            
            passed = sum(checks.values())
            total = len(checks)
            
            st.markdown("### Results")
            
            for check, status in checks.items():
                if status:
                    st.success(f"✅ {check}")
                else:
                    st.error(f"❌ {check}")
            
            st.metric("Checks Passed", f"{passed}/{total}")
            
            if passed == total:
                st.success("🎉 Ready for deployment!")
                st.balloons()
            else:
                st.warning("⚠️ Fix issues before deploying")

# ============ TAB 5: COURSE COMPLETE ============
with tab5:
    st.header("🎓 Course Complete!")
    
    st.balloons()
    
    st.success("""
    ### 🎉 Congratulations! You've completed the entire Streamlit course!
    """)
    
    st.markdown("---")
    
    # What you learned
    st.subheader("📚 What You've Mastered")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Core Concepts:**
        - ✅ Streamlit execution model
        - ✅ Session state management
        - ✅ Layouts and organization
        - ✅ Data handling and visualization
        - ✅ Forms and validation
        - ✅ Multi-page architecture
        - ✅ Custom navigation
        """)
    
    with col2:
        st.markdown("""
        **Advanced Topics:**
        - ✅ User authentication
        - ✅ Role-based access control
        - ✅ Caching and performance
        - ✅ Advanced security
        - ✅ Database integration
        - ✅ API integration
        - ✅ Deployment and secrets
        """)
    
    st.markdown("---")
    
    # Skills acquired
    st.subheader("💪 Skills You Can Now Apply")
    
    skills = [
        "Build full-stack web applications with Python",
        "Implement secure authentication systems",
        "Manage databases (SQLite, PostgreSQL)",
        "Integrate external APIs",
        "Deploy apps to production",
        "Optimize app performance",
        "Manage secrets securely",
        "Create multi-page applications",
        "Implement RBAC (Role-Based Access Control)",
        "Build real-time data dashboards",
        "Handle file uploads and downloads",
        "Create interactive data visualizations",
        "Implement form validation",
        "Write production-ready code"
    ]
    
    cols = st.columns(2)
    
    for i, skill in enumerate(skills):
        with cols[i % 2]:
            st.write(f"✅ {skill}")
    
    st.markdown("---")
    
    # Next steps
    st.subheader("🚀 Your Next Steps")
    
    next_steps = st.selectbox(
        "What would you like to do next?",
        [
            "Build a project",
            "Review specific topics",
            "Explore advanced features",
            "Deploy my first app",
            "Learn integration patterns"
        ]
    )
    
    if next_steps == "Build a project":
        st.markdown("""
        ### 🛠️ Project Ideas
        
        **Beginner:**
        1. Personal finance tracker
        2. Todo list with categories
        3. Data visualizer (CSV upload)
        4. Simple CRM system
        5. Habit tracker
        
        **Intermediate:**
        6. Multi-user task manager
        7. Analytics dashboard
        8. Inventory management
        9. Customer survey tool
        10. Blog/content manager
        
        **Advanced:**
        11. AI-powered chatbot
        12. Real-time monitoring system
        13. E-commerce admin panel
        14. API marketplace
        15. SaaS application
        
        **Pick one and start building!**
        """)
    
    elif next_steps == "Review specific topics":
        st.markdown("""
        ### 📖 Quick Review
        
        Navigate back to any chapter:
        - **Chapter 1-5**: Fundamentals
        - **Chapter 6-7**: Multi-page & Navigation
        - **Chapter 8-9**: Authentication & RBAC
        - **Chapter 10**: Forms & Validation
        - **Chapter 11**: Caching & Performance
        - **Chapter 12**: Advanced Security
        - **Chapter 13**: Database & API
        - **Chapter 14**: Deployment (this chapter)
        """)
    
    elif next_steps == "Explore advanced features":
        st.markdown("""
        ### 🔬 Advanced Topics to Explore
        
        **Not Covered (Yet):**
        - Custom components (JavaScript integration)
        - WebSocket for real-time updates
        - Advanced caching strategies
        - Microservices architecture
        - A/B testing implementation
        - Advanced analytics
        - CI/CD pipelines
        - Kubernetes deployment
        - Load balancing
        - Advanced monitoring (Datadog, New Relic)
        
        **Resources:**
        - [Streamlit Docs](https://docs.streamlit.io)
        - [Streamlit Forum](https://discuss.streamlit.io)
        - [GitHub Examples](https://github.com/streamlit)
        """)
    
    elif next_steps == "Deploy my first app":
        st.markdown("""
        ### 🚀 Deployment Quick Start
        
        **Option 1: Streamlit Cloud (Easiest)**
        1. Push code to GitHub
        2. Go to [share.streamlit.io](https://share.streamlit.io)
        3. Connect repository
        4. Deploy!
        
        **Option 2: Docker**
        1. Create Dockerfile
        2. Build image: `docker build -t myapp .`
        3. Run: `docker run -p 8501:8501 myapp`
        4. Deploy to cloud provider
        
        **Need help?** Review Tab 3 of this chapter!
        """)
    
    elif next_steps == "Learn integration patterns":
        st.markdown("""
        ### 🔗 Integration Patterns
        
        **Common Integrations:**
        - **OpenAI**: AI-powered features
        - **Stripe**: Payment processing
        - **SendGrid**: Email notifications
        - **Twilio**: SMS notifications
        - **AWS S3**: File storage
        - **Firebase**: Real-time database
        - **MongoDB**: Document storage
        - **Redis**: Caching layer
        - **Celery**: Background tasks
        - **Zapier**: Automation
        
        **Pattern:**
```python
        # Store API key in secrets
        api_key = st.secrets["service"]["api_key"]
        
        # Cache API calls
        @st.cache_data(ttl=600)
        def call_api(params):
            response = requests.post(
                "https://api.service.com/endpoint",
                headers={"Authorization": f"Bearer {api_key}"},
                json=params
            )
            return response.json()
```
        """)
    
    st.markdown("---")
    
    # Certificate
    st.subheader("📜 Course Completion")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 2rem; border: 3px solid #4CAF50; border-radius: 10px; background-color: #f0f8f0;'>
            <h2 style='color: #4CAF50;'>🎓 Certificate of Completion</h2>
            <p style='font-size: 1.2rem;'><strong>Streamlit Mastery Course</strong></p>
            <p>This certifies that you have successfully completed</p>
            <p><strong>14 Comprehensive Chapters</strong></p>
            <p style='margin-top: 1rem;'>covering fundamentals to advanced deployment</p>
            <p style='margin-top: 2rem; color: #666;'>Date: {}</p>
        </div>
        """.format(datetime.now().strftime('%B %d, %Y')), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Final message
    st.info("""
    ### 💬 Thank You!
    
    Thank you for completing this comprehensive Streamlit course!
    
    You now have the skills to build production-grade web applications with Python and Streamlit.
    
    **Remember:**
    - Start small, iterate quickly
    - Security first, always
    - Cache expensive operations
    - Test thoroughly before deploying
    - Keep learning and building!
    
    **Good luck with your Streamlit journey! 🚀**
    """)
    
    # Contact/Resources
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📚 Resources**
        - [Streamlit Docs](https://docs.streamlit.io)
        - [API Reference](https://docs.streamlit.io/library/api-reference)
        - [Gallery](https://streamlit.io/gallery)
        """)
    
    with col2:
        st.markdown("""
        **🤝 Community**
        - [Forum](https://discuss.streamlit.io)
        - [Discord](https://discord.gg/streamlit)
        - [GitHub](https://github.com/streamlit/streamlit)
        """)
    
    with col3:
        st.markdown("""
        **🎯 Practice**
        - Build projects
        - Share on Streamlit Cloud
        - Join hackathons
        """)

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 13 - Database & API")
with col2:
    st.success("✅ **Course Complete!** 🎉")