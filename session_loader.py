# session_loader.py
import json
import pandas as pd
import os

def load_newest_3_sessions(username):
    """Load the 3 newest sessions for a given user from JSON."""
    filename = f"{username}_newest_3_session.json"
    filepath = os.path.join(os.path.dirname(__file__), filename)

    # Read JSON file
    with open(filepath, "r") as f:
        data = json.load(f)

    # Sort sessions by datetime descending (newest first)
    sorted_sessions = sorted(data, key=lambda s: s["datetime"], reverse=True)

    # Return up to 3 newest sessions
    return sorted_sessions[:3]
