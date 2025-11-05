# Makes the court, and plot the trajectory of the shot

import plotly.graph_objects as go
import math
import numpy as np
import streamlit as st

def plot_top_view(shots, selected_idx):
    fig = go.Figure()
    court_width, court_length = 50, 47
    fig.add_shape(type="rect", x0=-court_width/2, y0=0, x1=court_width/2, y1=court_length,
                  line=dict(color="gray", width=2))
    rim_y, rim_x = 5.25, 0
    backboard_width = 6
    backboard_y = rim_y - 0.5
    fig.add_shape(type="line", x0=-backboard_width/2, y0=backboard_y, x1=backboard_width/2,
                  y1=backboard_y, line=dict(color="black", width=3))
    rim_diameter = 1.5
    fig.add_shape(type="circle", x0=rim_x-rim_diameter/2, y0=rim_y-rim_diameter/2,
                  x1=rim_x+rim_diameter/2, y1=rim_y+rim_diameter/2, line=dict(color="red", width=3))

    # Free throw arc
    theta = np.linspace(0, math.pi, 50)
    arc_radius = 6
    arc_x = arc_radius * np.cos(theta)
    arc_y = 19 + arc_radius * np.sin(theta)
    fig.add_trace(go.Scatter(x=arc_x, y=arc_y, mode='lines', line=dict(color="orange")))

    for i in selected_idx:
        shot = shots[i]
        color = "green" if shot['result']=="Make" else "red"
        fig.add_trace(go.Scatter(x=shot['top_x'], y=shot['top_y'],
                                 mode='lines+markers', line=dict(color=color, width=3),
                                 marker=dict(size=6),
                                 name=f"Shot {i+1} ({shot['result']})"))
    fig.update_layout(title="Top View of Ball Trajectory", xaxis=dict(range=[-25,25], scaleanchor="y", scaleratio=1),
                      yaxis=dict(range=[0,50]), height=500)
    st.plotly_chart(fig, use_container_width=True)

def plot_side_view(shots, selected_idx):
    fig = go.Figure()
    # Side view shapes here, simplified
    rim_height = 10
    backboard_x = 40
    backboard_bottom_y = rim_height - 3.5 + 2.5
    fig.add_shape(type="line", x0=backboard_x, y0=backboard_bottom_y, x1=backboard_x, y1=backboard_bottom_y+3.5,
                  line=dict(color="black", width=3))
    for i in selected_idx:
        shot = shots[i]
        color = "green" if shot['result']=="Make" else "red"
        fig.add_trace(go.Scatter(x=shot['side_x'], y=shot['side_y'],
                                 mode='lines+markers', line=dict(color=color, width=3),
                                 marker=dict(size=6),
                                 name=f"Shot {i+1} ({shot['result']})"))
    fig.update_layout(title="Side View of Ball Trajectory",
                      xaxis_title="Distance from Shooter (ft)", yaxis_title="Height (ft)",
                      xaxis=dict(range=[-5,45]), yaxis=dict(range=[0,15]), height=500)
    st.plotly_chart(fig, use_container_width=True)
