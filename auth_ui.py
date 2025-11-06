# The authentication UI for the app

import streamlit as st
from auth_utils import login, register, delete_user, change_password
import re

def validate_password(password):
    """Check if password meets requirements."""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True

def auth_ui():
    """
    Handles login, registration, and logout.
    Returns True if the user is logged in, False otherwise.
    """
    # -----------------------------
    # Initialize session state variables
    # -----------------------------
    defaults = {
        "logged_in": False,
        "username": "",
        "screen": "login",
        "login_username": "",
        "login_password": "",
        "register_username": "",
        "register_password": "",
        "message": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # -----------------------------
    # Logged-in state: show sidebar, change password, delete account, and logout
    # -----------------------------
    if st.session_state.logged_in:
        st.sidebar.success(f"Logged in as {st.session_state.username}")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.screen = "login"
            st.session_state.message = ""
    
        # Change Password
        pw_expander = st.sidebar.expander("Change Password")
        with pw_expander:
            st.info("Note: You may need to click 'Update Password' twice for Streamlit to process it.")
            new_pw = st.text_input("New Password", type="password")
            confirm_pw = st.text_input("Confirm New Password", type="password")
            if st.sidebar.button("Update Password"):
                if new_pw != confirm_pw:
                    st.warning("⚠️ Passwords do not match.")
                elif not validate_password(new_pw):
                    st.warning("⚠️ Password does not meet requirements.")
                else:
                    if change_password(st.session_state.username, new_pw):
                        st.success("✅ Password updated successfully.")
                    else:
                        st.error("❌ Could not update password.")
    
        # Delete Account
        delete_expander = st.sidebar.expander("Delete Account")
        with delete_expander:
            st.warning("⚠️ Deleting your account is permanent!")
            st.info("Note: You may need to click the button twice for Streamlit to update.")
            confirm_delete = st.checkbox("I understand and want to delete my account")
            if st.sidebar.button("Delete Account Permanently"):
                if confirm_delete:
                    if delete_user(st.session_state.username):
                        st.success("✅ Account deleted successfully.")
                        st.session_state.logged_in = False
                        st.session_state.username = ""
                        st.session_state.screen = "login"
                        st.session_state.message = ""
                    else:
                        st.error("❌ Could not delete account.")
                else:
                    st.info("Please confirm deletion by checking the box.")
    
        return True

    # -----------------------------
    # Login Screen
    # -----------------------------
    if st.session_state.screen == "login":
        st.subheader("Login")
        st.write("Enter your username and password. If you don't have an account, click Register.")
        st.write("**Note:** You may need to double-click buttons due to Streamlit behavior.")

        st.session_state.login_username = st.text_input(
            "Username", value=st.session_state.login_username
        )
        st.session_state.login_password = st.text_input(
            "Password", type="password", value=st.session_state.login_password
        )

        col1, col2 = st.columns(2)
        with col1:
            login_clicked = st.button("Login")
        with col2:
            register_clicked = st.button("Register")

        if login_clicked:
            username = st.session_state.login_username.strip()
            password = st.session_state.login_password.strip()
            if username == "" or password == "":
                st.warning("⚠️ Username and password cannot be empty.")
            elif login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.login_username = ""
                st.session_state.login_password = ""
                st.success(f"✅ Logged in as {username}")
            else:
                st.session_state.login_username = ""
                st.session_state.login_password = ""
                st.error("❌ Incorrect username or password.")

        if register_clicked:
            st.session_state.screen = "register"
            st.session_state.message = ""

    # -----------------------------
    # Register Screen
    # -----------------------------
    elif st.session_state.screen == "register":
        st.subheader("Register")
        st.write(
            "Create a new account. Password must be at least 8 characters long, "
            "contain at least 1 uppercase, 1 lowercase, and 1 number."
        )
        st.write("**Note:** You may need to double-click buttons due to Streamlit behavior.")

        st.session_state.register_username = st.text_input(
            "Desired Username", value=st.session_state.register_username
        )
        st.session_state.register_password = st.text_input(
            "Desired Password", type="password", value=st.session_state.register_password
        )

        col1, col2 = st.columns(2)
        with col1:
            confirm_clicked = st.button("Confirm Registration")
        with col2:
            back_clicked = st.button("Back to Login")

        if confirm_clicked:
            username = st.session_state.register_username.strip()
            password = st.session_state.register_password.strip()
            if username == "" or password == "":
                st.warning("⚠️ Username and password cannot be empty.")
            elif not validate_password(password):
                st.warning("⚠️ Password does not meet requirements.")
            elif register(username, password):
                st.success("✅ Registration successful! Please login.")
                st.session_state.screen = "login"
                st.session_state.register_username = ""
                st.session_state.register_password = ""
            else:
                st.error("❌ Username already exists. Choose another.")

        if back_clicked:
            st.session_state.screen = "login"
            st.session_state.message = ""

    return st.session_state.logged_in
