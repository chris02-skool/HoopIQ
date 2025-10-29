# HoopIQ Basketball Shot Tracker
# Tracks shot history, calculates averages, and shows top & side trajectory views

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="HoopIQ - Basketball Shot Tracker", layout="wide")
st.title("🏀 HoopIQ - Basketball Shot Tracker")

# -----------------------------
# Section 1: Shot Results Table
# -----------------------------
st.header("Shot Results")

# Example shot data (replace with sensor data later)
data = {
    "Backboard": [1, 0, 1, 1, 0],
    "Rim": [1, 0, 0, 1, 1],
    "Net": [0, 0, 1, 0, 1],
    "Game Make": [1, 0, 1, 1, 1]
}

df = pd.DataFrame(data)

# Calculate averages
component_avg = df[["Backboard", "Rim", "Net"]].mean()
game_make_avg = df["Game Make"].mean()

# Display table and averages
st.dataframe(df, use_container_width=True)
st.markdown("**Component Averages:**")
st.write(component_avg)
st.write(f"**Overall Game Make Rate:** {game_make_avg:.2f}")

# -----------------------------
# Section 2: Ball Trajectory
# -----------------------------
st.header("Ball Trajectory Visualization")

# User controls
user_x_offset = st.slider("Shooter horizontal position (ft)", -15, 15, 0)
user_y_distance = st.slider("Shot distance from hoop (ft)", 10, 40, 20)
max_shots = st.slider("Number of recent shots to show", 1, 30, 10)

# Generate sample shot history (to simulate actual data)
shots = []
now = datetime.now()
for i in range(20):
    x_offset = random.uniform(-15, 15)
    y_dist = random.uniform(10, 35)
    z_peak = random.uniform(8, 11)
    made = random.choice([True, False])
    shot_time = now - timedelta(seconds=i * 20)
    shots.append({
        "x_offset": x_offset,
        "y_dist": y_dist,
        "z_peak": z_peak,
        "made": made,
        "time": shot_time
    })

# Keep only most recent N shots
shots_to_plot = shots[-max_shots:]

# Compute fade intensity based on shot age
max_time = max(s["time"] for s in shots_to_plot)
min_time = min(s["time"] for s in shots_to_plot)
time_span = (max_time - min_time).total_seconds() or 1

# Create court drawings
top_fig = go.Figure()
side_fig = go.Figure()

# Court layout (Top View)
top_fig.add_shape(type="rect", x0=-25, y0=0, x1=25, y1=47,
                  line=dict(color="gray", width=2))
top_fig.add_shape(type="rect", x0=-8, y0=0, x1=8, y1=19,
                  line=dict(color="orange", width=2))
theta = [i for i in range(-90, 91)]
arc_x = [23.75 * (math.cos(t * math.pi / 180)) for t in theta]
arc_y = [23.75 * (math.sin(t * math.pi / 180)) for t in theta]
top_fig.add_trace(go.Scatter(x=arc_x, y=arc_y, mode='lines', line=dict(color="orange")))
top_fig.add_shape(type="circle", x0=-0.75, y0=-0.75, x1=0.75, y1=0.75,
                  line=dict(color="red", width=3))

# Hoop & backboard (Side View)
side_fig.add_shape(type="line", x0=0, y0=0, x1=user_y_distance + 5, y1=0,
                   line=dict(color="brown", width=3))
side_fig.add_shape(type="rect", x0=-1, y0=3.5, x1=0, y1=10.5,
                   line=dict(color="black", width=2), fillcolor="lightgray")
side_fig.add_shape(type="circle", x0=-0.75, y0=9.25, x1=0.75, y1=10.75,
                   line=dict(color="red", width=3))

# Plot each shot with fading color
for shot in shots_to_plot:
    time_diff = (max_time - shot["time"]).total_seconds()
    fade = 1 - (time_diff / time_span) * 0.8
    alpha = max(0.2, fade)
    color = f"rgba(0, 0, 255, {alpha})" if shot["made"] else f"rgba(255, 0, 0, {alpha})"

    # Generate a simple arc for top and side views
    x_vals = [shot["x_offset"], shot["x_offset"] * 0.6, 0]
    y_vals = [shot["y_dist"], shot["y_dist"]/2, 0]
    z_vals = [0, shot["z_peak"], 10]

    top_fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines',
                                 line=dict(color=color, width=3),
                                 showlegend=False))

    side_fig.add_trace(go.Scatter(x=y_vals, y=z_vals, mode='lines',
                                  line=dict(color=color, width=3),
                                  showlegend=False))

top_fig.update_layout(
    title="Top View",
    xaxis_title="Court Width (ft)",
    yaxis_title="Distance from Hoop (ft)",
    xaxis=dict(range=[-25, 25]),
    yaxis=dict(range=[-2, 50]),
    height=500
)

side_fig.update_layout(
    title="Side View",
    xaxis_title="Distance to Hoop (ft)",
    yaxis_title="Height (ft)",
    xaxis=dict(range=[-2, user_y_distance + 5]),
    yaxis=dict(range=[0, 12]),
    height=500
)

# Display plots side by side
col1, col2 = st.columns(2)
col1.plotly_chart(top_fig, use_container_width=True)
col2.plotly_chart(side_fig, use_container_width=True)

# -----------------------------
# Section 3: Notes
# -----------------------------
st.header("Notes")
st.markdown("""
- **Game Make:** 1 = point scored, 0 = miss.  
- **Color Fading:** newer shots = darker color.  
- **Future Work:** connect this with live tracking data and sensor inputs.  
- **Court Lines:** dynamically drawn to match real dimensions.  
""")
