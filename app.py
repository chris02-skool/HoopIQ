# Basketball Shot Tracker App
# Developed by Christopher Hong
# Team Name: HoopIQ
# Team Members: Christopher Hong, Alfonso Mejia Vasquez, Gondra Kelly, Matthew Margulies, Carlos Orozco
# Start Web Development Date: October 2025
# Finished Web Development Date: June 2026 (Ideally)
 

import streamlit as st
from data import df, shots, component_avg, game_make_avg
from shot_selection import selected_shots_idx
from plot_utils import plot_top_view, plot_side_view
from export_utils import export_section
from notes import show_notes
from auth_utils import login, register, get_user_sessions, add_user_session

# -----------------------------
# Streamlit config
# -----------------------------
st.set_page_config(page_title="Basketball Shot Tracker", layout="wide")

# -----------------------------
# Session state defaults
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "screen" not in st.session_state:
    st.session_state.screen = "login"

# -----------------------------
# Logout function
# -----------------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.username = None

# -----------------------------
# Authentication UI
# -----------------------------
if not st.session_state.logged_in:
    if st.session_state.screen == "login":
        st.subheader("Login")
        st.write("Enter your username and password. If you don't have an account, click Register.")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        col1, col2 = st.columns(2)
        with col1:
            login_clicked = st.button("Login")
        with col2:
            register_clicked = st.button("Register")

        if login_clicked:
            if username.strip() == "" or password.strip() == "":
                st.warning("Username and password cannot be empty.")
            elif login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Logged in as {username}")
            else:
                st.error("Incorrect username or password.")

        if register_clicked:
            st.session_state.screen = "register"

    elif st.session_state.screen == "register":
        st.subheader("Register")
        st.write("Create a new account.")
        new_username = st.text_input("Desired Username")
        new_password = st.text_input("Desired Password", type="password")

        col1, col2 = st.columns(2)
        with col1:
            confirm_clicked = st.button("Confirm Registration")
        with col2:
            back_clicked = st.button("Back to Login")

        if confirm_clicked:
            if new_username.strip() == "" or new_password.strip() == "":
                st.warning("Username and password cannot be empty.")
            elif register(new_username, new_password):
                st.success("Registration successful! Please login.")
                st.session_state.screen = "login"
            else:
                st.error("Username already exists. Choose another.")

        if back_clicked:
            st.session_state.screen = "login"

    st.stop()  # Stop rendering the main app until login
else:
    # -----------------------------
    # Logged-in Sidebar
    # -----------------------------
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    if st.sidebar.button("Logout"):
        logout()
        st.experimental_rerun()  # rerun to show login screen

# -----------------------------
# Main App (only for logged-in users)
# -----------------------------
st.title("🏀 Basketball Shot Tracker")

# Section 1: Shot Results
st.header("Shot Results")
st.dataframe(df)
st.markdown("**Technical Component Averages:**")
st.write(component_avg)
st.write(f"**Overall Game Make Rate:** {game_make_avg:.2f}")

# Section 2: Shot Selection
st.header("Select Shot(s) to Display")
selected_shots_idx = selected_shots_idx(shots)

# Section 3: Plots
col1, col2 = st.columns(2)
with col1:
    plot_top_view(shots, selected_shots_idx)
with col2:
    plot_side_view(shots, selected_shots_idx)

# Section 4: Export
st.header("Export Data")
export_section(df, component_avg)

# Section 5: Notes
show_notes()

# --------------------------------------
# 📝 Dev Notes
# --------------------------------------
#
# NOTES:
# - Next Step: Add real ball trajectory data when available.
# - Future: Let users export multiple datasets in one file.
# - A button to let the user scan their ball using the camera from tracking codes (will be at top).
# - Integrate real sensor data for shot results and trajectory.
# - Add a heat map of shot locations on the court to show how good you shot from a certain spot
# - Add sessions for when the user uses the app multiple times
# - Add user authentication for multiple users
# - Add ability to save and load shot data
# - Add 10 session limit, with the oldest 7 show averages and the latest 3 show individual shot data.
# - Add ability to compare multiple sessions (Bonus goal)
# - Add ability to overlay multiple shot trajectories for comparison (Should be implemented since plan was to show multiple shots in one court graph)
# - Add ability to adjust shot parameters (angle, speed) and see predicted trajectory
# - Add more detailed technical feedback based on shot data (if possible)
# - Data should add lines after every shot, so the user can see their progress over time