# Placeholder data for development-only session data
# dev_placeholder.py

from datetime import datetime
import copy
from data import df, shots, component_avg, game_make_avg

def generate_placeholder_sessions(username):
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
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "shot_data": copy.deepcopy(df),
            "component_avg": copy.deepcopy(component_avg),
            "game_make_avg": game_make_avg,
            "shots": copy.deepcopy(shots)
        }
        sessions_newest.append(session)

    # Oldest 7 sessions (averages only)
    sessions_oldest = []
    for i in range(7):
        session = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "component_avg": copy.deepcopy(component_avg),
            "game_make_avg": game_make_avg
        }
        sessions_oldest.append(session)

    return sessions_newest, sessions_oldest
