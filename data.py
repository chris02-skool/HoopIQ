# data.py
import pandas as pd
import json
import os

# Path to JSON file
JSON_FILE = os.path.join(os.path.dirname(__file__), "dev_shot_session_1.json")

# Load JSON
with open(JSON_FILE, "r") as f:
    data = json.load(f)

# DataFrame for shot results
df = pd.DataFrame(data["df"])
df.index = df.index + 1  # start index at 1

# Component averages and game make rate
component_avg = df[["Backboard", "Rim", "Net"]].mean()
game_make_avg = df["Game Make"].mean()

# Shot trajectories
shots = data["shots"]
