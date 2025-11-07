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
    
    # Step 1: Login/Register
    logged_in = auth_ui()
    if not logged_in:
        return None, None, None  # No user logged in

    username = st.session_state.username
    st.sidebar.success(f"Logged in as {username}")

    # Filenames for user sessions
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

    # Dev mode: generate placeholder sessions if empty
    if dev_mode and not newest_sessions and not oldest_sessions:
        newest_sessions, oldest_sessions = generate_placeholder_sessions(username)

    st.sidebar.header("📊 Sessions")

    # Step 2: Add new session button
    if st.sidebar.button("Scan Ball / Add New Session"):
        # Create new session placeholder
        new_session = {
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "shot_data": [],  # Placeholder, will be filled later
            "component_avg": {"Backboard":0, "Rim":0, "Net":0},
            "game_make_avg": 0.0
        }

        # Shift sessions: move oldest newest session to oldest 7
        if newest_sessions:
            session_to_oldest = newest_sessions.pop(-1)
            # Keep only average info
            avg_only = {
                "datetime": session_to_oldest["datetime"],
                "component_avg": session_to_oldest["component_avg"],
                "game_make_avg": session_to_oldest["game_make_avg"]
            }
            oldest_sessions.append(avg_only)
            if len(oldest_sessions) > 7:
                oldest_sessions.pop(0)  # remove 10th oldest

        newest_sessions.insert(0, new_session)  # add new as newest

        # Save sessions
        with open(newest_file, "w") as f:
            json.dump(newest_sessions, f, indent=4)
        with open(oldest_file, "w") as f:
            json.dump(oldest_sessions, f, indent=4)

    # Step 3: Select sessions to view
    st.sidebar.subheader("View Latest 3 Sessions")
    selected_newest = st.sidebar.multiselect(
        "Select sessions to display",
        options=[f"{i+1}: {s['datetime']}" for i, s in enumerate(newest_sessions)],
        default=[f"{i+1}: {newest_sessions[i]['datetime']}" for i in range(len(newest_sessions))]
    )
    newest_indices = [int(s.split(":")[0])-1 for s in selected_newest]

    if st.sidebar.button("Show Oldest 4th-10th Sessions"):
        st.session_state.show_oldest = True
    else:
        st.session_state.show_oldest = False

    return newest_sessions, oldest_sessions, newest_indices
