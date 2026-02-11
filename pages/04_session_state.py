# # ❌ THIS DOESN'T WORK!
# count = 0  # This resets to 0 on EVERY rerun!

# if st.button("Increment"):
#     count += 1  # Increments to 1
    
# st.write(f"Count: {count}")  # Always shows 0!

# # Why? Because the script reruns from top to bottom
# # and count gets reset to 0 every time!

# Session state persists across reruns!
import streamlit as st

st.set_page_config(
    page_title="Chapter 4: Session State",
    page_icon="💾",
    layout="wide"
)

st.title("💾 Chapter 4: Session State (Most Important!)")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📖 Learn",
    "🛒 Shopping Cart Demo",
    "🎮 Interactive Examples",
    "🧪 Quiz"
])

# ============ TAB 1: LEARN ============
with tab1:
    st.header("Understanding Session State")
    
    with st.expander("🔥 The Problem", expanded=True):
        st.markdown("""
        **Streamlit reruns your entire script on every interaction!**
        
        This means normal variables reset every time:
        """)
        
        st.code("""
# ❌ THIS DOESN'T WORK
count = 0  # Resets to 0 every rerun!

if st.button("Increment"):
    count += 1
    
st.write(count)  # Always shows 0!
        """, language="python")
        
        st.error("Variables don't persist between reruns!")
    
    with st.expander("✅ The Solution: Session State"):
        st.markdown("""
        **Session state persists data across reruns!**
        """)
        
        st.code("""
# ✅ THIS WORKS!
if 'count' not in st.session_state:
    st.session_state.count = 0

if st.button("Increment"):
    st.session_state.count += 1
    
st.write(st.session_state.count)  # Persists!
        """, language="python")
        
        st.success("Session state keeps data alive between reruns!")
    
    with st.expander("🎯 Basic Usage"):
        st.code("""
# Initialize
if 'key' not in st.session_state:
    st.session_state.key = 'value'

# Read
value = st.session_state.key

# Update
st.session_state.key = 'new_value'

# Check existence
if 'key' in st.session_state:
    # Key exists
    
# Delete
del st.session_state.key
        """, language="python")
    
    with st.expander("🔔 Callbacks"):
        st.markdown("""
        **Callbacks run BEFORE the page reruns!**
        
        Perfect for updating state in response to user actions.
        """)
        
        st.code("""
# Define callback
def increment():
    st.session_state.count += 1

# Use with button
st.button("Click", on_click=increment)

# With arguments
def add_amount(amount):
    st.session_state.total += amount
    
st.button("Add 10", on_click=add_amount, args=(10,))
        """, language="python")
    
    with st.expander("📝 Widget Keys"):
        st.code("""
# Widgets automatically use session state with 'key'
name = st.text_input("Name", key="user_name")

# This automatically does:
# st.session_state.user_name = <user input>

# Access it anywhere
st.write(st.session_state.user_name)
        """, language="python")

# ============ TAB 2: SHOPPING CART DEMO ============
with tab2:
    st.header("🛒 Shopping Cart Demo")
    
    # Initialize cart
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    
    # Product catalog
    products = {
        'Laptop': {'price': 999, 'emoji': '💻'},
        'Mouse': {'price': 25, 'emoji': '🖱️'},
        'Keyboard': {'price': 75, 'emoji': '⌨️'},
        'Monitor': {'price': 299, 'emoji': '🖥️'},
        'Headphones': {'price': 149, 'emoji': '🎧'}
    }
    
    # Product display
    st.subheader("📦 Products")
    
    cols = st.columns(5)
    
    for idx, (product, details) in enumerate(products.items()):
        with cols[idx]:
            st.markdown(f"### {details['emoji']}")
            st.write(f"**{product}**")
            st.write(f"${details['price']}")
            
            # Add to cart callback
            def add_to_cart(prod, price):
                st.session_state.cart.append({
                    'product': prod,
                    'price': price
                })
            
            if st.button(
                "Add to Cart",
                key=f"add_{product}",
                on_click=add_to_cart,
                args=(product, details['price'])
            ):
                pass  # Callback handles it
    
    st.markdown("---")
    
    # Cart display
    st.subheader("🛒 Your Cart")
    
    if len(st.session_state.cart) == 0:
        st.info("Cart is empty. Add some products!")
    else:
        # Display cart items
        for idx, item in enumerate(st.session_state.cart):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                emoji = products[item['product']]['emoji']
                st.write(f"{emoji} {item['product']}")
            with col2:
                st.write(f"${item['price']}")
            with col3:
                # Remove callback
                def remove_item(index):
                    st.session_state.cart.pop(index)
                
                if st.button("🗑️", key=f"remove_{idx}"):
                    remove_item(idx)
                    st.rerun()
        
        # Total
        total = sum(item['price'] for item in st.session_state.cart)
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Items", len(st.session_state.cart))
        with col2:
            st.metric("Total Price", f"${total}")
        
        # Checkout
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear Cart", type="secondary", use_container_width=True):
                st.session_state.cart = []
                st.rerun()
        
        with col2:
            if st.button("💳 Checkout", type="primary", use_container_width=True):
                st.success(f"Order placed! Total: ${total}")
                st.balloons()
                st.session_state.cart = []
                st.rerun()

# ============ TAB 3: INTERACTIVE EXAMPLES ============
with tab3:
    st.header("🎮 Interactive Examples")
    
    # Example 1: Counter
    st.subheader("1️⃣ Simple Counter")
    
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    def increment():
        st.session_state.counter += 1
    
    def decrement():
        st.session_state.counter -= 1
    
    def reset():
        st.session_state.counter = 0
    
    with col1:
        st.button("➕ Add", on_click=increment, use_container_width=True)
    with col2:
        st.button("➖ Subtract", on_click=decrement, use_container_width=True)
    with col3:
        st.button("🔄 Reset", on_click=reset, use_container_width=True)
    with col4:
        st.metric("Count", st.session_state.counter)
    
    st.markdown("---")
    
    # Example 2: Todo List
    st.subheader("2️⃣ Todo List")

    if 'todos' not in st.session_state:
        st.session_state.todos = []

    col1, col2 = st.columns([4, 1])

    with col1:
        new_todo = st.text_input("Add a task", key="new_todo_input")
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if st.button("➕ Add Task"):
            if new_todo:
                st.session_state.todos.append({
                    'task': new_todo,
                    'done': False
                })
                st.rerun()

    # Display todos
    if st.session_state.todos:
        for idx, todo in enumerate(st.session_state.todos):
            col1, col2, col3 = st.columns([1, 5, 1])
            
            with col1:
                # ✅ FIXED: Added proper label with label_visibility
                if st.checkbox(
                    "Complete", 
                    value=todo['done'], 
                    key=f"todo_check_{idx}",
                    label_visibility="collapsed"  # Hides the label but keeps it for accessibility
                ):
                    st.session_state.todos[idx]['done'] = True
                else:
                    st.session_state.todos[idx]['done'] = False
            
            with col2:
                if todo['done']:
                    st.markdown(f"~~{todo['task']}~~")
                else:
                    st.write(todo['task'])
            
            with col3:
                if st.button("🗑️", key=f"todo_del_{idx}"):
                    st.session_state.todos.pop(idx)
                    st.rerun()
        
        if st.button("Clear Completed"):
            st.session_state.todos = [t for t in st.session_state.todos if not t['done']]
            st.rerun()
    else:
        st.info("No tasks yet. Add one above!")
    
    st.markdown("---")
    
    # Example 3: Form with Validation
    st.subheader("3️⃣ Form with State")
    
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    
    with st.form("user_form"):
        st.write("**User Registration**")
        
        name = st.text_input("Name*")
        email = st.text_input("Email*")
        age = st.number_input("Age", 18, 100, 25)
        
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            errors = []
            
            if not name:
                errors.append("Name is required")
            if not email or '@' not in email:
                errors.append("Valid email is required")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                st.session_state.form_data = {
                    'name': name,
                    'email': email,
                    'age': age
                }
                st.session_state.form_submitted = True
                st.success("Form submitted!")
    
    # Display submitted data
    if st.session_state.form_submitted and 'form_data' in st.session_state:
        st.subheader("✅ Submitted Data")
        st.json(st.session_state.form_data)
        
        if st.button("Edit Form"):
            st.session_state.form_submitted = False
            st.rerun()

# ============ TAB 4: QUIZ ============
with tab4:
    st.header("🧪 Knowledge Check")
    
    q1 = st.radio(
        "Q1: Why do we need session state?",
        [
            "To make the app look better",
            "Because variables reset on every rerun",
            "To connect to databases"
        ]
    )
    
    q2 = st.radio(
        "Q2: How to check if a key exists?",
        [
            "st.session_state.has('key')",
            "'key' in st.session_state",
            "st.session_state.exists('key')"
        ]
    )
    
    q3 = st.radio(
        "Q3: When do callbacks execute?",
        [
            "After the page reruns",
            "Before the page reruns",
            "During the rerun"
        ]
    )
    
    q4 = st.checkbox("Q4: Session state is shared across pages")
    
    q5 = st.radio(
        "Q5: How to initialize session state?",
        [
            "st.session_state.init('key', value)",
            "if 'key' not in st.session_state: st.session_state.key = value",
            "st.session_state.set('key', value)"
        ]
    )
    
    if st.button("Check Answers", type="primary"):
        score = 0
        
        if q1 == "Because variables reset on every rerun":
            score += 1
        if q2 == "'key' in st.session_state":
            score += 1
        if q3 == "Before the page reruns":
            score += 1
        if q4:  # True
            score += 1
        if q5 == "if 'key' not in st.session_state: st.session_state.key = value":
            score += 1
        
        st.write(f"### Score: {score}/5")
        
        if score == 5:
            st.success("🎉 Perfect! You mastered session state!")
            st.balloons()
        elif score >= 3:
            st.info("👍 Good! Review callbacks and initialization.")
        else:
            st.warning("📖 Session state is critical - please review!")

# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.info("⬅️ **Previous:** Chapter 3 - Data Handling")
with col2:
    st.info("➡️ **Next:** Chapter 5 - Data Visualization")