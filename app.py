# Basketball Shot Tracker App
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

# Placeholder data for testing
data = {
    "Backboard": [1, 0, 1, 1, 0],
    "Rim": [1, 0, 0, 1, 1],
    "Net": [0, 0, 1, 0, 1],
    "Game Make": [1, 0, 1, 1, 1]
}
df = pd.DataFrame(data)

component_avg = df[['Backboard', 'Rim', 'Net']].mean()
game_make_avg = df['Game Make'].mean()

st.dataframe(df)
st.markdown("**Technical Component Averages:**")
st.write(component_avg)
st.write(f"**Overall Game Make Rate:** {game_make_avg:.2f}")

# -----------------------------
# Section 2: Trajectory Plots
# -----------------------------
st.header("Ball Trajectory")

# User adjustable parameters
user_x_offset = st.slider("Adjust shooter horizontal position (ft)", -15, 15, 0)
user_y_distance = st.slider("Adjust shot distance from hoop (ft)", 10, 40, 20)
user_height = st.slider("Shooter release height (ft)", 5, 8, 6)

# Placeholder ball trajectory data
top_view_x = [user_x_offset, user_x_offset*0.7, user_x_offset*0.3, 0, 0]
top_view_y = [user_y_distance, 25, 10, 2, 1]

# -----------------------------
# Top View - Correct High School Court
# -----------------------------
top_fig = go.Figure()

# Court dimensions (ft)
court_width = 50
court_length = 47

# Court boundaries
top_fig.add_shape(
    type="rect",
    x0=-court_width/2,
    y0=0,
    x1=court_width/2,
    y1=court_length,
    line=dict(color="gray", width=2)
)

# Backboard and Rim
rim_y = 5.25  # Rim center 63 in (5.25 ft) from baseline
rim_x = 0

backboard_width = 6  # 72 in = 6 ft wide
backboard_y = rim_y - 0.5  # 0.5 ft in front of rim
top_fig.add_shape(
    type="line",
    x0=-backboard_width/2,
    y0=backboard_y,
    x1=backboard_width/2,
    y1=backboard_y,
    line=dict(color="black", width=3)
)

rim_diameter = 1.5  # 18 in = 1.5 ft
top_fig.add_shape(
    type="circle",
    x0=rim_x - rim_diameter/2,
    y0=rim_y - rim_diameter/2,
    x1=rim_x + rim_diameter/2,
    y1=rim_y + rim_diameter/2,
    line=dict(color="red", width=3)
)

# Key / Box (12 x 19 ft)
box_width = 12
box_length = 19
top_fig.add_shape(
    type="rect",
    x0=-box_width/2,
    y0=0,
    x1=box_width/2,
    y1=box_length,
    line=dict(color="orange", width=2)
)

# Free Throw Arc (radius 6 ft)
free_throw_line_y = 19  # Distance from baseline to free throw line
arc_radius = 6
theta = [i for i in range(0, 181)]
arc_x = [arc_radius * math.cos(math.radians(t)) for t in theta]
arc_y = [free_throw_line_y + arc_radius * math.sin(math.radians(t)) for t in theta]
top_fig.add_trace(go.Scatter(
    x=arc_x,
    y=arc_y,
    mode='lines',
    line=dict(color="orange")
))

# -----------------------------
# 3-Point Line (HS court)
# -----------------------------
radius_3pt = 19.75  # 3-point radius from rim
corner_distance = 5.25  # 63 in from sideline

# Left corner straight line
top_fig.add_shape(
    type="line",
    x0=-court_width/2 + corner_distance,
    y0=0,
    x1=-court_width/2 + corner_distance,
    y1=rim_y + math.sqrt(radius_3pt**2 - (court_width/2 - corner_distance)**2),
    line=dict(color="orange", width=2)
)

# Right corner straight line
top_fig.add_shape(
    type="line",
    x0=court_width/2 - corner_distance,
    y0=0,
    x1=court_width/2 - corner_distance,
    y1=rim_y + math.sqrt(radius_3pt**2 - (court_width/2 - corner_distance)**2),
    line=dict(color="orange", width=2)
)

# Arc part of 3-point line
theta_limit = math.degrees(math.acos((court_width/2 - corner_distance)/radius_3pt))
theta_3pt = [i for i in range(int(-theta_limit), int(theta_limit)+1)]
arc3_x = [rim_x + radius_3pt * math.cos(math.radians(t)) for t in theta_3pt]
arc3_y = [rim_y + radius_3pt * math.sin(math.radians(t)) for t in theta_3pt]
top_fig.add_trace(go.Scatter(
    x=arc3_x,
    y=arc3_y,
    mode='lines',
    line=dict(color="orange", width=2)
))

# -----------------------------
# Ball trajectory
# -----------------------------
top_fig.add_trace(go.Scatter(
    x=top_view_x,
    y=top_view_y,
    mode='lines+markers',
    line=dict(color="blue", width=3),
    marker=dict(size=8),
    name="Ball Trajectory"
))

# -----------------------------
# Layout
# -----------------------------
top_fig.update_layout(
    title="Top View of Ball Trajectory",
    xaxis=dict(range=[-court_width/2, court_width/2], scaleanchor="y", scaleratio=1),
    yaxis=dict(range=[-5, court_length+5]),
    height=500
)

# -----------------------------
# Side View - Placeholder
# -----------------------------
side_fig = go.Figure()
side_fig.add_trace(go.Scatter(
    x=[0, 10, 20, 30, 40],
    y=[user_height, 8, 9, 10, 10],
    mode='lines+markers',
    line=dict(color="blue", width=3),
    marker=dict(size=8),
    name="Ball Trajectory"
))
side_fig.update_layout(
    title="Side View (Placeholder)",
    xaxis_title="Distance from Shooter (ft)",
    yaxis_title="Height (ft)",
    xaxis=dict(range=[0, court_length]),
    yaxis=dict(range=[0, 12]),
    height=500
)

# -----------------------------
# Display side by side
# -----------------------------
col1, col2 = st.columns(2)
col1.plotly_chart(top_fig, use_container_width=True)
col2.plotly_chart(side_fig, use_container_width=True)

# -----------------------------
# Notes
# -----------------------------
st.header("Notes")
st.markdown("""
- `Backboard`, `Rim`, `Net` columns provide **technical feedback**.
- `Game Make` column shows if the shot **scores a point** in a real game.
- Replace placeholder data with actual sensor and camera inputs.
- Averages and plots update automatically after every new shot.
""")
