# Basketball Shot Tracker App
# Developed by Christopher Hong
# Team Name: HoopIQ
# Team Members: Christopher Hong, Alfonso Mejia Vasquez, Gondra Kelly, Matthew Margulies, Carlos Orozco
# Start Web Development Date: October 2025
# Finished Web Development Date: June 2026 (Ideally)
# app.py

# app.py
import streamlit as st
from auth_ui import auth_ui

# Import main menu (works for dev and real users)
from main_menu import main_menu

def app():
    st.set_page_config(page_title="Basketball Analyzer", layout="wide")

    # -------------------------
    # Authentication / Dev mode
    # -------------------------
    logged_in = auth_ui()  # this handles login, dev mode, register, etc.

    if logged_in:
        # Determine username and dev mode
        username = st.session_state.username
        dev_mode = username == "dev" and st.session_state.dev_mode_enabled

        # -------------------------
        # Show main menu
        # -------------------------
        main_menu(username, dev_mode=dev_mode)
    else:
        st.info("Please log in or enable Dev Mode to continue.")

if __name__ == "__main__":
    app()



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
# - Add ability to save and load shot data
# - Add 10 session limit, with the oldest 7 show averages and the latest 3 show individual shot data.
# - Add ability to compare multiple sessions (Bonus goal)
# - Add more detailed technical feedback based on shot data (if possible)
# - Data should add lines after every shot, so the user can see their progress over time (can only test with real data)
