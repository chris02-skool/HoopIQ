import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title="Basketball Shot Analytics", layout="wide")

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("🏀 Basketball Shot Analytics")

# User options for data export
export_option = st.sidebar.selectbox(
    "Select Data to Export:",
    [
        "Shot Data",
        "Component Averages",
        "Game Make Rate"
    ]
)

export_format = st.sidebar.selectbox(
    "Select Export Format:",
    ["CSV", "Excel", "JSON"]
)

# -------------------------------
# MAIN LAYOUT
# -------------------------------
st.title("🏀 Basketball Shot Visualizer")

tab1, tab2 = st.tabs(["Top View", "Side View"])

# --------------------------------------
# 1️⃣ TOP VIEW (Court Layout + 3PT Arc)
# --------------------------------------
with tab1:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 25)

    # Outer boundary lines
    court_outline = plt.Rectangle((0, 0), 50, 25, fill=False, color="black", lw=2)
    ax.add_patch(court_outline)

    # Paint area (key)
    paint = plt.Rectangle((19, 8), 12, 9, fill=False, color="orange", lw=2)
    ax.add_patch(paint)

    # Free throw circle (adjusted)
    free_throw_center_x, free_throw_center_y = 25, 19  # <-- Adjusted from before
    free_throw_circle = plt.Circle(
        (free_throw_center_x, free_throw_center_y), 6, fill=False, color="orange", lw=2
    )
    ax.add_patch(free_throw_circle)

    # Backboard + rim
    backboard = plt.Line2D([24, 26], [4, 4], color="black", lw=3)
    ax.add_line(backboard)

    rim = plt.Circle((25, 4.75), 0.75, fill=False, color="red", lw=3)
    ax.add_patch(rim)

    # 3-Point Arc and side lines
    three_point_center = (25, 4)
    three_point_radius = 23.75 / 12  # 23'9" in feet -> inches to feet simplified
    three_point_radius = 23.75  # feet
    theta = np.linspace(np.pi / 8, np.pi - np.pi / 8, 200)
    x_arc = three_point_center[0] + three_point_radius * np.cos(theta)
    y_arc = three_point_center[1] + three_point_radius * np.sin(theta)
    ax.plot(x_arc, y_arc, color="blue", lw=2)

    # Tangent straight lines
    ax.plot([3, 3], [0, 8], color="blue", lw=2)
    ax.plot([47, 47], [0, 8], color="blue", lw=2)

    # Placeholder ball trajectory (will replace later)
    x_traj = np.linspace(25, 25, 10)
    y_traj = np.linspace(4.75, 20, 10)
    ax.plot(x_traj, y_traj, "o--", color="gray", label="Ball Trajectory (placeholder)")

    ax.set_aspect("equal")
    ax.axis("off")
    ax.legend()
    st.pyplot(fig)

# --------------------------------------
# 2️⃣ SIDE VIEW (Backboard, Rim, Net)
# --------------------------------------
with tab2:
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.set_xlim(0, 30)
    ax2.set_ylim(0, 15)

    # Court baseline
    ax2.plot([0, 30], [0, 0], color="black", lw=3)

    # Backboard (vertical)
    backboard_x = 25
    backboard_bottom = 9
    backboard_top = 13
    ax2.plot([backboard_x, backboard_x], [backboard_bottom, backboard_top], color="black", lw=4)

    # Rim (horizontal, slightly in front of backboard)
    rim_front = backboard_x - 1.5
    rim_back = backboard_x
    rim_height = 10
    ax2.plot([rim_front, rim_back], [rim_height, rim_height], color="red", lw=4, zorder=3)

    # Net (dotted trapezoid)
    net_bottom_y = 8.5
    net_x_left = rim_front
    net_x_right = rim_back
    ax2.plot(
        [net_x_left, net_x_right],
        [rim_height, rim_height],
        color="red",
        lw=3,
        zorder=3,
    )
    ax2.plot(
        [net_x_left, net_x_left + 0.4],
        [rim_height, net_bottom_y],
        linestyle="dotted",
        color="blue",
        lw=2,
        zorder=2,
    )
    ax2.plot(
        [net_x_right, net_x_right - 0.4],
        [rim_height, net_bottom_y],
        linestyle="dotted",
        color="blue",
        lw=2,
        zorder=2,
    )
    ax2.plot(
        [net_x_left + 0.4, net_x_right - 0.4],
        [net_bottom_y, net_bottom_y],
        linestyle="dotted",
        color="blue",
        lw=2,
        zorder=2,
    )

    # Labels
    ax2.text(15, 14, "Side View", fontsize=14, fontweight="bold")
    ax2.axis("off")
    st.pyplot(fig2)

# --------------------------------------
# 3️⃣ EXPORT FUNCTIONALITY
# --------------------------------------
# Example dummy data (replace with actual data later)
shot_data = pd.DataFrame({
    "Shot #": [1, 2, 3, 4],
    "Make/Miss": ["Make", "Miss", "Make", "Miss"],
    "X_Pos": [23, 26, 24, 27],
    "Y_Pos": [10, 12, 14, 11]
})

component_averages = pd.DataFrame({
    "Component": ["Arc Height", "Release Angle", "Shot Speed"],
    "Average": [45.2, 51.8, 23.5]
})

game_make_rate = pd.DataFrame({
    "Total Shots": [4],
    "Makes": [2],
    "Misses": [2],
    "Make %": [50.0]
})

# Export logic
if export_option == "Shot Data":
    data_to_export = shot_data
elif export_option == "Component Averages":
    data_to_export = component_averages
else:
    data_to_export = game_make_rate

# Export button
if st.sidebar.button("Export Data"):
    if export_format == "CSV":
        csv = data_to_export.to_csv(index=False).encode("utf-8")
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{export_option.replace(' ', '_')}.csv",
            mime="text/csv"
        )

    elif export_format == "Excel":
        excel_buffer = pd.ExcelWriter(f"{export_option.replace(' ', '_')}.xlsx", engine="openpyxl")
        data_to_export.to_excel(excel_buffer, index=False)
        excel_buffer.close()
        with open(f"{export_option.replace(' ', '_')}.xlsx", "rb") as f:
            st.sidebar.download_button(
                label="Download Excel",
                data=f,
                file_name=f"{export_option.replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    elif export_format == "JSON":
        json_data = data_to_export.to_json(orient="records", indent=4)
        st.sidebar.download_button(
            label="Download JSON",
            data=json_data,
            file_name=f"{export_option.replace(' ', '_')}.json",
            mime="application/json"
        )

# --------------------------------------
# 📝 YOUR NOTES SECTION (untouched)
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
