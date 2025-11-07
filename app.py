# Basketball Shot Tracker App
# Developed by Christopher Hong
# Team Name: HoopIQ
# Team Members: Christopher Hong, Alfonso Mejia Vasquez, Gondra Kelly, Matthew Margulies, Carlos Orozco
# Start Web Development Date: October 2025
# Finished Web Development Date: June 2026 (Ideally)
# app.py

import streamlit as st
from data import df, shots, component_avg, game_make_avg
from shot_selection import selected_shots_idx
from plot_utils import plot_top_view, plot_side_view
from export_utils import export_section
from notes import show_notes
from sidebar_ui import sidebar_ui

# -----------------------------
# Streamlit config
# -----------------------------
st.set_page_config(page_title="Basketball Shot Tracker", layout="wide")

# -----------------------------
# Sidebar
# -----------------------------
# Set dev_mode=True for testing without real login/data
newest_sessions, oldest_sessions, newest_indices = sidebar_ui(dev_mode=True)
if newest_sessions is None:
    st.stop()  # Not logged in

# -----------------------------
# Main App
# -----------------------------
st.title("🏀 Basketball Shot Tracker")

# -----------------------------
# Section 1: Oldest sessions overview
# -----------------------------
if st.session_state.get("show_oldest", False):
    st.header("Oldest Sessions (4th-10th)")
    if oldest_sessions:
        avg_table = []
        for i, s in enumerate(oldest_sessions):
            avg_table.append({
                "Session": f"{i+4}",  # 4th to 10th
                "Datetime": s["datetime"],
                "Backboard": s["component_avg"]["Backboard"],
                "Rim": s["component_avg"]["Rim"],
                "Net": s["component_avg"]["Net"],
                "Game Make %": s["game_make_avg"]
            })
        st.table(avg_table)
    else:
        st.info("No older sessions yet.")
else:
    # -----------------------------
    # Section 2: Newest sessions full data
    # -----------------------------
    st.header("Shot Results / Selected Sessions")
    combined_shots = []
    combined_component_avg = {"Backboard":0, "Rim":0, "Net":0}
    combined_game_make_avg = 0.0

    if newest_sessions:
        for idx in newest_indices:
            session = newest_sessions[idx]
            combined_shots.extend(session.get("shot_data", []))
            comp = session.get("component_avg", {"Backboard":0, "Rim":0, "Net":0})
            combined_component_avg["Backboard"] += comp["Backboard"]
            combined_component_avg["Rim"] += comp["Rim"]
            combined_component_avg["Net"] += comp["Net"]
            combined_game_make_avg += session.get("game_make_avg", 0)

        n = len(newest_indices)
        if n > 0:
            combined_component_avg = {k:v/n for k,v in combined_component_avg.items()}
            combined_game_make_avg /= n

    st.dataframe(df)  # Placeholder: real implementation would merge session shot_data
    st.markdown("**Technical Component Averages:**")
    st.write(combined_component_avg)
    st.write(f"**Overall Game Make Rate:** {combined_game_make_avg:.2f}")

    # -----------------------------
    # Section 3: Shot Selection
    # -----------------------------
    st.header("Select Shot(s) to Display")
    selected_shots_idx(combined_shots)

    # -----------------------------
    # Section 4: Plots
    # -----------------------------
    col1, col2 = st.columns(2)
    with col1:
        plot_top_view(combined_shots, list(range(len(combined_shots))))
    with col2:
        plot_side_view(combined_shots, list(range(len(combined_shots))))

# -----------------------------
# Section 5: Export
# -----------------------------
st.header("Export Data")
export_section(df, component_avg)

# -----------------------------
# Section 6: Notes
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
