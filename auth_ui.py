# The authentication UI for the app

# auth_ui.py
import streamlit as st
from auth_utils import login, register

def auth_ui():
    """
    Handles login, registration, and logout.
    Returns True if the user is logged in, False otherwise.
    """
    # Initialize session state variables
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "screen" not in st.session_state:
        st.session_state.screen = "login"
    if "login_username" not in st.session_state:
        st.session_state.login_username = ""
    if "login_password" not in st.session_state:
        st.session_state.login_password = ""
    if "register_username" not in st.session_state:
        st.session_state.register_username = ""
    if "register_password" not in st.session_state:
        st.session_state.register_password = ""
    if "message" not in st.session_state:
        st.session_state.message = ""

    # -----------------------------
    # Logout
    # -----------------------------
    if st.session_state.logged_in:
        st.sidebar.success(f"Logged in as {st.session_state.username}")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.screen = "login"
            st.session_state.message = ""
        return True

    # -----------------------------
    # Login Screen
    # -----------------------------
    if st.session_state.screen == "login":
        st.subheader("Login")
        st.write("Enter your username and password. If you don't have an account, click Register.")
        
        st.session_state.login_username = st.text_input("Username", value=st.session_state.login_username)
        st.session_state.login_password = st.text_input("Password", type="password", value=st.session_state.login_password)

        col1, col2 = st.columns(2)
        with col1:
            login_clicked = st.button("Login")
        with col2:
            register_clicked = st.button("Register")

        if login_clicked:
            username = st.session_state.login_username.strip()
            password = st.session_state.login_password.strip()
            if username == "" or password == "":
                st.session_state.message = "Username and password cannot be empty."
            elif login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.login_username = ""
                st.session_state.login_password = ""
                st.session_state.message = ""
            else:
                st.session_state.login_username = ""
                st.session_state.login_password = ""
                st.session_state.message = "Incorrect username or password."

        if register_clicked:
            st.session_state.screen = "register"
            st.session_state.message = ""

    # -----------------------------
    # Register Screen
    # -----------------------------
    elif st.session_state.screen == "register":
        st.subheader("Register")
        st.write("Create a new account.")

        st.session_state.register_username = st.text_input("Desired Username", value=st.session_state.register_username)
        st.session_state.register_password = st.text_input("Desired Password", type="password", value=st.session_state.register_password)

        col1, col2 = st.columns(2)
        with col1:
            confirm_clicked = st.button("Confirm Registration")
        with col2:
            back_clicked = st.button("Back to Login")

        if confirm_clicked:
            username = st.session_state.register_username.strip()
            password = st.session_state.register_password.strip()
            if username == "" or password == "":
                st.session_state.message = "Username and password cannot be empty."
            elif register(username, password):
                st.session_state.screen = "login"
                st.session_state.register_username = ""
                st.session_state.register_password = ""
                st.session_state.message = "Registration successful! Please login."
            else:
                st.session_state.message = "Username already exists. Choose another."

        if back_clicked:
            st.session_state.screen = "login"
            st.session_state.message = ""

    # Show message if exists
    if st.session_state.message:
        st.warning(st.session_state.message)

    # Return login status
    return st.session_state.logged_in
