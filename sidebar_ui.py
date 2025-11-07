# Sidebar UI for Basketball Shot Tracker
# Handles dev mode, session management, and user authentication
# sidebar_ui.py

import streamlit as st
import json
import datetime
from auth_ui import auth_ui
from dev_placeholder import generate_placeholder_sessions  # Only used in dev mode

def sidebar_ui(dev_mode=False):
    """Handles sidebar UI including login, sessions, and account management."""

    # -----------------------------
    # Login/Register
    # -----------------------------
    if not dev_mode:
        logged_in = auth_ui()
        if not logged_in:
            return None, None, None  # No user logged in
    else:
        # Dev bypass
        st.session_state.logged_in = True

    username = st.session_state.username
    st.sidebar.success(f"Logged in as {username}")

    # -----------------------------
    # Filenames for user sessions
    # -----------------------------
    newest_file = f"{username}_newest_3_sessions.json"
    oldest_file = f"{username}_oldest_7_sessions.json"

    # Load session data
    try:
        with open(newest_file, "r") as f:
            newest_sessions = json.load(f)
    except FileNotFoundError:
        newest_sessions = []

    try:
        with open(oldest_file, "r") as f:
            oldest_sessions = json.load(f)
    except FileNotFoundError:
        oldest_sessions = []

    # -----------------------------
    # Dev mode: placeholder sessions
    # -----------------------------
    if dev_mode and not newest_sessions and not oldest_sessions:
        newest_sessions, oldest_sessions = generate_placeholder_sessions(username)

    # -----------------------------
    # Sidebar: Sessions
    # -----------------------------
    st.sidebar.header("📊 Sessions")

    # Add new session button
    if st.sidebar.button("Scan Ball / Add New Session"):
        new_session = {
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "shot_data": [],
            "component_avg": {"Backboard":0, "Rim":0, "Net":0},
            "game_make_avg": 0.0
        }

        # Shift sessions: move oldest newest session to oldest 7
        if newest_sessions:
            session_to_oldest = newest_sessions.pop(-1)
            avg_only = {
                "datetime": session_to_oldest["datetime"],
                "component_avg": session_to_oldest["component_avg"],
                "game_make_avg": session_to_oldest["game_make_avg"]
            }
            oldest_sessions.append(avg_only)
            if len(oldest_sessions) > 7:
                oldest_sessions.pop(0)  # remove 10th oldest

        newest_sessions.insert(0, new_session)

        # Save sessions
        with open(newest_file, "w") as f:
            json.dump(newest_sessions, f, indent=4)
        with open(oldest_file, "w") as f:
            json.dump(oldest_sessions, f, indent=4)

    # -----------------------------
    # Select newest sessions
    # -----------------------------
    st.sidebar.subheader("View Latest 3 Sessions")
    selected_newest = st.sidebar.multiselect(
        "Select sessions to display",
        options=[f"{i+1}: {s['datetime']}" for i, s in enumerate(newest_sessions)],
        default=[f"{i+1}: {s['datetime']}" for i, s in enumerate(newest_sessions)]
    )
    newest_indices = [int(s.split(":")[0])-1 for s in selected_newest]

    # Show oldest sessions toggle
    if st.sidebar.button("Show Oldest 4th-10th Sessions"):
        st.session_state.show_oldest = True
    else:
        st.session_state.show_oldest = False

    return newest_sessions, oldest_sessions, newest_indices
