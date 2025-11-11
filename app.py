# Basketball Shot Tracker App
# Developed by Christopher Hong
# Team Name: HoopIQ
# Team Members: Christopher Hong, Alfonso Mejia Vasquez, Gondra Kelly, Matthew Margulies, Carlos Orozco
# Start Web Development Date: October 2025
# Finished Web Development Date: June 2026 (Ideally)
# app.py

import streamlit as st
import pandas as pd
from session_loader import load_newest_3_sessions, load_oldest_7_sessions
from shot_selection import selected_shots_idx
from plot_utils import plot_top_view, plot_side_view
from export_utils import export_section
from notes import show_notes
from auth_ui import auth_ui

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
# Load user session data
# -----------------------------
username = st.session_state.get("username")
if not username:
    st.warning("Please log in or enable dev mode to load session data.")
    st.stop()

# Load sessions
newest_sessions = load_newest_3_sessions(username)
oldest_sessions = load_oldest_7_sessions(username)

# -----------------------------
# Session selection dropdown
# -----------------------------
session_options = [
    f"Session {s['session_number']} ({s['datetime']})" for s in newest_sessions
] + ["Oldest Sessions 4-10"]

selected_session_idx = st.selectbox(
    "Select a session to view",
    range(len(session_options)),
    format_func=lambda x: session_options[x]
)

# -----------------------------
# Load session data based on selection
# -----------------------------
if selected_session_idx < 3:
    # Individual newest session
    selected_session = newest_sessions[selected_session_idx]
    df = pd.DataFrame(selected_session["df"])
    shots = selected_session["shots"]
    component_avg = {col: df[col].mean() for col in ["Backboard", "Rim", "Net"]}
    game_make_avg = df["Game Make"].mean()
    show_individual = True
else:
    # Oldest 4–10 sessions summary
    df = pd.DataFrame([{
        "Session Number": s["session_number"],
        "DateTime": s["datetime"],
        "Backboard Avg": s["Component_Averages"]["Backboard"],
        "Rim Avg": s["Component_Averages"]["Rim"],
        "Net Avg": s["Component_Averages"]["Net"],
        "Game Make Avg": s["Game_Make_Avg"],
        "Total Shots": s["Total_Shots"],
        "Makes": s["Makes"],
        "Misses": s["Misses"]
    } for s in oldest_sessions])
    
    # Sort table newest → oldest
    df = df.sort_values("DateTime", ascending=False).reset_index(drop=True)
    
    shots = []
    component_avg = {
        "Backboard": df["Backboard Avg"].mean(),
        "Rim": df["Rim Avg"].mean(),
        "Net": df["Net Avg"].mean()
    }
    game_make_avg = None
    show_individual = False

# -----------------------------
# Main App
# -----------------------------
st.title("🏀 Basketball Shot Tracker")

# -----------------------------
# Section 1: Shot Results
# -----------------------------
st.header("Shot Results")
st.dataframe(df)

if show_individual:
    st.markdown("**Technical Component Averages:**")
    st.write(component_avg)
    st.write(f"**Overall Game Make Rate:** {game_make_avg:.2f}")
else:
    st.info("Showing summary of oldest sessions. Individual shot selection, plots, and averages are not available.")

# -----------------------------
# Section 2 & 3: Shot Selection and Plots
# -----------------------------
if show_individual:
    st.header("Select Shot(s) to Display")
    selected_idx = selected_shots_idx(shots)

    col1, col2 = st.columns(2)
    with col1:
        safe_selected_idx = [i for i in selected_idx if isinstance(i, int) and 0 <= i < len(shots)]
        plot_top_view(shots, safe_selected_idx)
    with col2:
        plot_side_view(shots, safe_selected_idx)

# -----------------------------
# Section 4: Export
# -----------------------------
st.header("Export Data")
if show_individual:
    export_section(df, component_avg)
else:
    st.info("Export not available for summary of oldest sessions.")

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
# - Find a way to move the old session when a new session is created
# - Add ability to save shot data
# - Add ability to compare multiple sessions (Bonus goal)
# - Add more detailed technical feedback based on shot data (if possible)
# - Data should add lines after every shot, so the user can see their progress over time (can only test with real data)
