# Basketball Shot Tracker App
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math
import numpy as np
from io import BytesIO

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
df.index = df.index + 1 # Start index at 1 for shot number

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

shooter_x = 0  # directly behind free throw
shooter_y = 22  # approx 3-pt line behind free throw

# Placeholder trajectories (10 shots)
# Each shot: dict with 'top_x', 'top_y', 'side_x', 'side_y', 'result'
shots = [
    {'top_x':[0, 1, 0, 0], 'top_y':[shooter_y, 18, 12, 5.25], 'side_x':[0, 10, 20, 25], 'side_y':[6, 8, 9, 10], 'result':'Make'},
    {'top_x':[0, 2, 1, 0], 'top_y':[shooter_y, 17.5, 11, 5.25], 'side_x':[0, 10, 20, 25], 'side_y':[6, 8, 9, 10], 'result':'Make'},
    {'top_x':[0, 0, 0, 0], 'top_y':[shooter_y, 18, 12, 5.25], 'side_x':[0, 10, 20, 25], 'side_y':[6, 8, 9, 10], 'result':'Make'},
    {'top_x':[0, -2, -3, -3], 'top_y':[shooter_y, 17, 12, 6], 'side_x':[0, 10, 20, 25], 'side_y':[6, 9, 8, 4], 'result':'Miss'},
    {'top_x':[0, 1, 2, 3], 'top_y':[shooter_y, 18, 13, 7], 'side_x':[0, 10, 20, 25], 'side_y':[6, 9, 8, 5], 'result':'Miss'},
    {'top_x':[0, -1, -0.5, 0], 'top_y':[shooter_y, 19, 13, 5.25], 'side_x':[0, 10, 20, 25], 'side_y':[6, 8, 9, 10], 'result':'Make'},
    {'top_x':[0, -1, -2, -2.5], 'top_y':[shooter_y, 18, 13, 6], 'side_x':[0, 10, 20, 25], 'side_y':[6, 8, 8, 4], 'result':'Miss'},
    {'top_x':[0, -2, -1, 0], 'top_y':[shooter_y, 17, 10, 5.25], 'side_x':[0, 10, 20, 25], 'side_y':[6, 8, 9, 10], 'result':'Make'},
    {'top_x':[0, 2, 3, 3], 'top_y':[shooter_y, 19, 14, 6], 'side_x':[0, 10, 20, 25], 'side_y':[6, 8, 7, 4], 'result':'Miss'},
    {'top_x':[0, 0, 1, 2], 'top_y':[shooter_y, 18, 14, 6], 'side_x':[0, 10, 20, 25], 'side_y':[6, 8, 7, 4], 'result':'Miss'}
]

# LEFT PANEL: Scrollable checkbox list (aligned with plot height)
col_left, col_right = st.columns([1,3])  # Left for list, right for plots

with col_left:
    st.subheader("Shots List")

    # Scrollable area styling
    st.markdown("""
        <style>
        .scroll-box {
            height: 500px;  /* matches plot height */
            overflow-y: auto;
            border: 1px solid #bbb;
            border-radius: 8px;
            padding: 6px 10px;
            background-color: #f9f9f9;
        }
        .scroll-box::-webkit-scrollbar {
            width: 8px;
        }
        .scroll-box::-webkit-scrollbar-thumb {
            background: #ccc;
            border-radius: 4px;
        }
        </style>
        """, unsafe_allow_html=True)

    # Scrollable checkbox list
    selected_shots_idx = []
    st.markdown('<div class="scroll-box">', unsafe_allow_html=True)
    for i, shot in enumerate(shots):
        checked = st.checkbox(f"Shot {i+1} ({shot['result']})", value=True, key=f"shot_{i}")
        if checked:
            selected_shots_idx.append(i)
    st.markdown('</div>', unsafe_allow_html=True)

# Prepare plots
top_fig = go.Figure()
side_fig = go.Figure()

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

# -----------------------------
# Side View - Correct Backboard, Rim, Net
# -----------------------------
side_fig = go.Figure()

# Rim and court dimensions
floor_y = 0
rim_height = 10

# Backboard - vertical
backboard_height = 3.5
backboard_x = 40
backboard_bottom_y = rim_height - backboard_height+2.5
backboard_top_y = backboard_bottom_y + backboard_height

side_fig.add_shape(
    type="line",
    x0=backboard_x,
    y0=backboard_bottom_y,
    x1=backboard_x,
    y1=backboard_top_y,
    line=dict(color="black", width=3)
)

# Rim - horizontal line in front of backboard
rim_length = 1.5
rim_offset_from_backboard = 0.5
rim_x_left = backboard_x - rim_offset_from_backboard - rim_length/2
rim_x_right = backboard_x - rim_offset_from_backboard + rim_length/2
side_fig.add_shape(
    type="line",
    x0=rim_x_left,
    y0=rim_height,
    x1=rim_x_right,
    y1=rim_height,
    line=dict(color="red", width=3)
)

# Net - dotted trapezoid slightly in front of backboard
net_top_width = rim_length
net_bottom_width = 1
net_height = 1
net_offset = 0.2

net_top_left_x = rim_x_left - net_offset
net_top_right_x = rim_x_right - net_offset
net_bottom_left_x = net_top_left_x + (net_top_width - net_bottom_width)/2
net_bottom_right_x = net_top_right_x - (net_top_width - net_bottom_width)/2
net_bottom_y = rim_height - net_height

side_fig.add_shape(type="line", x0=net_top_left_x, y0=rim_height,
                   x1=net_bottom_left_x, y1=net_bottom_y,
                   line=dict(color="blue", width=2, dash='dot'))
side_fig.add_shape(type="line", x0=net_top_right_x, y0=rim_height,
                   x1=net_bottom_right_x, y1=net_bottom_y,
                   line=dict(color="blue", width=2, dash='dot'))
side_fig.add_shape(type="line", x0=net_bottom_left_x, y0=net_bottom_y,
                   x1=net_bottom_right_x, y1=net_bottom_y,
                   line=dict(color="blue", width=2, dash='dot'))

# Plot selected shots based on checkbox selection
for i in selected_shots_idx:
    shot = shots[i]
    color = "green" if shot['result']=="Make" else "red"
    top_fig.add_trace(go.Scatter(
        x=shot['top_x'],
        y=shot['top_y'],
        mode='lines+markers',
        line=dict(color=color, width=3),
        marker=dict(size=6),
        name=f"Shot {i+1} ({shot['result']})"
    ))
    side_fig.add_trace(go.Scatter(
        x=shot['side_x'],
        y=shot['side_y'],
        mode='lines+markers',
        line=dict(color=color, width=3),
        marker=dict(size=6),
        name=f"Shot {i+1} ({shot['result']})"
    ))

# Layout updates
top_fig.update_layout(
    title="Top View of Ball Trajectory",
    xaxis=dict(range=[-25, 25], scaleanchor="y", scaleratio=1),
    yaxis=dict(range=[0, 50]),
    height=500
)
side_fig.update_layout(
    title="Side View of Ball Trajectory",
    xaxis_title="Distance from Shooter (ft)",
    yaxis_title="Height (ft)",
    xaxis=dict(range=[-5, 45]),
    yaxis=dict(range=[0, 15]),
    height=500
)

# Display side by side
col1, col2 = st.columns(2)
col1.plotly_chart(top_fig, use_container_width=True)
col2.plotly_chart(side_fig, use_container_width=True)

# -----------------------------
# Section 3: EXPORT FUNCTIONALITY (MULTIPLE SELECTIONS)
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

# User selects which data to export (multiple)
export_options = st.multiselect(
    "Select Data to Export (multiple allowed):",
    ["Shot Data", "Component Averages", "Game Make Rate"],
    default=["Shot Data"]
)

export_format = st.selectbox(
    "Select Export Format:",
    ["CSV", "Excel", "JSON"]
)

if st.button("Export"):
    if export_format == "CSV":
        for option in export_options:
            if option == "Shot Data":
                data_to_export = shot_data
            elif option == "Component Averages":
                data_to_export = component_averages
            elif option == "Game Make Rate":
                data_to_export = game_make_rate

            csv = data_to_export.to_csv(index=False).encode("utf-8")
            st.download_button(
                label=f"Download {option} CSV",
                data=csv,
                file_name=f"{option.replace(' ', '_')}.csv",
                mime="text/csv"
            )

    elif export_format == "Excel":
        import io
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for option in export_options:
                if option == "Shot Data":
                    data_to_export = shot_data
                elif option == "Component Averages":
                    data_to_export = component_averages
                elif option == "Game Make Rate":
                    data_to_export = game_make_rate

                # Write each dataframe to a separate sheet
                sheet_name = option[:31]  # Excel sheet names max 31 chars
                data_to_export.to_excel(writer, index=False, sheet_name=sheet_name)
        output.seek(0)
        st.download_button(
            label="Download Excel",
            data=output,
            file_name="Basketball_Shot_Data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    elif export_format == "JSON":
        combined_json = {}
        for option in export_options:
            if option == "Shot Data":
                data_to_export = shot_data
            elif option == "Component Averages":
                data_to_export = component_averages
            elif option == "Game Make Rate":
                data_to_export = game_make_rate
            combined_json[option.replace(' ', '_')] = data_to_export.to_dict(orient="records")
        import json
        json_data = json.dumps(combined_json, indent=4)
        st.download_button(
            label="Download JSON",
            data=json_data,
            file_name="Basketball_Shot_Data.json",
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
#
# NOTES:
# - Next Step: Add real ball trajectory data when available.
# - Future: Let users export multiple datasets in one file.
# - A button to let the user scan their ball using the camera from tracking codes (will be at top).
# - Integrate real sensor data for shot results and trajectory.
# - Add check/tab/selection to show the which shot they want to see (latest, best, worst, custom)
# - Add a heat map of shot locations on the court to show how good you shot from a certain spot
# - Add sessions for when the user uses the app multiple times
# - Add user authentication for multiple users
# - Add ability to save and load shot data
# - Add 10 session limit, with the oldest 7 show averages and the latest 3 show individual shot data.
# - Add ability to compare multiple sessions (Bonus goal)
# - Add ability to overlay multiple shot trajectories for comparison (Should be implemented since plan was to show multiple shots in one court graph)
# - Add ability to adjust shot parameters (angle, speed) and see predicted trajectory
# - Add more detailed technical feedback based on shot data (if possible)
# - Data should add lines after every shot, so the user can see their progress over time