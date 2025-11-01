import streamlit as st
from services.check_login import check_login

def login_page():
    st.title("💗 Welcome to FluffyTail 💗")
    st.markdown("Please login:")

    role = st.selectbox("Select Role", ["Customer", "Staff"])
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.warning("⚠️ Username and password cannot be empty")
            return None

        user_id = check_login(username, password, role)
        if user_id:
            st.success(f"✅ Login successful! Welcome {username}")
            return {
                'id': user_id,
                'username': username,
                'role': role.lower()
            }
        else:
            st.error("❌ Login failed, please check credentials.")
            return None