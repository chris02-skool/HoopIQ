# Basketball Shot Tracker App
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math
import numpy as np

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
# Top View - Correct High School Court with 3-point arc and corner lines
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
rim_y = 5.25
rim_x = 0
backboard_width = 6
backboard_y = rim_y - 0.5
top_fig.add_shape(
    type="line",
    x0=-backboard_width/2,
    y0=backboard_y,
    x1=backboard_width/2,
    y1=backboard_y,
    line=dict(color="black", width=3)
)

rim_diameter = 1.5
top_fig.add_shape(
    type="circle",
    x0=rim_x - rim_diameter/2,
    y0=rim_y - rim_diameter/2,
    x1=rim_x + rim_diameter/2,
    y1=rim_y + rim_diameter/2,
    line=dict(color="red", width=3)
)

# Key / Box
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

# Free Throw Arc
free_throw_line_y = 19
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

# 3-Point Arc
radius_3pt = 19.75
x_left = - (court_width/2 - 5.25)
x_right = (court_width/2 - 5.25)
theta_left = math.asin(x_left / radius_3pt)
theta_right = math.asin(x_right / radius_3pt)
theta_vals = np.linspace(theta_left, theta_right, 100)
arc3_x = rim_x + radius_3pt * np.sin(theta_vals)
arc3_y = rim_y + radius_3pt * np.cos(theta_vals)
top_fig.add_trace(go.Scatter(
    x=arc3_x,
    y=arc3_y,
    mode='lines',
    line=dict(color="orange", width=2)
))

# 3-Point Corner Lines
corner_distance = 5.25
x_left_corner = -court_width/2 + corner_distance
y_left_top = rim_y + math.sqrt(radius_3pt**2 - (x_left_corner - rim_x)**2)
top_fig.add_shape(
    type="line",
    x0=x_left_corner,
    y0=0,
    x1=x_left_corner,
    y1=y_left_top,
    line=dict(color="orange", width=2)
)
x_right_corner = court_width/2 - corner_distance
y_right_top = rim_y + math.sqrt(radius_3pt**2 - (x_right_corner - rim_x)**2)
top_fig.add_shape(
    type="line",
    x0=x_right_corner,
    y0=0,
    x1=x_right_corner,
    y1=y_right_top,
    line=dict(color="orange", width=2)
)

# Ball trajectory (placeholder)
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
    xaxis=dict(range=[-court_width/2, court_width/2], scaleanchor="y", scaleratio=1),
    yaxis=dict(range=[-5, court_length+5]),
    height=500
)

# -----------------------------
# Side View - High School Rim & Backboard
# -----------------------------
side_fig = go.Figure()

floor_y = 0
rim_height = 10

backboard_width = 6
backboard_bottom_y = rim_height - 3.5
backboard_top_y = rim_height + 1.5
backboard_x = 40

side_fig.add_shape(
    type="line",
    x0=backboard_x,
    y0=backboard_bottom_y,
    x1=backboard_x,
    y1=backboard_top_y,
    line=dict(color="black", width=3)
)

rim_radius = 0.75
side_fig.add_shape(
    type="circle",
    x0=-rim_radius,
    y0=rim_height - rim_radius,
    x1=rim_radius,
    y1=rim_height + rim_radius,
    line=dict(color="red", width=3)
)

net_radius = 0.5
side_fig.add_shape(
    type="circle",
    x0=-net_radius,
    y0=rim_height - net_radius,
    x1=net_radius,
    y1=rim_height,
    line=dict(color="blue", width=2, dash="dot")
)

# Placeholder ball trajectory
side_fig.add_trace(go.Scatter(
    x=[0, 10, 20, 30, 40],
    y=[6, 8, 9, 10, 10],
    mode='lines+markers',
    line=dict(color="blue", width=3),
    marker=dict(size=8),
    name="Ball Trajectory"
))

side_fig.update_layout(
    title="Side View of Ball Trajectory",
    xaxis_title="Distance from Shooter (ft)",
    yaxis_title="Height (ft)",
    xaxis=dict(range=[-5, 40]),
    yaxis=dict(range=[0, 15]),
    height=500
)

# Display side by side
col1, col2 = st.columns(2)
col1.plotly_chart(top_fig, use_container_width=True)
col2.plotly_chart(side_fig, use_container_width=True)

# -----------------------------
# 3️⃣ EXPORT FUNCTIONALITY
# -----------------------------
st.header("Export Data")

# Example placeholders
shot_data = df.copy()
component_averages = pd.DataFrame(component_avg).reset_index()
component_averages.columns = ["Component", "Average"]
game_make_rate = pd.DataFrame({
    "Total Shots": [len(df)],
    "Makes": [df['Game Make'].sum()],
    "Misses": [len(df) - df['Game Make'].sum()],
    "Make %": [df['Game Make'].mean() * 100]
})

# User selects which data to export
export_option = st.selectbox(
    "Select Data to Export:",
    ["Shot Data", "Component Averages", "Game Make Rate"]
)

export_format = st.selectbox(
    "Select Export Format:",
    ["CSV", "Excel", "JSON"]
)

if export_option == "Shot Data":
    data_to_export = shot_data
elif export_option == "Component Averages":
    data_to_export = component_averages
else:
    data_to_export = game_make_rate

if st.button("Export"):
    if export_format == "CSV":
        csv = data_to_export.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{export_option.replace(' ', '_')}.csv",
            mime="text/csv"
        )
    elif export_format == "Excel":
        with pd.ExcelWriter(f"{export_option.replace(' ', '_')}.xlsx", engine="openpyxl") as writer:
            data_to_export.to_excel(writer, index=False)
        with open(f"{export_option.replace(' ', '_')}.xlsx", "rb") as f:
            st.download_button(
                label="Download Excel",
                data=f,
                file_name=f"{export_option.replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    elif export_format == "JSON":
        json_data = data_to_export.to_json(orient="records", indent=4)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name=f"{export_option.replace(' ', '_')}.json",
            mime="application/json"
        )

# -----------------------------
# NOTES
# -----------------------------
st.header("Notes")
st.markdown("""
- `Backboard`, `Rim`, `Net` columns provide **technical feedback**.
- `Game Make` column shows if the shot **scores a point** in a real game.
- Replace placeholder data with actual sensor and camera inputs.
- Averages and plots update automatically after every new shot.
""")


# --------------------------------------
# 📝 Dev Notes
# --------------------------------------
"""
NOTES:
- Adjusted free throw circle y-position to 19 for realism.
- 3-point arc now displays correctly with tangent corner lines.
- Backboard made vertical on the right side.
- Rim is now properly horizontal and layered over the net.
- Net is a dotted trapezoid offset from the backboard.
- Next Step: Add real ball trajectory data when available.
- Future: Let users export additional data (e.g., trajectory stats).
"""
