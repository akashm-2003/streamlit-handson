import streamlit as st
from datetime import date

st.set_page_config(page_title="Chapter 1", page_icon="📚", layout="wide")

st.title("📚 Chapter 1: Fundamentals")
st.markdown("---")

# Tabs for organization
tab1, tab2, tab3 = st.tabs(["📖 Learn", "🎮 Practice", "🧪 Quiz"])

with tab1:
    st.header("Core Concepts")
    
    st.subheader("1. Execution Model")
    st.info("""
    **Key Concept:** Streamlit reruns your entire script on every interaction!
    - No event handlers needed
    - Widget values persist automatically
    - State management via session_state (Chapter 4)
    """)
    
    st.subheader("2. Basic Syntax")
    st.code("""
# Display
st.write("Anything")
st.title("Big Text")

# Input
value = st.text_input("Label")
number = st.slider("Pick", 0, 100)

# Button
if st.button("Click"):
    st.write("Clicked!")
    """, language="python")

with tab2:
    st.header("🎮 Interactive Demo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Your Profile")
        name = st.text_input("Full Name", key="profile_name")
        age = st.number_input("Age", 18, 100, 25)
        country = st.selectbox("Country", ["USA", "UK", "India", "Canada"])
        hobbies = st.multiselect(
            "Hobbies",
            ["Reading", "Gaming", "Sports", "Music", "Coding"]
        )
        birthday = st.date_input("Birthday", value=date(2000, 1, 1))
    
    with col2:
        st.subheader("Preview")
        if name:
            st.markdown(f"""
            ### {name}
            - **Age:** {age}
            - **Country:** {country}
            - **Birthday:** {birthday}
            - **Hobbies:** {', '.join(hobbies) if hobbies else 'None'}
            """)
        else:
            st.info("👈 Fill the form to see preview")
    
    if st.button("💾 Save Profile", type="primary"):
        if name:
            st.success(f"✅ Profile saved for {name}!")
            st.balloons()
        else:
            st.error("❌ Please enter your name!")

with tab3:
    st.header("🧪 Quick Quiz")
    
    q1 = st.radio(
        "Q1: When does Streamlit rerun your script?",
        ["Only on page load", "On every interaction", "Only when you refresh"]
    )
    
    q2 = st.radio(
        "Q2: Which method displays the biggest text?",
        ["st.write()", "st.title()", "st.header()"]
    )
    
    q3 = st.checkbox("Q3: Widget values persist between reruns automatically")
    
    if st.button("Submit Quiz"):
        score = 0
        if q1 == "On every interaction":
            score += 1
        if q2 == "st.title()":
            score += 1
        if q3:
            score += 1
        
        st.write(f"Score: {score}/3")
        if score == 3:
            st.success("🎉 Perfect! You understand the basics!")
            st.balloons()
        elif score >= 2:
            st.info("👍 Good! Review the concepts once more.")
        else:
            st.warning("📖 Please review the concepts again.")

# Navigation hint
st.markdown("---")
st.info("💡 **Next:** Chapter 2 - Layouts & Organization")