import streamlit as st
import hashlib
import hmac
import secrets
import json
import time
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Chapter 12: Advanced Security",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 Chapter 12: Advanced Security")
st.markdown("---")

# Initialize security state
if 'security_tokens' not in st.session_state:
    st.session_state.security_tokens = {}

if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = {}

if 'locked_accounts' not in st.session_state:
    st.session_state.locked_accounts = {}

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 Learn",
    "🔒 Password Security",
    "🎫 Token Authentication",
    "🛡️ Security Features",
    "🧪 Quiz"
])

# ============ TAB 1: LEARN ============
with tab1:
    st.header("Advanced Security Concepts")
    
    with st.expander("🔐 1. Password Hashing (Beyond Basics)", expanded=True):
        st.markdown("""
        **Why SHA256 is NOT enough for passwords:**
        - Too fast (allows brute force attacks)
        - No built-in salt
        - Not designed for passwords
        
        **Better options: bcrypt, scrypt, argon2**
        - Intentionally slow (prevents brute force)
        - Built-in salting
        - Configurable work factor
        - Industry standard for passwords
        """)
        
        st.code("""
# ❌ WEAK: SHA256 (what we used for learning)
import hashlib
weak_hash = hashlib.sha256("password".encode()).hexdigest()
# Fast = vulnerable to brute force!


# ✅ STRONG: bcrypt (production-ready)
import bcrypt

# Hash password
password = "mypassword123"
salt = bcrypt.gensalt(rounds=12)  # rounds = work factor
hashed = bcrypt.hashpw(password.encode(), salt)

# Verify password
input_password = "mypassword123"
if bcrypt.checkpw(input_password.encode(), hashed):
    print("Login successful!")


# ✅ EVEN STRONGER: argon2 (most modern)
from argon2 import PasswordHasher

ph = PasswordHasher()

# Hash password
hashed = ph.hash("mypassword123")

# Verify password
try:
    ph.verify(hashed, "mypassword123")
    print("Login successful!")
except:
    print("Invalid password")
        """, language="python")
        
        st.warning("⚠️ **Production:** Always use bcrypt or argon2, NEVER plain SHA256!")
    
    with st.expander("🎫 2. Token-Based Authentication"):
        st.markdown("""
        **Why tokens?**
        - Stateless authentication
        - Can be revoked
        - Expire automatically
        - Work across services
        - More secure than sessions alone
        
        **Types of tokens:**
        - **Session tokens**: Short-lived, server-side
        - **JWT (JSON Web Tokens)**: Self-contained, can be verified without DB
        - **API keys**: Long-lived, for programmatic access
        - **Refresh tokens**: Get new access tokens without re-login
        """)
        
        st.code("""
import secrets
from datetime import datetime, timedelta

# Generate secure random token
def generate_token():
    return secrets.token_urlsafe(32)

# Create token with expiration
def create_session_token(user_id, expires_in_hours=24):
    token = generate_token()
    
    # Store token
    st.session_state.tokens[token] = {
        'user_id': user_id,
        'created': datetime.now(),
        'expires': datetime.now() + timedelta(hours=expires_in_hours)
    }
    
    return token

# Validate token
def validate_token(token):
    if token not in st.session_state.tokens:
        return None, "Invalid token"
    
    token_data = st.session_state.tokens[token]
    
    # Check expiration
    if datetime.now() > token_data['expires']:
        del st.session_state.tokens[token]
        return None, "Token expired"
    
    return token_data['user_id'], None

# Usage
token = create_session_token(user_id='user123')
user_id, error = validate_token(token)

if error:
    st.error(error)
else:
    st.success(f"Authenticated as {user_id}")
        """, language="python")
    
    with st.expander("🗄️ 3. Secure Credential Storage"):
        st.markdown("""
        **NEVER store credentials in code!**
        
        **Options for storing secrets:**
        1. **Streamlit Secrets** (best for Streamlit apps)
        2. **Environment Variables**
        3. **Database (encrypted)**
        4. **Secret Management Services** (AWS Secrets Manager, Azure Key Vault)
        """)
        
        st.code("""
# ❌ NEVER DO THIS
DATABASE_PASSWORD = "mypassword123"  # Visible in code!
API_KEY = "sk-abc123xyz"  # Will be committed to git!


# ✅ METHOD 1: Streamlit Secrets
# Create .streamlit/secrets.toml:
# [database]
# password = "mypassword123"
# 
# [api]
# key = "sk-abc123xyz"

import streamlit as st

db_password = st.secrets["database"]["password"]
api_key = st.secrets["api"]["key"]


# ✅ METHOD 2: Environment Variables
import os

db_password = os.getenv("DATABASE_PASSWORD")
api_key = os.getenv("API_KEY")

# Set in terminal:
# export DATABASE_PASSWORD="mypassword123"
# export API_KEY="sk-abc123xyz"


# ✅ METHOD 3: Encrypted Database Storage
from cryptography.fernet import Fernet

# Generate key (do this once, store securely)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt credential
encrypted = cipher.encrypt(b"mypassword123")

# Store encrypted value in database
save_to_db(encrypted)

# Later, decrypt when needed
decrypted = cipher.decrypt(encrypted)
        """, language="python")
        
        st.error("🚨 **Critical:** Add `.streamlit/secrets.toml` to `.gitignore`!")
    
    with st.expander("🛡️ 4. Rate Limiting & Brute Force Protection"):
        st.markdown("""
        **Protect against brute force attacks:**
        - Limit login attempts
        - Lock accounts temporarily
        - Add delays after failures
        - Use CAPTCHA for repeated failures
        """)
        
        st.code("""
import streamlit as st
from datetime import datetime, timedelta

# Track failed login attempts
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = {}

if 'locked_until' not in st.session_state:
    st.session_state.locked_until = {}

def check_rate_limit(username):
    '''Check if user is rate limited'''
    
    # Check if account is locked
    if username in st.session_state.locked_until:
        unlock_time = st.session_state.locked_until[username]
        
        if datetime.now() < unlock_time:
            remaining = (unlock_time - datetime.now()).seconds
            return False, f"Account locked. Try again in {remaining}s"
        else:
            # Unlock account
            del st.session_state.locked_until[username]
            st.session_state.failed_attempts[username] = 0
    
    return True, None

def record_failed_attempt(username):
    '''Record failed login attempt'''
    
    if username not in st.session_state.failed_attempts:
        st.session_state.failed_attempts[username] = 0
    
    st.session_state.failed_attempts[username] += 1
    
    # Lock account after 5 failed attempts
    if st.session_state.failed_attempts[username] >= 5:
        # Lock for 15 minutes
        st.session_state.locked_until[username] = datetime.now() + timedelta(minutes=15)
        return True  # Account locked
    
    return False  # Not locked yet

def record_successful_login(username):
    '''Clear failed attempts on successful login'''
    if username in st.session_state.failed_attempts:
        st.session_state.failed_attempts[username] = 0

# Usage in login
def login(username, password):
    # Check rate limit
    allowed, error = check_rate_limit(username)
    if not allowed:
        return False, error
    
    # Verify credentials
    if verify_password(username, password):
        record_successful_login(username)
        return True, "Login successful"
    else:
        locked = record_failed_attempt(username)
        if locked:
            return False, "Too many failed attempts. Account locked for 15 minutes"
        else:
            attempts_left = 5 - st.session_state.failed_attempts[username]
            return False, f"Invalid password. {attempts_left} attempts remaining"
        """, language="python")
    
    with st.expander("🔑 5. Two-Factor Authentication (2FA)"):
        st.markdown("""
        **Add extra security layer:**
        - Something you know (password)
        - Something you have (phone, authenticator app)
        
        **Implementation options:**
        - SMS codes (less secure, but convenient)
        - Authenticator apps (Google Authenticator, Authy)
        - Email codes
        - Hardware keys (YubiKey)
        """)
        
        st.code("""
import pyotp  # pip install pyotp
import qrcode

# Generate secret for user (do once during setup)
def setup_2fa(username):
    # Generate secret
    secret = pyotp.random_base32()
    
    # Store secret for user
    st.session_state.user_2fa_secrets[username] = secret
    
    # Generate QR code for authenticator app
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=username,
        issuer_name="MyApp"
    )
    
    # User scans this QR code with authenticator app
    qr = qrcode.make(totp_uri)
    return qr, secret

# Verify 2FA code
def verify_2fa(username, code):
    secret = st.session_state.user_2fa_secrets.get(username)
    
    if not secret:
        return False
    
    totp = pyotp.TOTP(secret)
    
    # Verify code (valid for 30 seconds)
    return totp.verify(code, valid_window=1)

# Login with 2FA
def login_with_2fa(username, password, code):
    # First, verify password
    if not verify_password(username, password):
        return False, "Invalid password"
    
    # Then, verify 2FA code
    if not verify_2fa(username, code):
        return False, "Invalid 2FA code"
    
    return True, "Login successful"
        """, language="python")
    
    with st.expander("🔒 6. Input Sanitization (Prevent Injection)"):
        st.code("""
import re
import html

# SQL Injection Prevention
# ❌ NEVER do string formatting for SQL
query = f"SELECT * FROM users WHERE username = '{username}'"  # VULNERABLE!

# ✅ Always use parameterized queries
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))


# XSS (Cross-Site Scripting) Prevention
# ❌ Displaying user input directly
st.markdown(f"<h1>{user_input}</h1>", unsafe_allow_html=True)  # VULNERABLE!

# ✅ Escape HTML
import html
safe_input = html.escape(user_input)
st.markdown(f"<h1>{safe_input}</h1>", unsafe_allow_html=True)


# Path Traversal Prevention
# ❌ Using user input in file paths
filepath = f"uploads/{filename}"  # User could use ../../../etc/passwd

# ✅ Validate and sanitize
import os

def safe_join(base_dir, filename):
    # Remove path separators
    safe_name = filename.replace('/', '').replace('\\', '')
    
    # Remove parent directory references
    safe_name = safe_name.replace('..', '')
    
    # Join safely
    filepath = os.path.join(base_dir, safe_name)
    
    # Verify it's still inside base_dir
    if not filepath.startswith(base_dir):
        raise ValueError("Invalid filename")
    
    return filepath


# Email Validation (prevent injection)
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
        """, language="python")
    
    with st.expander("🎯 7. Security Best Practices Checklist"):
        st.markdown("""
        **Authentication:**
        - ✅ Use bcrypt/argon2 for password hashing
        - ✅ Implement rate limiting (5 attempts max)
        - ✅ Lock accounts after failed attempts
        - ✅ Use secure token generation
        - ✅ Set token expiration (24 hours max)
        - ✅ Consider 2FA for sensitive apps
        
        **Data Protection:**
        - ✅ Use HTTPS in production (always!)
        - ✅ Store secrets in st.secrets or env vars
        - ✅ Never commit secrets to git
        - ✅ Encrypt sensitive data in database
        - ✅ Use parameterized queries (prevent SQL injection)
        - ✅ Sanitize all user inputs
        
        **Session Management:**
        - ✅ Generate secure random session IDs
        - ✅ Regenerate session on login
        - ✅ Clear session on logout
        - ✅ Set session timeout
        - ✅ Validate session on every request
        
        **Application Security:**
        - ✅ Validate all inputs (frontend AND backend)
        - ✅ Use RBAC for access control
        - ✅ Log security events
        - ✅ Keep dependencies updated
        - ✅ Regular security audits
        - ✅ Error messages don't reveal system info
        """)

# ============ TAB 2: PASSWORD SECURITY ============
with tab2:
    st.header("🔒 Password Security Demo")
    
    st.subheader("1️⃣ Password Strength Checker")
    
    with st.form("password_strength"):
        password = st.text_input("Enter Password", type="password")
        
        if st.form_submit_button("Check Strength", type="primary"):
            if not password:
                st.error("Please enter a password")
            else:
                # Calculate strength
                score = 0
                feedback = []
                
                # Length check
                if len(password) >= 8:
                    score += 20
                    feedback.append("✅ Length: 8+ characters")
                else:
                    feedback.append(f"❌ Length: {len(password)}/8 characters")
                
                if len(password) >= 12:
                    score += 10
                    feedback.append("✅ Bonus: 12+ characters")
                
                # Uppercase
                if any(c.isupper() for c in password):
                    score += 15
                    feedback.append("✅ Contains uppercase letter")
                else:
                    feedback.append("❌ Missing uppercase letter")
                
                # Lowercase
                if any(c.islower() for c in password):
                    score += 15
                    feedback.append("✅ Contains lowercase letter")
                else:
                    feedback.append("❌ Missing lowercase letter")
                
                # Numbers
                if any(c.isdigit() for c in password):
                    score += 15
                    feedback.append("✅ Contains number")
                else:
                    feedback.append("❌ Missing number")
                
                # Special characters
                if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
                    score += 15
                    feedback.append("✅ Contains special character")
                else:
                    feedback.append("❌ Missing special character")
                
                # No common patterns
                common = ['password', '123456', 'qwerty', 'admin', '12345']
                if not any(c in password.lower() for c in common):
                    score += 10
                    feedback.append("✅ No common patterns")
                else:
                    score -= 30
                    feedback.append("❌ Contains common pattern!")
                
                # Display strength
                st.markdown("---")
                
                if score >= 80:
                    st.success(f"🟢 **Strong Password** (Score: {score}/100)")
                    st.progress(score / 100)
                elif score >= 50:
                    st.warning(f"🟡 **Medium Password** (Score: {score}/100)")
                    st.progress(score / 100)
                else:
                    st.error(f"🔴 **Weak Password** (Score: {score}/100)")
                    st.progress(max(score, 0) / 100)
                
                st.markdown("**Feedback:**")
                for item in feedback:
                    st.write(item)
    
    st.markdown("---")
    
    # Bcrypt demo (simulated)
    st.subheader("2️⃣ Secure Hashing Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ❌ SHA256 (Fast = Vulnerable)")
        
        test_password = "MyPassword123"
        
        # SHA256 (fast)
        import time
        start = time.time()
        sha_hash = hashlib.sha256(test_password.encode()).hexdigest()
        sha_time = time.time() - start
        
        st.code(sha_hash, language="text")
        st.warning(f"⏱️ Time: {sha_time*1000:.4f}ms (Too fast!)")
        st.write("**Problem:** Attacker can try billions of passwords per second")
    
    with col2:
        st.markdown("### ✅ bcrypt (Slow = Secure)")
        
        st.info("bcrypt intentionally adds work to slow down hashing")
        st.code("$2b$12$XxXxXxXxXxXxXxXxXxXxXx...", language="text")
        st.success("⏱️ Time: ~100-300ms (Good!)")
        st.write("**Benefit:** Attacker can only try thousands per second")
    
    st.markdown("---")
    
    # Installation guide
    with st.expander("📦 How to Use bcrypt in Your App"):
        st.code("""
# Install bcrypt
pip install bcrypt

# In your Streamlit app
import bcrypt

# Hash a password (during registration)
def hash_password(password):
    salt = bcrypt.gensalt(rounds=12)  # Higher = more secure but slower
    return bcrypt.hashpw(password.encode(), salt)

# Verify password (during login)
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

# Usage
hashed = hash_password("mypassword123")
# Store 'hashed' in database

# Later, during login
if verify_password(user_input, stored_hash):
    st.success("Login successful!")
        """, language="python")

# ============ TAB 3: TOKEN AUTHENTICATION ============
with tab3:
    st.header("🎫 Token-Based Authentication")
    
    st.subheader("Token Generation & Validation")
    
    # Token generator
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎲 Generate Token")
        
        if st.button("Generate Secure Token", use_container_width=True):
            token = secrets.token_urlsafe(32)
            
            # Store token
            st.session_state.security_tokens[token] = {
                'user': 'demo_user',
                'created': datetime.now(),
                'expires': datetime.now() + timedelta(hours=1)
            }
            
            st.success("✅ Token Generated!")
            st.code(token, language="text")
            
            st.info(f"""
            **Token Info:**
            - User: demo_user
            - Created: {datetime.now().strftime('%H:%M:%S')}
            - Expires: in 1 hour
            """)
    
    with col2:
        st.markdown("### ✅ Validate Token")
        
        test_token = st.text_input("Enter Token", placeholder="Paste token here")
        
        if st.button("Validate Token", use_container_width=True):
            if not test_token:
                st.error("Please enter a token")
            elif test_token not in st.session_state.security_tokens:
                st.error("❌ Invalid token")
            else:
                token_data = st.session_state.security_tokens[test_token]
                
                if datetime.now() > token_data['expires']:
                    st.error("❌ Token expired")
                    del st.session_state.security_tokens[test_token]
                else:
                    remaining = token_data['expires'] - datetime.now()
                    minutes = int(remaining.total_seconds() / 60)
                    
                    st.success(f"✅ Valid token for: {token_data['user']}")
                    st.info(f"⏱️ Expires in: {minutes} minutes")
    
    st.markdown("---")
    
    # API Key simulation
    st.subheader("🔑 API Key Management")
    
    if 'api_keys' not in st.session_state:
        st.session_state.api_keys = {}
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        key_name = st.text_input("API Key Name", placeholder="e.g., Production API")
    
    with col2:
        st.write("")
        st.write("")
        if st.button("Generate API Key", type="primary"):
            if key_name:
                api_key = f"sk_{secrets.token_urlsafe(32)}"
                
                st.session_state.api_keys[api_key] = {
                    'name': key_name,
                    'created': datetime.now(),
                    'last_used': None,
                    'uses': 0
                }
                
                st.success(f"✅ Created: {key_name}")
                st.code(api_key, language="text")
                st.warning("⚠️ Save this key! It won't be shown again.")
    
    # Display API keys
    if st.session_state.api_keys:
        st.markdown("### 🔑 Your API Keys")
        
        for api_key, data in list(st.session_state.api_keys.items()):
            with st.expander(f"{data['name']} - Created {data['created'].strftime('%Y-%m-%d')}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Uses:** {data['uses']}")
                
                with col2:
                    last_used = data['last_used']
                    st.write(f"**Last used:** {last_used.strftime('%Y-%m-%d %H:%M') if last_used else 'Never'}")
                
                with col3:
                    if st.button("🗑️ Revoke", key=f"revoke_{api_key}"):
                        del st.session_state.api_keys[api_key]
                        st.success("Key revoked")
                        st.rerun()
                
                st.code(api_key, language="text")

# ============ TAB 4: SECURITY FEATURES ============
with tab4:
    st.header("🛡️ Security Features Demo")
    
    # Rate limiting demo
    st.subheader("1️⃣ Rate Limiting & Account Locking")
    
    if 'demo_failed_attempts' not in st.session_state:
        st.session_state.demo_failed_attempts = 0
    
    if 'demo_locked_until' not in st.session_state:
        st.session_state.demo_locked_until = None
    
    # Check if locked
    if st.session_state.demo_locked_until:
        if datetime.now() < st.session_state.demo_locked_until:
            remaining = (st.session_state.demo_locked_until - datetime.now()).seconds
            st.error(f"🔒 Account locked! Try again in {remaining} seconds")
            
            if st.button("Reset Demo"):
                st.session_state.demo_failed_attempts = 0
                st.session_state.demo_lock