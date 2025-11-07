# Export the data to any file the user requests

import streamlit as st
import pandas as pd
import io
import json

def export_section(df, component_avg):
    shot_data = df.copy()
    component_averages = pd.DataFrame(component_avg).reset_index()
    component_averages.columns = ["Component", "Average"]
    game_make_rate = pd.DataFrame({
        "Total Shots": [len(df)],
        "Makes": [df['Game Make'].sum()],
        "Misses": [len(df) - df['Game Make'].sum()],
        "Make %": [df['Game Make'].mean() * 100]
    })

    export_options = st.multiselect(
        "Select Data to Export (multiple allowed):",
        ["Shot Data", "Component Averages", "Game Make Rate"],
        default=["Shot Data"]
    )

    export_format = st.selectbox("Select Export Format:", ["Excel", "CSV", "JSON"])

    if st.button("Export"):
        if export_format == "CSV":
            for option in export_options:
                if option=="Shot Data": data_to_export = shot_data
                elif option=="Component Averages": data_to_export = component_averages
                elif option=="Game Make Rate": data_to_export = game_make_rate
                csv = data_to_export.to_csv(index=False).encode("utf-8")
                st.download_button(label=f"Download {option} CSV", data=csv,
                                   file_name=f"{option.replace(' ','_')}.csv", mime="text/csv")
        elif export_format=="Excel":
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                for option in export_options:
                    if option=="Shot Data": data_to_export = shot_data
                    elif option=="Component Averages": data_to_export = component_averages
                    elif option=="Game Make Rate": data_to_export = game_make_rate
                    sheet_name = option[:31]
                    data_to_export.to_excel(writer, index=False, sheet_name=sheet_name)
            output.seek(0)
            st.download_button(label="Download Excel", data=output,
                               file_name="Basketball_Shot_Data.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        elif export_format=="JSON":
            combined_json = {}
            for option in export_options:
                if option=="Shot Data": data_to_export = shot_data
                elif option=="Component Averages": data_to_export = component_averages
                elif option=="Game Make Rate": data_to_export = game_make_rate
                combined_json[option.replace(' ','_')] = data_to_export.to_dict(orient="records")
            json_data = json.dumps(combined_json, indent=4)
            st.download_button(label="Download JSON", data=json_data,
                               file_name="Basketball_Shot_Data.json", mime="application/json")
