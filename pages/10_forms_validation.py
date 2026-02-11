import streamlit as st
import re
from datetime import datetime, date

st.set_page_config(
    page_title="Chapter 10: Forms & Validation",
    page_icon="📝",
    layout="wide"
)

# Initialize form state
if 'form_step' not in st.session_state:
    st.session_state.form_step = 1

if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

if 'submitted_forms' not in st.session_state:
    st.session_state.submitted_forms = []

st.title("📝 Chapter 10: Forms & Validation")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 Learn",
    "📋 Simple Forms",
    "✅ Validation Examples",
    "🪜 Multi-Step Form",
    "🧪 Quiz"
])

# ============ TAB 1: LEARN ============
with tab1:
    st.header("Forms & Validation Concepts")
    
    with st.expander("📋 1. Why Use st.form()?", expanded=True):
        st.markdown("""
        **Without forms:** Every widget interaction triggers a full rerun
        
        **With forms:** Inputs are batched, rerun only happens on submit
        
        **Benefits:**
        - Better performance (fewer reruns)
        - Group related inputs together
        - Validate all inputs before submission
        - Better user experience
        """)
        
        st.code("""
# WITHOUT form (reruns on every input!)
name = st.text_input("Name")
email = st.text_input("Email")
age = st.number_input("Age")
# Triggers 3 reruns if user fills all fields!

# WITH form (reruns only on submit)
with st.form("my_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age")
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        # All inputs captured, only 1 rerun!
        st.write(f"Hello {name}")
        """, language="python")
    
    with st.expander("✍️ 2. Basic Form Syntax"):
        st.code("""
import streamlit as st

# Create a form
with st.form("form_key"):  # Unique key required
    
    # Add inputs inside form
    name = st.text_input("Name")
    email = st.text_input("Email")
    
    # Must have submit button (required!)
    submitted = st.form_submit_button("Submit")
    
    # Handle submission
    if submitted:
        st.write(f"Name: {name}")
        st.write(f"Email: {email}")

# Alternative: form.form_submit_button()
form = st.form("my_form")
name = form.text_input("Name")
submitted = form.form_submit_button("Submit")
        """, language="python")
        
        st.warning("⚠️ **Important:** Every form MUST have a submit button!")
    
    with st.expander("✅ 3. Input Validation"):
        st.markdown("**Common Validation Patterns:**")
        
        st.code("""
import re

# Email validation
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Phone validation
def validate_phone(phone):
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None

# Password strength
def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain a number"
    return True, "Password is strong"

# Usage
if not validate_email(email):
    st.error("Invalid email format")
        """, language="python")
    
    with st.expander("🪜 4. Multi-Step Forms"):
        st.code("""
import streamlit as st

# Initialize step
if 'step' not in st.session_state:
    st.session_state.step = 1

# Step 1
if st.session_state.step == 1:
    with st.form("step1"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        
        if st.form_submit_button("Next"):
            if name and email:
                st.session_state.form_data = {'name': name, 'email': email}
                st.session_state.step = 2
                st.rerun()

# Step 2
elif st.session_state.step == 2:
    with st.form("step2"):
        phone = st.text_input("Phone")
        address = st.text_area("Address")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Back"):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.form_submit_button("Submit"):
                st.session_state.form_data.update({'phone': phone, 'address': address})
                st.success("Form submitted!")
        """, language="python")
    
    with st.expander("💡 5. Best Practices"):
        st.markdown("""
        **✅ DO:**
        - Always validate input before processing
        - Show clear error messages
        - Use form for grouped inputs (3+ fields)
        - Validate on both frontend and backend
        - Provide helpful placeholder text
        - Use appropriate input types (email, number, date)
        - Give immediate feedback on validation
        - Save form data in session state for multi-step
        
        **❌ DON'T:**
        - Validate after every keystroke (use forms!)
        - Show generic error messages ("Invalid input")
        - Mix form and non-form inputs confusingly
        - Forget to check for empty inputs
        - Allow form submission with invalid data
        - Lose user input on validation errors
        """)
    
    with st.expander("🔧 6. Advanced Patterns"):
        st.code("""
# Pattern 1: Conditional validation
if field_type == "email":
    validate_email(value)
elif field_type == "phone":
    validate_phone(value)

# Pattern 2: Cross-field validation
if start_date > end_date:
    st.error("Start date must be before end date")

# Pattern 3: Async validation (e.g., check if username exists)
@st.cache_data
def check_username_exists(username):
    # Check against database
    return username in existing_users

# Pattern 4: Form with file upload
with st.form("upload_form"):
    file = st.file_uploader("Upload")
    description = st.text_area("Description")
    
    if st.form_submit_button("Submit"):
        if file is None:
            st.error("Please upload a file")
        else:
            process_file(file)
        """, language="python")

# ============ TAB 2: SIMPLE FORMS ============
with tab2:
    st.header("📋 Simple Form Examples")
    
    # Example 1: Contact Form
    st.subheader("1️⃣ Contact Form")
    
    with st.form("contact_form", clear_on_submit=True):
        st.markdown("**Get in Touch**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*", placeholder="John Doe")
            email = st.text_input("Email*", placeholder="john@example.com")
        
        with col2:
            phone = st.text_input("Phone", placeholder="+1234567890")
            subject = st.selectbox("Subject", ["General", "Support", "Sales", "Other"])
        
        message = st.text_area("Message*", placeholder="Your message here...", height=100)
        
        submitted = st.form_submit_button("📧 Send Message", type="primary", use_container_width=True)
        
        if submitted:
            errors = []
            
            # Validation
            if not name:
                errors.append("Name is required")
            if not email:
                errors.append("Email is required")
            elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                errors.append("Invalid email format")
            if not message:
                errors.append("Message is required")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                st.success("✅ Message sent successfully!")
                st.balloons()
                
                # Store submission
                st.session_state.submitted_forms.append({
                    'type': 'contact',
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'subject': subject,
                    'message': message,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
    
    st.markdown("---")
    
    # Example 2: Registration Form
    st.subheader("2️⃣ User Registration")
    
    with st.form("registration_form"):
        st.markdown("**Create Account**")
        
        username = st.text_input("Username*", placeholder="Choose a username")
        
        col1, col2 = st.columns(2)
        
        with col1:
            password = st.text_input("Password*", type="password", placeholder="Min 8 characters")
        
        with col2:
            confirm_password = st.text_input("Confirm Password*", type="password")
        
        email = st.text_input("Email*", placeholder="your@email.com")
        
        col1, col2 = st.columns(2)
        
        with col1:
            birthdate = st.date_input("Date of Birth*", min_value=date(1900, 1, 1), max_value=date.today())
        
        with col2:
            country = st.selectbox("Country*", ["USA", "UK", "Canada", "India", "Other"])
        
        agree = st.checkbox("I agree to Terms & Conditions*")
        
        submitted = st.form_submit_button("📝 Register", type="primary", use_container_width=True)
        
        if submitted:
            errors = []
            
            # Validation
            if not username:
                errors.append("Username is required")
            elif len(username) < 3:
                errors.append("Username must be at least 3 characters")
            
            if not password:
                errors.append("Password is required")
            elif len(password) < 8:
                errors.append("Password must be at least 8 characters")
            elif not re.search(r'[A-Z]', password):
                errors.append("Password must contain uppercase letter")
            elif not re.search(r'[a-z]', password):
                errors.append("Password must contain lowercase letter")
            elif not re.search(r'\d', password):
                errors.append("Password must contain a number")
            
            if password != confirm_password:
                errors.append("Passwords don't match")
            
            if not email or '@' not in email:
                errors.append("Valid email is required")
            
            if not agree:
                errors.append("You must agree to Terms & Conditions")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                st.success(f"✅ Account created for {username}!")
                st.balloons()
                
                st.session_state.submitted_forms.append({
                    'type': 'registration',
                    'username': username,
                    'email': email,
                    'country': country,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
    
    st.markdown("---")
    
    # Show submitted forms
    if st.session_state.submitted_forms:
        with st.expander("📋 View Submitted Forms"):
            for idx, form in enumerate(st.session_state.submitted_forms):
                st.write(f"**{idx + 1}. {form['type'].title()} Form** - {form['timestamp']}")
                st.json(form)

# ============ TAB 3: VALIDATION EXAMPLES ============
with tab3:
    st.header("✅ Validation Patterns")
    
    # Email Validation
    st.subheader("1️⃣ Email Validation")
    
    with st.form("email_validation"):
        email_input = st.text_input("Enter Email", placeholder="test@example.com")
        
        if st.form_submit_button("Validate Email"):
            if not email_input:
                st.error("❌ Email is required")
            elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email_input):
                st.error("❌ Invalid email format")
            else:
                st.success(f"✅ Valid email: {email_input}")
    
    st.markdown("---")
    
    # Password Strength
    st.subheader("2️⃣ Password Strength")
    
    with st.form("password_validation"):
        password_input = st.text_input("Enter Password", type="password")
        
        if st.form_submit_button("Check Strength"):
            if not password_input:
                st.error("❌ Password is required")
            else:
                strength = 0
                feedback = []
                
                if len(password_input) >= 8:
                    strength += 1
                    feedback.append("✅ Length OK (8+ characters)")
                else:
                    feedback.append("❌ Too short (need 8+ characters)")
                
                if re.search(r'[A-Z]', password_input):
                    strength += 1
                    feedback.append("✅ Has uppercase letter")
                else:
                    feedback.append("❌ Needs uppercase letter")
                
                if re.search(r'[a-z]', password_input):
                    strength += 1
                    feedback.append("✅ Has lowercase letter")
                else:
                    feedback.append("❌ Needs lowercase letter")
                
                if re.search(r'\d', password_input):
                    strength += 1
                    feedback.append("✅ Has number")
                else:
                    feedback.append("❌ Needs number")
                
                if re.search(r'[!@#$%^&*(),.?":{}|<>]', password_input):
                    strength += 1
                    feedback.append("✅ Has special character")
                else:
                    feedback.append("⚠️ Consider adding special character")
                
                # Show strength
                if strength <= 2:
                    st.error(f"🔴 Weak Password (Score: {strength}/5)")
                elif strength <= 3:
                    st.warning(f"🟡 Medium Password (Score: {strength}/5)")
                else:
                    st.success(f"🟢 Strong Password (Score: {strength}/5)")
                
                # Show feedback
                for item in feedback:
                    st.write(item)
    
    st.markdown("---")
    
    # Phone Number Validation
    st.subheader("3️⃣ Phone Number Validation")
    
    with st.form("phone_validation"):
        phone_input = st.text_input("Enter Phone", placeholder="+1234567890 or 1234567890")
        
        if st.form_submit_button("Validate Phone"):
            if not phone_input:
                st.error("❌ Phone number is required")
            else:
                # Remove spaces and dashes
                clean_phone = re.sub(r'[\s\-\(\)]', '', phone_input)
                
                if re.match(r'^\+?1?\d{10,15}$', clean_phone):
                    st.success(f"✅ Valid phone: {clean_phone}")
                else:
                    st.error("❌ Invalid phone format (10-15 digits, optional +)")
    
    st.markdown("---")
    
    # Date Range Validation
    st.subheader("4️⃣ Date Range Validation")
    
    with st.form("date_validation"):
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", value=date.today())
        
        with col2:
            end_date = st.date_input("End Date", value=date.today())
        
        if st.form_submit_button("Validate Dates"):
            if start_date > end_date:
                st.error("❌ Start date must be before or equal to end date")
            elif start_date == end_date:
                st.warning("⚠️ Start and end dates are the same")
            else:
                days = (end_date - start_date).days
                st.success(f"✅ Valid range: {days} days")
    
    st.markdown("---")
    
    # Number Range Validation
    st.subheader("5️⃣ Number Range Validation")
    
    with st.form("number_validation"):
        age_input = st.number_input("Enter Age", min_value=0, max_value=150, value=25)
        
        if st.form_submit_button("Validate Age"):
            if age_input < 18:
                st.error("❌ Must be 18 or older")
            elif age_input > 100:
                st.warning("⚠️ Age seems unusually high")
            else:
                st.success(f"✅ Valid age: {age_input}")

# ============ TAB 4: MULTI-STEP FORM ============
with tab4:
    st.header("🪜 Multi-Step Form Wizard")
    
    # Progress indicator
    progress = st.session_state.form_step / 4
    st.progress(progress)
    st.write(f"**Step {st.session_state.form_step} of 4**")
    
    st.markdown("---")
    
    # Step 1: Personal Info
    if st.session_state.form_step == 1:
        st.subheader("📝 Step 1: Personal Information")
        
        with st.form("step1_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name*", value=st.session_state.form_data.get('first_name', ''))
                email = st.text_input("Email*", value=st.session_state.form_data.get('email', ''))
            
            with col2:
                last_name = st.text_input("Last Name*", value=st.session_state.form_data.get('last_name', ''))
                phone = st.text_input("Phone*", value=st.session_state.form_data.get('phone', ''))
            
            birthdate = st.date_input(
                "Date of Birth*",
                value=st.session_state.form_data.get('birthdate', date(2000, 1, 1)),
                min_value=date(1900, 1, 1),
                max_value=date.today()
            )
            
            col1, col2 = st.columns([3, 1])
            
            with col2:
                if st.form_submit_button("Next →", type="primary", use_container_width=True):
                    errors = []
                    
                    if not first_name:
                        errors.append("First name is required")
                    if not last_name:
                        errors.append("Last name is required")
                    if not email or '@' not in email:
                        errors.append("Valid email is required")
                    if not phone:
                        errors.append("Phone is required")
                    
                    if errors:
                        for error in errors:
                            st.error(f"❌ {error}")
                    else:
                        st.session_state.form_data.update({
                            'first_name': first_name,
                            'last_name': last_name,
                            'email': email,
                            'phone': phone,
                            'birthdate': birthdate
                        })
                        st.session_state.form_step = 2
                        st.rerun()
    
    # Step 2: Address
    elif st.session_state.form_step == 2:
        st.subheader("🏠 Step 2: Address")
        
        with st.form("step2_form"):
            street = st.text_input("Street Address*", value=st.session_state.form_data.get('street', ''))
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                city = st.text_input("City*", value=st.session_state.form_data.get('city', ''))
            
            with col2:
                state = st.text_input("State*", value=st.session_state.form_data.get('state', ''))
            
            with col3:
                zipcode = st.text_input("ZIP Code*", value=st.session_state.form_data.get('zipcode', ''))
            
            country = st.selectbox(
                "Country*",
                ["USA", "UK", "Canada", "India", "Other"],
                index=["USA", "UK", "Canada", "India", "Other"].index(st.session_state.form_data.get('country', 'USA'))
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("← Back", use_container_width=True):
                    st.session_state.form_step = 1
                    st.rerun()
            
            with col2:
                if st.form_submit_button("Next →", type="primary", use_container_width=True):
                    errors = []
                    
                    if not street:
                        errors.append("Street address is required")
                    if not city:
                        errors.append("City is required")
                    if not state:
                        errors.append("State is required")
                    if not zipcode:
                        errors.append("ZIP code is required")
                    
                    if errors:
                        for error in errors:
                            st.error(f"❌ {error}")
                    else:
                        st.session_state.form_data.update({
                            'street': street,
                            'city': city,
                            'state': state,
                            'zipcode': zipcode,
                            'country': country
                        })
                        st.session_state.form_step = 3
                        st.rerun()
    
    # Step 3: Account
    elif st.session_state.form_step == 3:
        st.subheader("🔐 Step 3: Account Setup")
        
        with st.form("step3_form"):
            username = st.text_input("Username*", value=st.session_state.form_data.get('username', ''))
            
            col1, col2 = st.columns(2)
            
            with col1:
                password = st.text_input("Password*", type="password")
            
            with col2:
                confirm_password = st.text_input("Confirm Password*", type="password")
            
            security_question = st.selectbox(
                "Security Question*",
                ["What was your first pet's name?", "What city were you born in?", "What's your favorite food?"]
            )
            
            security_answer = st.text_input("Security Answer*", value=st.session_state.form_data.get('security_answer', ''))
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("← Back", use_container_width=True):
                    st.session_state.form_step = 2
                    st.rerun()
            
            with col2:
                if st.form_submit_button("Next →", type="primary", use_container_width=True):
                    errors = []
                    
                    if not username:
                        errors.append("Username is required")
                    elif len(username) < 3:
                        errors.append("Username must be at least 3 characters")
                    
                    if not password:
                        errors.append("Password is required")
                    elif len(password) < 8:
                        errors.append("Password must be at least 8 characters")
                    
                    if password != confirm_password:
                        errors.append("Passwords don't match")
                    
                    if not security_answer:
                        errors.append("Security answer is required")
                    
                    if errors:
                        for error in errors:
                            st.error(f"❌ {error}")
                    else:
                        st.session_state.form_data.update({
                            'username': username,
                            'password': '***hidden***',
                            'security_question': security_question,
                            'security_answer': security_answer
                        })
                        st.session_state.form_step = 4
                        st.rerun()
    
    # Step 4: Review & Submit
    elif st.session_state.form_step == 4:
        st.subheader("✅ Step 4: Review & Submit")
        
        st.write("**Please review your information:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Personal Information")
            st.write(f"**Name:** {st.session_state.form_data.get('first_name')} {st.session_state.form_data.get('last_name')}")
            st.write(f"**Email:** {st.session_state.form_data.get('email')}")
            st.write(f"**Phone:** {st.session_state.form_data.get('phone')}")
            st.write(f"**Birth Date:** {st.session_state.form_data.get('birthdate')}")
            
            st.markdown("### Account")
            st.write(f"**Username:** {st.session_state.form_data.get('username')}")
            st.write(f"**Security Q:** {st.session_state.form_data.get('security_question')}")
        
        with col2:
            st.markdown("### Address")
            st.write(f"**Street:** {st.session_state.form_data.get('street')}")
            st.write(f"**City:** {st.session_state.form_data.get('city')}")
            st.write(f"**State:** {st.session_state.form_data.get('state')}")
            st.write(f"**ZIP:** {st.session_state.form_data.get('zipcode')}")
            st.write(f"**Country:** {st.session_state.form_data.get('country')}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("← Back to Edit", use_container_width=True):
                st.session_state.form_step = 3
                st.rerun()
        
        with col2:
            if st.button("✅ Submit Application", type="primary", use_container_width=True):
                st.success("🎉 Application submitted successfully!")
                st.balloons()
                
                # Store submission
                st.session_state.submitted_forms.append({
                    'type': 'multi-step-application',
                    'data': st.session_state.form_data.copy(),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
                # Reset
                st.session_state.form_step = 1
                st.session_state.form_data = {}
                
                st.write("**Your application has been submitted!**")

# ============ TAB 5: QUIZ ============
with tab5:
    st.header("🧪 Knowledge Check")
    
    q1 = st.radio(
        "Q1: What's the main benefit of using st.form()?",
        [
            "Makes UI look better",
            "Batches inputs, reduces reruns",
            "Validates automatically"
        ]
    )
    
    q2 = st.radio(
        "Q2: What's required in every form?",
        ["A title", "A submit button", "At least 3 inputs"]
    )
    
    q3 = st.checkbox("Q3: You should validate input on both frontend and backend")
    
    q4 = st.radio(
        "Q4: How to preserve data across multi-step forms?",
        [
            "Store in st.session_state",
            "Use global variables",
            "Write to file"
        ]
    )
    
    q5 = st.radio(
        "Q5: What's a good email validation regex pattern?",
        [
            r".*@.*",
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            r"^.*@.*\..*$"
        ]
    )
    
    if st.button("✅ Check Answers", type="primary"):
        score = 0
        feedback = []
        
        if q1 == "Batches inputs, reduces reruns":
            score += 1
            feedback.append("✅ Q1: Correct! Forms batch inputs")
        else:
            feedback.append("❌ Q1: Forms reduce reruns by batching")
        
        if q2 == "A submit button":
            score += 1
            feedback.append("✅ Q2: Correct!")
        else:
            feedback.append("❌ Q2: Every form needs a submit button")
        
        if q3:
            score += 1
            feedback.append("✅ Q3: Correct! Always validate both sides")
        else:
            feedback.append("❌ Q3: Validate frontend AND backend")
        
        if q4 == "Store in st.session_state":
            score += 1
            feedback.append("✅ Q4: Correct!")
        else:
            feedback.append("❌ Q4: Use st.session_state for multi-step")
        
        if q5 == r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$":
            score += 1
            feedback.append("✅ Q5: Correct! Comprehensive regex")
        else:
            feedback.append("❌ Q5: Use comprehensive email regex")
        
        st.markdown("---")
        st.write(f"### 🎯 Score: {score}/5")
        
        for fb in feedback:
            st.write(fb)
        
        if score == 5:
            st.success("🎉 Perfect! You mastered forms!")
            st.balloons()
        elif score >= 3:
            st.info("👍 Good! Review validation patterns.")
        else:
            st.warning("📖 Please review forms & validation.")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 9 - Access Control")
with col2:
    st.info("➡️ **Next:** Chapter 11 - Caching & Performance")