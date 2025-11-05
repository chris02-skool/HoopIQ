# Data placeholder file

import pandas as pd

# Placeholder data
data = {
    "Backboard": [1, 0, 1, 1, 0],
    "Rim": [1, 0, 0, 1, 1],
    "Net": [0, 0, 1, 0, 1],
    "Game Make": [1, 0, 1, 1, 1]
}
df = pd.DataFrame(data)
df.index = df.index + 1  # Start index at 1

component_avg = df[["Backboard", "Rim", "Net"]].mean()
game_make_avg = df["Game Make"].mean()

# Placeholder shot trajectories
shots = [ 
     {'top_x':[0, 1, 0, 0], 'top_y':[22, 18, 12, 5.25], 'side_x':[0,10,20,25], 'side_y':[6,8,9,10], 'result':'Make'},
    {'top_x':[0, 2, 1, 0], 'top_y':[22,17.5,11,5.25], 'side_x':[0,10,20,25], 'side_y':[6,8,9,10], 'result':'Make'},
    {'top_x':[0, 0, 0, 0], 'top_y':[22,18,12,5.25], 'side_x':[0,10,20,25], 'side_y':[6,8,9,10], 'result':'Make'},
    {'top_x':[0, -2, -3, -3], 'top_y':[22,17,12,6], 'side_x':[0,10,20,25], 'side_y':[6,9,8,4], 'result':'Miss'},
    {'top_x':[0, 1, 2, 3], 'top_y':[22,18,13,7], 'side_x':[0,10,20,25], 'side_y':[6,9,8,5], 'result':'Miss'},
    {'top_x':[0, -1, -0.5, 0], 'top_y':[22,19,13,5.25], 'side_x':[0,10,20,25], 'side_y':[6,8,9,10], 'result':'Make'},
    {'top_x':[0, -1, -2, -2.5], 'top_y':[22,18,13,6], 'side_x':[0,10,20,25], 'side_y':[6,8,8,4], 'result':'Miss'},
    {'top_x':[0, -2, -1, 0], 'top_y':[22,17,10,5.25], 'side_x':[0,10,20,25], 'side_y':[6,8,9,10], 'result':'Make'},
    {'top_x':[0, 2, 3, 3], 'top_y':[22,19,14,6], 'side_x':[0,10,20,25], 'side_y':[6,8,7,4], 'result':'Miss'},
    {'top_x':[0, 0, 1, 2], 'top_y':[22,18,14,6], 'side_x':[0,10,20,25], 'side_y':[6,8,7,4], 'result':'Miss'}
]