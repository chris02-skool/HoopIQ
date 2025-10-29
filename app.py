# This code is to create an app that tracks basketball player shots using Streamlit

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math

st.set_page_config(page_title="Basketball Shot Tracker", layout="wide")
st.title("🏀 Basketball Shot Tracker")

# -----------------------------
# Section 1: Shot Results Table
# -----------------------------
st.header("Shot Results")

# Placeholder shot data (replace with your sensor/backboard input)
# 1 = hit / 0 = miss for technical components
data = {
    "Backboard": [1, 0, 1, 1, 0],
    "Rim": [1, 0, 0, 1, 1],
    "Net": [0, 0, 1, 0, 1],
    # Game Make = 1 if the shot scores a point, 0 if missed
    "Game Make": [1, 0, 1, 1, 1]
}

df = pd.DataFrame(data)

# Calculate averages
component_avg = df[['Backboard', 'Rim', 'Net']].mean()
game_make_avg = df['Game Make'].mean()

# Display the table
st.dataframe(df)

# Display component averages
st.markdown("**Technical Component Averages:**")
st.write(component_avg)

# Display overall Game Make rate clearly
st.write(f"**Overall Game Make Rate:** {game_make_avg:.2f}")

# -----------------------------
# Section 2: Trajectory Plots
# -----------------------------
st.header("Ball Trajectory")

# Example: user starts from x=5 ft left/right, y=20 ft from hoop
# (You’ll eventually get these from your camera/sensor)
user_x_offset = st.slider("Adjust shooter horizontal position (ft)", -15, 15, 0)
user_y_distance = st.slider("Adjust shot distance from hoop (ft)", 10, 40, 20)

# Example ball trajectory data
# Top view (x = left/right on court, y = distance toward hoop)
top_view_x = [user_x_offset, user_x_offset * 0.7, user_x_offset * 0.3, 0, 0]
top_view_y = [user_y_distance, 15, 8, 2, 0]

# Side view (x = distance to hoop, z = height)
side_view_x = [user_y_distance, 15, 8, 2, 0]
side_view_z = [0, 5, 9, 10, 10]  # height in feet

# -----------------------------
# Top View with Court Lines
# -----------------------------
top_fig = go.Figure()

# Half-court rectangle
top_fig.add_shape(type="rect", x0=-25, y0=0, x1=25, y1=47,
                  line=dict(color="gray", width=2))

# Key (painted area)
top_fig.add_shape(type="rect", x0=-8, y0=0, x1=8, y1=19,
                  line=dict(color="orange", width=2))

# 3-point arc
theta = [i for i in range(-90, 91)]
arc_x = [23.75 * (math.cos(t * math.pi / 180)) for t in theta]
arc_y = [23.75 * (math.sin(t * math.pi / 180)) for t in theta]
top_fig.add_trace(go.Scatter(x=arc_x, y=arc_y, mode='lines', line=dict(color="orange")))

# Hoop at (0, 0)
top_fig.add_shape(type="circle", x0=-0.75, y0=-0.75, x1=0.75, y1=0.75,
                  line=dict(color="red", width=3))

# Ball trajectory
top_fig.add_trace(go.Scatter(
    x=top_view_x,
    y=top_view_y,
    mode='lines+markers',
    name='Ball Trajectory',
    line=dict(color="blue", width=3),
    marker=dict(size=8)
))

top_fig.update_layout(
    title="Top View of Ball Trajectory",
    xaxis_title="Court Width (ft)",
    yaxis_title="Distance from Hoop (ft)",
    xaxis=dict(range=[-25, 25]),
    yaxis=dict(range=[-2, 50]),
    height=500
)

# -----------------------------
# Side View with Hoop & Backboard
# -----------------------------
side_fig = go.Figure()

# Ground line
side_fig.add_shape(type="line", x0=0, y0=0, x1=user_y_distance + 5, y1=0,
                   line=dict(color="brown", width=3))

# Backboard
side_fig.add_shape(type="rect", x0=-1, y0=3.5, x1=0, y1=10.5,
                   line=dict(color="black", width=2), fillcolor="lightgray")

# Rim (10 ft high, 18 in = 1.5 ft diameter)
side_fig.add_shape(type="circle", x0=-0.75, y0=9.25, x1=0.75, y1=10.75,
                   line=dict(color="red", width=3))

# Ball trajectory
side_fig.add_trace(go.Scatter(
    x=side_view_x,
    y=side_view_z,
    mode='lines+markers',
    name='Ball Trajectory',
    line=dict(color="blue", width=3),
    marker=dict(size=8)
))

side_fig.update_layout(
    title="Side View of Ball Trajectory",
    xaxis_title="Distance from Hoop (ft)",
    yaxis_title="Height (ft)",
    xaxis=dict(range=[-2, user_y_distance + 5]),
    yaxis=dict(range=[0, 12]),
    height=500
)

# Display side by side
col1, col2 = st.columns(2)
col1.plotly_chart(top_fig, use_container_width=True)
col2.plotly_chart(side_fig, use_container_width=True)


# -----------------------------
# Section 3: Notes / Future Inputs
# -----------------------------
st.header("Notes")
st.markdown("""
- `Backboard`, `Rim`, `Net` columns provide **technical feedback**.
- `Game Make` column shows if the shot **scores a point** in a real game.
- Replace placeholder data with actual sensor and camera inputs.
- Averages and plots update automatically after every new shot.
""")
