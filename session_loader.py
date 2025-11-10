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
        raise FileNotFoundError(f"Session file not found for user: {filename}")

    # Read JSON file
    with open(filepath, "r") as f:
        data = json.load(f)

    # Get the newest session (last one in the list)
    newest_session = data["sessions"][-1]  # sessions list is ordered chronologically

    # Convert df data to DataFrame
    df = pd.DataFrame(newest_session["df"])
    shots = newest_session["shots"]

    # Compute component averages
    component_avg = {
        col: round(df[col].mean(), 2) for col in ["Backboard", "Rim", "Net"]
    }

    # Compute game make average
    game_make_avg = round(df["Game Make"].mean(), 2)

    return df, shots, component_avg, game_make_avg
