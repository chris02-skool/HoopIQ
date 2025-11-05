# Shot Selection where user can select which shots to include in the analysis

import streamlit as st

def selected_shots_idx(shots):
    shot_labels = [f"Shot {i+1} ({s['result']})" for i, s in enumerate(shots)]
    if 'selected_shots' not in st.session_state:
        st.session_state.selected_shots = shot_labels.copy()

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Select All Shots"):
            st.session_state.selected_shots = shot_labels.copy()
    with col2:
        if st.button("Clear All Shots"):
            st.session_state.selected_shots = []

    st.session_state.selected_shots = st.multiselect(
        "Choose which shots to display:",
        options=shot_labels,
        default=st.session_state.selected_shots
    )

    return [shot_labels.index(s) for s in st.session_state.selected_shots]