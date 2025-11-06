# Makes the court, and plot the trajectory of the shot

import plotly.graph_objects as go
import math
import numpy as np
import streamlit as st

def plot_top_view(shots, selected_idx):
    fig = go.Figure()

    # Draw court outline rim, and backboard
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
    
    # Key Box
    box_width = 12
    box_length = 19
    fig.add_shape(type="rect", x0=-box_width/2, y0=0, x1=box_width/2, y1=box_length,
                  line=dict(color="orange", width=2))

    # Free throw arc
    theta = np.linspace(0, math.pi, 50)
    arc_radius = 6
    arc_x = arc_radius * np.cos(theta)
    arc_y = 19 + arc_radius * np.sin(theta)
    fig.add_trace(go.Scatter(x=arc_x, y=arc_y, mode='lines', line=dict(color="orange")))

    # 3-point line
    radius_3pt = 19.75
    x_left = -(court_width/2 - 5.25)
    x_right = (court_width/2 - 5.25)
    theta_left = math.asin(x_left / radius_3pt)
    theta_right = math.asin(x_right / radius_3pt)
    theta_vals = np.linspace(theta_left, theta_right, 100)
    arc3_x = rim_x + radius_3pt * np.sin(theta_vals)
    arc3_y = rim_y + radius_3pt * np.cos(theta_vals)
    fig.add_trace(go.Scatter(x=arc3_x, y=arc3_y, mode='lines', line=dict(color="orange", width=2)))

    # 3-Point Corner Lines
    corner_distance = 5.25
    x_left_corner = -court_width/2 + corner_distance
    y_left_top = rim_y + math.sqrt(radius_3pt**2 - (x_left_corner - rim_x)**2)
    fig.add_shape(type="line", x0=x_left_corner, y0=0, x1=x_left_corner, y1=y_left_top,
                  line=dict(color="orange", width=2))
    x_right_corner = court_width/2 - corner_distance
    y_right_top = rim_y + math.sqrt(radius_3pt**2 - (x_right_corner - rim_x)**2)
    fig.add_shape(type="line", x0=x_right_corner, y0=0, x1=x_right_corner, y1=y_right_top,
                  line=dict(color="orange", width=2))

    # Plot selected shot
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

    # Side view backboard
    rim_height = 10
    backboard_height = 3.5
    backboard_x = 40
    backboard_bottom_y = rim_height - backboard_height + 2.5
    backboard_top_y = backboard_bottom_y + backboard_height

    fig.add_shape(type="line", x0=backboard_x, y0=backboard_bottom_y,
                   x1=backboard_x, y1=backboard_top_y, line=dict(color="black", width=3))

    # Rim
    rim_length = 1.5
    rim_offset_from_backboard = -0.5
    rim_x_left = backboard_x - rim_offset_from_backboard - rim_length/2
    rim_x_right = backboard_x - rim_offset_from_backboard + rim_length/2
    fig.add_shape(type="line", x0=rim_x_left, y0=rim_height,
                       x1=rim_x_right, y1=rim_height, line=dict(color="red", width=3))

    # Net
    net_top_width = rim_length
    net_bottom_width = 1
    net_height = 1
    net_offset = 0.2
    net_top_left_x = rim_x_left - net_offset
    net_top_right_x = rim_x_right - net_offset
    net_bottom_left_x = net_top_left_x + (net_top_width - net_bottom_width)/2
    net_bottom_right_x = net_top_right_x - (net_top_width - net_bottom_width)/2
    net_bottom_y = rim_height - net_height

    fig.add_shape(type="line", x0=net_top_left_x, y0=rim_height,
                   x1=net_bottom_left_x, y1=net_bottom_y, line=dict(color="blue", width=2, dash='dot'))
    fig.add_shape(type="line", x0=net_top_right_x, y0=rim_height,
                   x1=net_bottom_right_x, y1=net_bottom_y, line=dict(color="blue", width=2, dash='dot'))
    fig.add_shape(type="line", x0=net_bottom_left_x, y0=net_bottom_y,
                   x1=net_bottom_right_x, y1=net_bottom_y, line=dict(color="blue", width=2, dash='dot'))

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
