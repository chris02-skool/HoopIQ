# The authentication UI for the app

import streamlit as st
from auth_utils import login, register
import re

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
    # Logged-in state: show sidebar and logout
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
        st.info("💡 Tip: You may need to press the button twice to continue (Streamlit quirk).")

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
        st.info("💡 Tip: You may need to press the button twice to continue (Streamlit quirk).")
        st.info("Password must be at least 8 characters long, with at least 1 uppercase, 1 lowercase, and 1 number.")

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

        # Password validation function
        def is_valid_password(pwd):
            if len(pwd) < 8:
                return False
            if not re.search(r"[A-Z]", pwd):
                return False
            if not re.search(r"[a-z]", pwd):
                return False
            if not re.search(r"[0-9]", pwd):
                return False
            return True

        if confirm_clicked:
            username = st.session_state.register_username.strip()
            password = st.session_state.register_password.strip()
            if username == "" or password == "":
                st.session_state.message = "Username and password cannot be empty."
            elif not is_valid_password(password):
                st.session_state.message = "Password does not meet requirements."
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

    # -----------------------------
    # Show message if exists
    # -----------------------------
    if st.session_state.message:
        st.warning(st.session_state.message)

    return st.session_state.logged_in
