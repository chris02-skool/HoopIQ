# Placeholder data for development-only session data
# dev_placeholder.py

from datetime import datetime
import pandas as pd
from data import df, shots, component_avg, game_make_avg
import copy

def generate_placeholder_sessions():
    """
    Generate placeholder session data for testing the session sidebar.
    Returns:
        sessions_newest (list): 3 newest sessions with full data
        sessions_oldest (list): 7 oldest sessions with averages only
    """
    # Newest 3 sessions (full data)
    sessions_newest = []
    for i in range(3):
        session = {
            "name": f"Session {i+1}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "df": copy.deepcopy(df),
            "shots": copy.deepcopy(shots)
        }
        sessions_newest.append(session)

    # Oldest 7 sessions (averages only)
    sessions_oldest = []
    for i in range(7):
        session = {
            "name": f"Session {i+4}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "averages": copy.deepcopy(component_avg),
            "make_rate": game_make_avg
        }
        sessions_oldest.append(session)

    return sessions_newest, sessions_oldest
