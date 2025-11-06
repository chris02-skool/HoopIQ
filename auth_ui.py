# The authentication UI for the app

import streamlit as st
from auth_utils import login, register

def auth_ui():
    """
    Handles login, registration, logout.
    Returns True if logged in, False otherwise.
    """
    # -----------------------------
    # Initialize session state
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
    # Logged-in state: sidebar
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
        st.write("Double-click buttons to proceed due to Streamlit behavior.")
        st.write("Enter your username and password. If you don't have an account, click Register.")

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
                st.warning("Username and password cannot be empty.")
            else:
                success, message = login(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.login_username = ""
                    st.session_state.login_password = ""
                    st.success(f"Logged in as {username}")
                else:
                    st.session_state.login_username = ""
                    st.session_state.login_password = ""
                    st.error(message)

        if register_clicked:
            st.session_state.screen = "register"
            st.session_state.message = ""

    # -----------------------------
    # Register Screen
    # -----------------------------
    elif st.session_state.screen == "register":
        st.subheader("Register")
        st.write("Double-click buttons to proceed due to Streamlit behavior.")
        st.write("Create a new account.")

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
                st.warning("Username and password cannot be empty.")
            else:
                success, message = register(username, password)
                if success:
                    st.success(message)
                    st.session_state.screen = "login"
                    st.session_state.register_username = ""
                    st.session_state.register_password = ""
                else:
                    st.error(message)

        if back_clicked:
            st.session_state.screen = "login"
            st.session_state.message = ""

    return st.session_state.logged_in
