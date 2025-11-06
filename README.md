🏀 Basketball Shot Tracker App

Team Name: HoopIQ
Developed by: Christopher Hong, Alfonso Mejia Vasquez, Gondra Kelly, Matthew Margulies, Carlos Orozco
Start Web Development: October 2025
Target Completion: June 2026
-----------------------------------------------------------------------------------------------------------
Overview

The Basketball Shot Tracker App allows users to log and analyze basketball shots with both technical feedback (Backboard, Rim, Net) and overall game make rates. Users can visualize ball trajectories, export data, and track progress over time.

The app is built with Streamlit, using Python for data handling, plotting, and authentication.
-----------------------------------------------------------------------------------------------------------
Features
🔹 Core Features
1. Shot Results Table: Displays Backboard, Rim, Net, and Game Make data.
2. Technical Component Averages: Shows average performance on each component.
3. Shot Selection: Users can select which shots to display, including buttons to:
    • Select All Shots
    • Clear All Shots
    • Show All Makes
    • Show All Misses
4. Ball Trajectory Plots:
    • Top View: Shows XY trajectory from above.
    • Side View: Shows distance and height of each shot.
5. Export Data: Users can export data in CSV, Excel, or JSON formats.

🔹 User Account Features
1. Login / Register: Users can create accounts and log in.
2. Sidebar Account Management:
    • Logout
    • Delete Account: Permanently removes the user. (Double-click may be needed due to Streamlit rerun behavior)
    • Change Password: Update your password. (Double-click may be needed)

Note: Double-click behavior is a known quirk of Streamlit buttons. Users may need to click twice for certain actions to take effect.
-----------------------------------------------------------------------------------------------------------
Installation

1. Clone the repository:

git clone https://github.com/chris02-skool/HoopIQ.git
cd basketball-shot-tracker

2. Create a Python virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

3. Install dependencies:

pip install -r requirements.txt

4. Run the app:

streamlit run app.py
-----------------------------------------------------------------------------------------------------------
Project Structure
basketball-shot-tracker/
│
├─ app.py                # Main Streamlit app
├─ data.py               # Placeholder shot data and averages
├─ plot_utils.py         # Functions for plotting top and side view
├─ shot_selection.py     # Shot selection UI
├─ export_utils.py       # Data export functions
├─ auth_ui.py            # Streamlit login/register and sidebar
├─ auth_utils.py         # Functions for login, register, delete, change password
├─ notes.py              # Notes and instructions shown in the app
├─ users.json            # User accounts (auto-generated)
├─ requirements.txt      # Python dependencies
└─ README.md             # This file
-----------------------------------------------------------------------------------------------------------
Future Improvements
    • Integrate real sensor data for shot results and trajectory.
    • Add heat map of shot locations.
    • Enable multi-user session management.
    • Allow users to compare multiple sessions and overlay shot trajectories.
    • Advanced technical feedback based on shot parameters.
    • Implement username confirmation (e.g., typing delete [username]) for account deletion.
-----------------------------------------------------------------------------------------------------------
Dependencies
    • Python 3.11+
    • Streamlit >=1.36.0
    • Plotly >=5.22.0
    • Pandas >=2.2.0
    • NumPy >=1.26.0
    • OpenPyXL >=3.1.3
-----------------------------------------------------------------------------------------------------------
Notes
    • Placeholder data is used for development. Replace with real input when available.
    • Buttons in Streamlit may require double-click due to UI rerun behavior.