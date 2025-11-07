# main_menu.py
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from plot_utils import plot_top_view, plot_side_view
from export_utils import export_section
from shot_selection import selected_shots_idx
from notes import show_notes

DEV_NEWEST_FILE = "dev_newest_3.json"
DEV_OLDEST_FILE = "dev_oldest_7.json"

def load_json(file_path):
    if not os.path.exists(file_path):
        st.warning(f"File {file_path} not found.")
        return []
    with open(file_path, "r") as f:
        return json.load(f)

def main_menu(username, dev_mode=False):
    st.title("Basketball Shot Analyzer")

    # -------------------------
    # Load sessions
    # -------------------------
    if dev_mode:
        newest_sessions = load_json(DEV_NEWEST_FILE)
        oldest_sessions = load_json(DEV_OLDEST_FILE)
    else:
        newest_file = f"{username}_newest_3.json"
        oldest_file = f"{username}_oldest_7.json"
        newest_sessions = load_json(newest_file)
        oldest_sessions = load_json(oldest_file)

    if "selected_session_idx" not in st.session_state:
        st.session_state.selected_session_idx = 0  # default: newest session 1

    # -------------------------
    # Sidebar buttons
    # -------------------------
    st.sidebar.header("Sessions")

    def set_session(idx):
        st.session_state.selected_session_idx = idx

    # Newest 3 sessions
    for i, session in enumerate(newest_sessions):
        btn_label = f"Session {session.get('session_number', '?')} - {session.get('datetime', session.get('date_time', session.get('date', 'Unknown Date')))}"
        if st.sidebar.button(btn_label):
            set_session(i)

    # Oldest 7 averages button
    if st.sidebar.button("Show 7 Oldest Average Stats"):
        st.session_state.selected_session_idx = -1  # special index for averages

    # -------------------------
    # Main display
    # -------------------------
    if st.session_state.selected_session_idx == -1:
        # Show oldest 7 average stats
        st.subheader("Average Stats: Oldest 7 Sessions")
        avg_stats = []
        for session in oldest_sessions:
            comp = session.get('component_avg', {})
            avg_stats.append({
                "Session": session['session_number'],
                "Date/Time": session['datetime'],
                "Backboard %": round(comp.get('Backboard', 0), 2),
                "Rim %": round(comp.get('Rim', 0), 2),
                "Net %": round(comp.get('Net', 0), 2),
                "Make %": round(comp.get('Game Make', 0), 2)
            })
        st.table(avg_stats)
    else:
        # Show full data of selected newest session
        session = newest_sessions[st.session_state.selected_session_idx]
        st.subheader(f"Session {session['session_number']} - {session['datetime']} Full Data")

        shots = session.get('shots', [])

        # -------------------------
        # Compute averages if missing
        # -------------------------
        if 'component_avg' in session:
            comp_avg = session['component_avg']
        else:
            if shots:
                df = pd.DataFrame(shots)
                comp_avg = df[['Backboard', 'Rim', 'Net']].mean().to_dict()
                comp_avg['Game Make'] = df['Game Make'].mean()
            else:
                comp_avg = {"Backboard": 0, "Rim": 0, "Net": 0, "Game Make": 0}

        # Get selected shots indices for display
        selected_idx = selected_shots_idx(shots)

        # Top view and side view plots
        plot_top_view(shots, selected_idx)
        plot_side_view(shots, selected_idx)

        # Component averages
        st.markdown("### Component Averages")
        st.write({
            "Backboard": round(comp_avg['Backboard'], 2),
            "Rim": round(comp_avg['Rim'], 2),
            "Net": round(comp_avg['Net'], 2),
            "Game Make": round(comp_avg['Game Make'], 2)
        })

        # Export section
        export_section(pd.DataFrame(shots), comp_avg)

        # Notes
        show_notes()

    st.info("✅ Data loaded successfully.")
