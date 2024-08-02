import streamlit as st
import pandas as pd

from palmavillapp.components.data_pipelines.comparing_utils import compare_data
from palmavillapp.components.table_formatting.utils import highlight_rows

from palmavillapp.components.constants import FELHO_COLUMNS, BOOKING_COLUMNS


# Streamlit app
st.set_page_config(layout="wide")
st.title(
    "Check which accounts are missing from Felhomatrac that are present in Booking"
)

col1, col2 = st.columns(2)

with col1:
    uploaded_felho = st.file_uploader(
        "Upload Felhőmatrac Excel here", type=["xlsx", "xls"]
    )

with col2:
    uploaded_booking = st.file_uploader(
        "Upload Booking Excel here", type=["xlsx", "xls"]
    )

# Store the uploaded files in session state and display success message
if uploaded_felho is not None:
    st.session_state["uploaded_felho"] = uploaded_felho
    st.success("Felhőmatrac Excel file uploaded successfully!")

if uploaded_booking is not None:
    st.session_state["uploaded_booking"] = uploaded_booking
    st.success("Booking Excel file uploaded successfully!")

custom_css = """
<style>
table {
    font-size: 12px;
    width: 50%;
}
</style>
"""

if uploaded_felho is not None and uploaded_booking is not None:
    df_felho = pd.read_excel(uploaded_felho)
    df_booking = pd.read_excel(uploaded_booking)
    df_felho.columns = FELHO_COLUMNS
    df_booking.columns = BOOKING_COLUMNS
    df_booking["children"] = df_booking["children"].fillna(0).astype(int)
    df_booking["children_ages"] = df_booking["children_ages"].fillna("")

    df_result = compare_data(df_felho, df_booking)
    styled_df = df_result[
        [
            "full_name",
            "first_night",
            "last_night",
            "full_name_match",
            "has_name_overlap",
            "has_date_overlap",
            "number_of_guests",
            "children",
            "children_ages",
            "phone_number",
            "address",
            "colour_code",
            "colour_sort_key",
        ]
    ].style.apply(highlight_rows, axis=1)

    # Button to process and display the dataframe
    if st.button("Process and Display DataFrame"):
        # Legend
        st.markdown(
            """
        **Legend:**
        - <span style='background-color: #d4edda; color: black;'>Green</span>: Name and date match found.
        - <span style='background-color: #fff3cd; color: black;'>Yellow</span>: Date match found, name match not found. Possibly correct.
        - <span style='background-color: #f8d7da; color: black;'>Red</span>: Booking entry missing entirely from Felhőmatrac. Update accounts in Felhőmatrac.
        """,
            unsafe_allow_html=True,
        )

        st.dataframe(
            styled_df,
            hide_index=True,
            use_container_width=True,
            column_order=[
                "colour_code",
                "full_name",
                "first_night",
                "last_night",
                "full_name_match",
                # "colour_sort_key",
                # "has_name_overlap",
                # "has_date_overlap",
                "number_of_guests",
                "children",
                "children_ages",
                "phone_number",
                "address",
            ],
        )

        # Display the styled dataframe in a scrollable area
        # st.write(
        #     '<div style="overflow-x: auto">'
        #     + styled_df.to_html()
        #     + custom_css
        #     + "</div>",
        #     unsafe_allow_html=True,
        # )
else:
    st.write("Please upload both Excel files to proceed.")
