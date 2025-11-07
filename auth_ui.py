# auth_ui.py
import streamlit as st
from auth_utils import login, register, delete_user, change_password
import re

DEV_USERNAME = "dev"  # single dev username used for bypass

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
    Handles login, registration, change password, delete account, logout.
    Returns True if the user is logged in, False otherwise.
    """
    # -----------------------------
    # Initialize session state variables (including dev-mode guard)
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
        # dev mode
        "dev_mode_enabled": False,
        "prev_dev_mode": False,  # track previous checkbox value to detect toggles
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # -----------------------------
    # Dev Mode checkbox (single toggle)
    # - When checked -> automatically log in as `DEV_USERNAME`
    # - When unchecked -> if previously in dev mode, log out and return to login screen
    # -----------------------------
    st.markdown("**Developer / Test Mode (local only)**")
    st.session_state.dev_mode_enabled = st.checkbox(
        "Enable Dev Mode (bypass login)",
        value=st.session_state.dev_mode_enabled,
        help="Toggle to bypass login for local testing. Uncheck to return to the login screen."
    )

    # Detect transitions
    prev = st.session_state.prev_dev_mode
    curr = st.session_state.dev_mode_enabled

    # If user toggled ON dev mode this run -> log in as dev immediately
    if not prev and curr:
        st.session_state.logged_in = True
        st.session_state.username = DEV_USERNAME
        st.session_state.screen = "login"  # keep main flow consistent
        # no return here — let the function continue so sidebar renders in same run

    # If user toggled OFF dev mode this run and they were logged in as dev -> log out
    if prev and not curr:
        if st.session_state.logged_in and st.session_state.username == DEV_USERNAME:
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.screen = "login"
            st.info("Dev Mode disabled — returned to login screen.")

    # update prev_dev_mode for next run
    st.session_state.prev_dev_mode = curr

    # -----------------------------
    # Logged-in state: show sidebar and account management
    # -----------------------------
    if st.session_state.logged_in:
        st.sidebar.success(f"Logged in as {st.session_state.username}")

        # ---------------------------
        # Change Password
        # ---------------------------
        with st.sidebar.expander("Change Password"):
            with st.form(key="change_pw_form"):
                st.info("Note: Password must meet requirements: 8+ chars, 1 uppercase, 1 lowercase, 1 number")
                new_pw = st.text_input("New Password", type="password", key="new_pw")
                confirm_pw = st.text_input("Confirm New Password", type="password", key="confirm_pw")
                submit_pw = st.form_submit_button("Update Password")
                if submit_pw:
                    if new_pw != confirm_pw:
                        st.warning("⚠️ Passwords do not match.")
                    elif not validate_password(new_pw):
                        st.warning("⚠️ Password does not meet requirements.")
                    else:
                        # dev user is not persisted
                        if st.session_state.username == DEV_USERNAME:
                            st.info("Dev user — password change skipped (not persisted).")
                        else:
                            if change_password(st.session_state.username, new_pw):
                                st.success("✅ Password updated successfully.")
                            else:
                                st.error("❌ Could not update password.")

        # -----------------------------
        # Logout
        # -----------------------------
        if st.sidebar.button("Logout"):
            # If logged out via sidebar, also clear dev-mode checkbox if it was set
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.screen = "login"
            st.session_state.message = ""
            if st.session_state.dev_mode_enabled:
                st.session_state.dev_mode_enabled = False
                st.session_state.prev_dev_mode = False

        # ---------------------------
        # Delete Account
        # ---------------------------
        with st.sidebar.expander("Delete Account"):
            with st.form(key="delete_account_form"):
                st.warning("⚠️ Deleting your account is permanent!")
                confirm_delete = st.checkbox("I understand and want to delete my account", key="confirm_delete")
                submit_delete = st.form_submit_button("Delete Account Permanently")
                if submit_delete:
                    if confirm_delete:
                        if st.session_state.username == DEV_USERNAME:
                            st.info("Dev user — nothing to delete from persistent store.")
                            st.session_state.logged_in = False
                            st.session_state.username = ""
                            st.session_state.screen = "login"
                            # also clear dev-mode checkbox
                            st.session_state.dev_mode_enabled = False
                            st.session_state.prev_dev_mode = False
                        else:
                            if delete_user(st.session_state.username):
                                st.success("✅ Account deleted successfully.")
                                st.session_state.logged_in = False
                                st.session_state.username = ""
                                st.session_state.screen = "login"
                            else:
                                st.error("❌ Could not delete account.")
                    else:
                        st.info("Please confirm deletion by checking the box.")

        return True  # logged in

    # -----------------------------
    # Login Screen (normal)
    # -----------------------------
    if st.session_state.screen == "login":
        st.subheader("Login")
        st.write("Enter your username and password. If you don't have an account, click Register.")
        st.write("**Note:** You may need to double-click buttons due to Streamlit behavior.")

        # Use a form for predictable submit behavior
        with st.form(key="login_form"):
            st.session_state.login_username = st.text_input(
                "Username", value=st.session_state.login_username
            )
            st.session_state.login_password = st.text_input(
                "Password", type="password", value=st.session_state.login_password
            )
            col1, col2 = st.columns(2)
            with col1:
                login_submitted = st.form_submit_button("Login")
            with col2:
                register_clicked = st.form_submit_button("Register")

        if login_submitted:
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

        # Use a form for register as well
        with st.form(key="register_form"):
            st.session_state.register_username = st.text_input(
                "Desired Username", value=st.session_state.register_username
            )
            st.session_state.register_password = st.text_input(
                "Desired Password", type="password", value=st.session_state.register_password
            )
            col1, col2 = st.columns(2)
            with col1:
                confirm_submitted = st.form_submit_button("Confirm Registration")
            with col2:
                back_submitted = st.form_submit_button("Back to Login")

        if confirm_submitted:
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

        if back_submitted:
            st.session_state.screen = "login"
            st.session_state.message = ""

    return st.session_state.logged_in



# # auth_ui.py (dev-bypass removed)
# import streamlit as st
# from auth_utils import login, register, delete_user, change_password
# import re
# 
# def validate_password(password):
#     """Check if password meets requirements."""
#     if len(password) < 8:
#         return False
#     if not re.search(r"[A-Z]", password):
#         return False
#     if not re.search(r"[a-z]", password):
#         return False
#     if not re.search(r"\d", password):
#         return False
#     return True
# 
# def auth_ui():
#     """
#     Handles login, registration, change password, delete account, logout.
#     Returns True if the user is logged in, False otherwise.
#     """
#     # -----------------------------
#     # Initialize session state variables
#     # -----------------------------
#     defaults = {
#         "logged_in": False,
#         "username": "",
#         "screen": "login",
#         "login_username": "",
#         "login_password": "",
#         "register_username": "",
#         "register_password": "",
#         "message": "",
#     }
#     for key, value in defaults.items():
#         if key not in st.session_state:
#             st.session_state[key] = value
# 
#     # -----------------------------
#     # Logged-in state: show sidebar and account management
#     # -----------------------------
#     if st.session_state.logged_in:
#         st.sidebar.success(f"Logged in as {st.session_state.username}")
# 
#         # ---------------------------
#         # Change Password
#         # ---------------------------
#         with st.sidebar.expander("Change Password"):
#             with st.form(key="change_pw_form"):
#                 st.info("Note: Password must meet requirements: 8+ chars, 1 uppercase, 1 lowercase, 1 number")
#                 new_pw = st.text_input("New Password", type="password", key="new_pw")
#                 confirm_pw = st.text_input("Confirm New Password", type="password", key="confirm_pw")
#                 submit_pw = st.form_submit_button("Update Password")
#                 if submit_pw:
#                     if new_pw != confirm_pw:
#                         st.warning("⚠️ Passwords do not match.")
#                     elif not validate_password(new_pw):
#                         st.warning("⚠️ Password does not meet requirements.")
#                     else:
#                         if change_password(st.session_state.username, new_pw):
#                             st.success("✅ Password updated successfully.")
#                         else:
#                             st.error("❌ Could not update password.")
# 
#         # -----------------------------
#         # Logout
#         # -----------------------------
#         if st.sidebar.button("Logout"):
#             st.session_state.logged_in = False
#             st.session_state.username = ""
#             st.session_state.screen = "login"
#             st.session_state.message = ""
# 
#         # ---------------------------
#         # Delete Account
#         # ---------------------------
#         with st.sidebar.expander("Delete Account"):
#             with st.form(key="delete_account_form"):
#                 st.warning("⚠️ Deleting your account is permanent!")
#                 confirm_delete = st.checkbox("I understand and want to delete my account", key="confirm_delete")
#                 submit_delete = st.form_submit_button("Delete Account Permanently")
#                 if submit_delete:
#                     if confirm_delete:
#                         if delete_user(st.session_state.username):
#                             st.success("✅ Account deleted successfully.")
#                             st.session_state.logged_in = False
#                             st.session_state.username = ""
#                             st.session_state.screen = "login"
#                         else:
#                             st.error("❌ Could not delete account.")
#                     else:
#                         st.info("Please confirm deletion by checking the box.")
# 
#         return True
# 
#     # -----------------------------
#     # Login Screen
#     # -----------------------------
#     if st.session_state.screen == "login":
#         st.subheader("Login")
#         st.write("Enter your username and password. If you don't have an account, click Register.")
#         st.write("**Note:** You may need to double-click buttons due to Streamlit behavior.")
# 
#         # Use a form for predictable submit behavior
#         with st.form(key="login_form"):
#             st.session_state.login_username = st.text_input(
#                 "Username", value=st.session_state.login_username
#             )
#             st.session_state.login_password = st.text_input(
#                 "Password", type="password", value=st.session_state.login_password
#             )
#             col1, col2 = st.columns(2)
#             with col1:
#                 login_submitted = st.form_submit_button("Login")
#             with col2:
#                 register_clicked = st.form_submit_button("Register")
# 
#         if login_submitted:
#             username = st.session_state.login_username.strip()
#             password = st.session_state.login_password.strip()
#             if username == "" or password == "":
#                 st.warning("⚠️ Username and password cannot be empty.")
#             elif login(username, password):
#                 st.session_state.logged_in = True
#                 st.session_state.username = username
#                 st.session_state.login_username = ""
#                 st.session_state.login_password = ""
#                 st.success(f"✅ Logged in as {username}")
#             else:
#                 st.session_state.login_username = ""
#                 st.session_state.login_password = ""
#                 st.error("❌ Incorrect username or password.")
# 
#         if register_clicked:
#             st.session_state.screen = "register"
#             st.session_state.message = ""
# 
#     # -----------------------------
#     # Register Screen
#     # -----------------------------
#     elif st.session_state.screen == "register":
#         st.subheader("Register")
#         st.write(
#             "Create a new account. Password must be at least 8 characters long, "
#             "contain at least 1 uppercase, 1 lowercase, and 1 number."
#         )
#         st.write("**Note:** You may need to double-click buttons due to Streamlit behavior.")
# 
#         # Use a form for register as well
#         with st.form(key="register_form"):
#             st.session_state.register_username = st.text_input(
#                 "Desired Username", value=st.session_state.register_username
#             )
#             st.session_state.register_password = st.text_input(
#                 "Desired Password", type="password", value=st.session_state.register_password
#             )
#             col1, col2 = st.columns(2)
#             with col1:
#                 confirm_submitted = st.form_submit_button("Confirm Registration")
#             with col2:
#                 back_submitted = st.form_submit_button("Back to Login")
# 
#         if confirm_submitted:
#             username = st.session_state.register_username.strip()
#             password = st.session_state.register_password.strip()
#             if username == "" or password == "":
#                 st.warning("⚠️ Username and password cannot be empty.")
#             elif not validate_password(password):
#                 st.warning("⚠️ Password does not meet requirements.")
#             elif register(username, password):
#                 st.success("✅ Registration successful! Please login.")
#                 st.session_state.screen = "login"
#                 st.session_state.register_username = ""
#                 st.session_state.register_password = ""
#             else:
#                 st.error("❌ Username already exists. Choose another.")
# 
#         if back_submitted:
#             st.session_state.screen = "login"
#             st.session_state.message = ""
# 
#     return st.session_state.logged_in
