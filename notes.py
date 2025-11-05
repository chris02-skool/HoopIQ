# Just showing notes

import streamlit as st

def show_notes():
    st.header("Notes")
    st.markdown("""
    - `Backboard`, `Rim`, `Net` columns provide **technical feedback**.
    - `Game Make` column shows if the shot **scores a point** in a real game.
    - Replace placeholder data with actual sensor and camera inputs.
    - Averages and plots update automatically after every new shot.
    """)
