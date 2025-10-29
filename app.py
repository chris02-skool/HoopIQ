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

# Placeholder data: 1 = hit, 0 = miss, Game Make = 1 if scores
data = {
    "Backboard": [1, 0, 1, 1, 0],
    "Rim": [1, 0, 0, 1, 1],
    "Net": [0, 0, 1, 0, 1],
    "Game Make": [1, 0, 1, 1, 1]
}
df = pd.DataFrame(data)

# Calculate averages
component_avg = df[['Backboard', 'Rim', 'Net']].mean()
game_make_avg = df['Game Make'].mean()

# Display table and averages
st.dataframe(df)
st.markdown("**Technical Component Averages:**")
st.write(component_avg)
st.write(f"**Overall Game Make Rate:** {game_make_avg:.2f}")

# -----------------------------
# Section 2: Trajectory Plots
# -----------------------------
st.header("Ball Trajectory")

# Shooter position sliders
user_x_offset = st.slider("Adjust shooter horizontal position (ft)", -15, 15, 0)
user_y_distance = st.slider("Adjust shot distance from hoop (ft)", 10, 40, 20)
user_height = st.slider("Shooter release height (ft)", 5, 8, 6)

# Example placeholder trajectories
top_view_x = [user_x_offset, user_x_offset*0.7, user_x_offset*0.3, 0, 0]
top_view_y = [user_y_distance, 15, 8, 2, 0]
side_view_x = [user_y_distance, 15, 8, 2, 0]
side_view_z = [user_height, 8, 9, 10, 10]

# -----------------------------
# Top View - Park Court
# -----------------------------
top_fig = go.Figure()

# Half-court rectangle
top_fig.add_shape(type="rect", x0=-25, y0=0, x1=25, y1=47,
                  line=dict(color="gray", width=2))

# Key
top_fig.add_shape(type="rect", x0=-8, y0=0, x1=8, y1=19,
                  line=dict(color="orange", width=2))

# Free throw arc (6 ft radius)
theta = [i for i in range(0, 181)]
circle_x = [6 * math.cos(math.radians(t)) for t in theta]
circle_y = [19 + 6 * math.sin(math.radians(t)) for t in theta]
top_fig.add_trace(go.Scatter(x=circle_x, y=circle_y, mode='lines', line=dict(color="orange")))

# 3-point arc (23.75 ft radius, clipped to park court)
theta_limit = math.degrees(math.acos(22/23.75))
theta = [i for i in range(int(-theta_limit), int(theta_limit)+1)]
arc_x = [23.75 * math.cos(math.radians(t)) for t in theta]
arc_y = [23.75 * math.sin(math.radians(t)) for t in theta]
top_fig.add_trace(go.Scatter(x=arc_x, y=arc_y, mode='lines', line=dict(color="orange")))

# Rim at (0,0)
top_fig.add_shape(type="circle", x0=-0.75, y0=-0.75, x1=0.75, y1=0.75,
                  line=dict(color="red", width=3))

# Backboard
top_fig.add_shape(type="line", x0=-3, y0=-1, x1=3, y1=-1,
                  line=dict(color="black", width=3))

# Ball trajectory
top_fig.add_trace(go.Scatter(
    x=top_view_x,
    y=top_view_y,
    mode='lines+markers',
    line=dict(color="blue", width=3),
    marker=dict(size=8),
    name="Ball Trajectory"
))

top_fig.update_layout(
    title="Top View of Ball Trajectory",
    xaxis_title="Court Width (ft)",
    yaxis_title="Distance from Hoop (ft)",
    xaxis=dict(range=[-25, 25]),
    yaxis=dict(range=[-5, 50]),
    height=500
)

# -----------------------------
# Side View - Backboard, Rim, Net
# -----------------------------
side_fig = go.Figure()

# Floor
side_fig.add_shape(type="line", x0=0, y0=0, x1=45, y1=0,
                   line=dict(color="brown", width=3))

# Backboard (on right)
backboard_bottom = 6.5
backboard_top = 10
backboard_x0 = 0
backboard_x1 = 0.5
side_fig.add_shape(type="rect",
                   x0=backboard_x0, y0=backboard_bottom,
                   x1=backboard_x1, y1=backboard_top,
                   line=dict(color="black", width=2),
                   fillcolor="lightgray")

# Rim as horizontal line
rim_y = 10
rim_length = 1.5
side_fig.add_shape(type="line",
                   x0=backboard_x0 - rim_length, y0=rim_y,
                   x1=backboard_x0, y1=rim_y,
                   line=dict(color="red", width=3))

# Net as vertical dashed line
side_fig.add_shape(type="line",
                   x0=backboard_x0 - rim_length/2, y0=rim_y,
                   x1=backboard_x0 - rim_length/2, y1=rim_y - 1,
                   line=dict(color="blue", width=2, dash="dot"))

# Ball trajectory
side_fig.add_trace(go.Scatter(
    x=side_view_x,
    y=side_view_z,
    mode='lines+markers',
    line=dict(color="blue", width=3),
    marker=dict(size=8),
    name="Ball Trajectory"
))

side_fig.update_layout(
    title="Side View of Ball Trajectory",
    xaxis_title="Distance from Shooter (ft)",
    yaxis_title="Height (ft)",
    xaxis=dict(range=[-2, 45]),
    yaxis=dict(range=[0, 12]),
    height=500
)

# Display both views side by side
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
