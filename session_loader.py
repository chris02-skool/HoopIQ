# session_loader.py
import json
import pandas as pd
import os

def load_newest_session(username):
    """Loads the newest session data for a given user from JSON."""
    filename = f"{username}_newest_3_session.json"
    filepath = os.path.join(os.path.dirname(__file__), filename)

    # Check if file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Session file not found for user: {username}")

    # Read JSON (which is a list of sessions)
    with open(filepath, "r") as f:
        data = json.load(f)

    if not isinstance(data, list) or len(data) == 0:
        raise ValueError(f"No session data found in {filename}")

    # Sort by datetime (most recent first) and take the newest one
    newest_session = sorted(data, key=lambda s: s["datetime"], reverse=True)[0]

    # Convert df data to a pandas DataFrame
    df = pd.DataFrame(newest_session["df"])
    shots = newest_session["shots"]

    # Compute averages
    component_avg = {
        col: round(df[col].mean(), 2) for col in ["Backboard", "Rim", "Net"]
    }
    game_make_avg = round(df["Game Make"].mean(), 2)

    return df, shots, component_avg, game_make_avg
