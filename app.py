# Basketball Shot Tracker App
# Developed by Christopher Hong
# Team Name: HoopIQ
# Team Members: Christopher Hong, Alfonso Mejia Vasquez, Gondra Kelly, Matthew Margulies, Carlos Orozco
# Start Web Development Date: October 2025
# Finished Web Development Date: June 2026 (Ideally)
# app.py

import streamlit as st
# from data import df, shots, component_avg, game_make_avg
from session_loader import load_newest_3_sessions
from shot_selection import selected_shots_idx
from plot_utils import plot_top_view, plot_side_view
from export_utils import export_section
from notes import show_notes
from auth_ui import auth_ui
import pandas as pd

# -----------------------------
# Streamlit config
# -----------------------------
st.set_page_config(page_title="Basketball Shot Tracker", layout="wide")

# -----------------------------
# Login
# -----------------------------
logged_in = auth_ui()
if not logged_in:
    st.stop()

# -----------------------------
# ✅ Load the newest session data here (allow selecting from 3 newest)
# -----------------------------
username = st.session_state.get("username")
if not username:
    st.warning("Please log in or enable dev mode to load session data.")
    st.stop()

# Load up to 3 newest sessions
newest_sessions = load_newest_3_sessions(username)

# Build selection options
session_options = [
    f"Session {s['session_number']} ({s['datetime']})" for s in newest_sessions
]

# Let user pick which session to load
selected_session_idx = st.selectbox(
    "Select a session to view", 
    range(len(session_options)),
    format_func=lambda x: session_options[x]
)

# Load the selected session
selected_session = newest_sessions[selected_session_idx]
df = pd.DataFrame(selected_session["df"])
shots = selected_session["shots"]
component_avg = {col: df[col].mean() for col in ["Backboard", "Rim", "Net"]}
game_make_avg = df["Game Make"].mean()

# -----------------------------
# Main App
# -----------------------------
st.title("🏀 Basketball Shot Tracker")

# -----------------------------
# Section 1: Shot Results
# -----------------------------
st.header("Shot Results")
st.dataframe(df)
st.markdown("**Technical Component Averages:**")
st.write(component_avg)
st.write(f"**Overall Game Make Rate:** {game_make_avg:.2f}")

# -----------------------------
# Section 2: Shot Selection
# -----------------------------
st.header("Select Shot(s) to Display")
selected_idx = selected_shots_idx(shots)

# -----------------------------
# Section 3: Plots
# -----------------------------
col1, col2 = st.columns(2)
with col1:
    # guard: ensure selected_idx is a list of valid indices
    safe_selected_idx = [i for i in selected_idx if isinstance(i, int) and 0 <= i < len(shots)]
    plot_top_view(shots, safe_selected_idx)
with col2:
    plot_side_view(shots, safe_selected_idx)

# -----------------------------
# Section 4: Export
# -----------------------------
st.header("Export Data")
export_section(df, component_avg)

# -----------------------------
# Section 5: Notes
# -----------------------------
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
# - Add ability to save and load shot data
# - Add 10 session limit, with the oldest 7 show averages and the latest 3 show individual shot data.
# - Add ability to compare multiple sessions (Bonus goal)
# - Add more detailed technical feedback based on shot data (if possible)
# - Data should add lines after every shot, so the user can see their progress over time (can only test with real data)
