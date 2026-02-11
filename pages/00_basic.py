from datetime import date, time
import streamlit as st

# Text Hierarchy
st.title("🎯 Main Title")
st.header("Section Header")
st.subheader("Subsection")
st.text("Plain text")
st.markdown("**Bold** *italic* `code`")
st.caption("Small caption")

# Special Text
st.code("print('hello')", language="python")
st.latex(r"e^{i\pi} + 1 = 0")

# Status Messages
st.success("✅ Success!")
st.info("ℹ️ Information")
st.warning("⚠️ Warning")
st.error("❌ Error")

# Visual Elements
st.divider()  # Horizontal line
# st.balloons()  # Celebration animation (try it!)
# st.snow()      # Snow animation



st.header("📝 Input Widgets")

# Text Inputs
name = st.text_input("Name", placeholder="Enter name")
bio = st.text_area("Bio", height=100)
password = st.text_input("Password", type="password")

# Numeric Inputs
age = st.number_input("Age", min_value=0, max_value=120, value=25)
salary = st.slider("Salary (K)", 0, 200, 50)

# Selection
gender = st.radio("Gender", ["Male", "Female", "Other"])
role = st.selectbox("Role", ["Developer", "Designer", "Manager"])
skills = st.multiselect("Skills", ["Python", "Java", "JS", "Go"])

# Boolean
newsletter = st.checkbox("Subscribe to newsletter")
terms = st.toggle("Accept terms")  # Modern switch

# Date/Time
birthday = st.date_input("Birthday", value=date(2000, 1, 1))
meeting = st.time_input("Meeting time", value=time(9, 0))

# File & Color
uploaded_file = st.file_uploader("Upload file")
color = st.color_picker("Pick color", "#00f900")

# Buttons
if st.button("Submit", type="primary"):
    st.success("Form submitted!")


st.markdown("---")
st.subheader("🔗 Multi-Page Demo (From Chapter 6)")

st.info("""
This section shows **shared state** from Chapter 6.
Go to Chapter 6, set values, then come back here to see them!
""")

# Show shared counter
if 'shared_counter' in st.session_state:
    st.metric("Shared Counter (from Ch 6)", st.session_state.shared_counter)
else:
    st.warning("No counter set. Go to Chapter 6 to set it!")

# Show shared message
if 'shared_message' in st.session_state and st.session_state.shared_message:
    st.success(f"📝 **Shared Message:** {st.session_state.shared_message}")
else:
    st.info("No message set. Go to Chapter 6 to set a message!")

# Show shared dataframe
if 'shared_dataframe' in st.session_state and st.session_state.shared_dataframe is not None:
    df = st.session_state.shared_dataframe
    st.success(f"📊 **Shared Data:** {len(df)} rows (from Chapter 6)")
    
    with st.expander("View Shared Data"):
        st.dataframe(df, width=None)
else:
    st.info("No data set. Go to Chapter 6 to generate data!")

# Quick navigation
if st.button("👉 Go to Chapter 6", type="secondary"):
    st.switch_page("pages/06_multipage.py")