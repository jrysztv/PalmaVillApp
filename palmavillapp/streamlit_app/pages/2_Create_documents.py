from io import BytesIO
import zipfile
import streamlit as st
import pandas as pd

from palmavillapp.components.constants import FELHO_COLUMNS
from palmavillapp.components.data_pipelines.guest_nights_calculations import (
    calculate_guest_nights_by_age_month,
)
from palmavillapp.components.file_formatting.excel_gen import (
    update_template_word_with_values,
)

# Page configuration
st.set_page_config(layout="wide")
st.title("Create Word files with correct tax information")

# Optional file re-upload widgets
uploaded_felho = st.file_uploader(
    "Optional: Re-upload Felhomatrac Excel here", type=["xlsx", "xls"]
)

# Use re-uploaded files or previously uploaded files
if "uploaded_felho" not in st.session_state:
    st.session_state["uploaded_felho"] = None

if uploaded_felho is not None:
    st.session_state["uploaded_felho"] = uploaded_felho

felho_file = st.session_state["uploaded_felho"]

if uploaded_felho is None and st.session_state["uploaded_felho"] is not None:
    st.success("Using Felhomatrac Excel file from the previous upload.")
elif uploaded_felho is not None:
    st.success("Felhomatrac Excel file uploaded successfully.")


# Load dataframes if files are available
def create_document(guest_nights, date_year, month):
    # total_nights = guest_nights[month]["adult"] + guest_nights[month]["kid"]
    kid_nights = guest_nights[month]["kid"]
    adult_nights = guest_nights[month]["adult"]
    # total_ifa = guest_nights[month]["adult"] * 530
    doc = update_template_word_with_values(kid_nights, adult_nights, date_year, month)
    return month, doc


if "date_year" not in st.session_state:
    st.session_state["date_year"] = 0

if "guest_nights" not in st.session_state:
    st.session_state["guest_nights"] = {}

if "months_detected" not in st.session_state:
    st.session_state["months_detected"] = []

if "selected_months" not in st.session_state:
    st.session_state["selected_months"] = []

# Flag to check if start button has been pressed
if "start_pressed" not in st.session_state:
    st.session_state["start_pressed"] = False

if felho_file is not None:
    if st.button("Start"):
        st.session_state["start_pressed"] = True
        df_felho = pd.read_excel(felho_file)
        df_felho.columns = FELHO_COLUMNS
        guest_nights = calculate_guest_nights_by_age_month(df_felho=df_felho)
        st.session_state["date_year"] = guest_nights["date_year"]
        st.session_state["guest_nights"] = guest_nights["monthly"]
        st.session_state["months_detected"] = list(guest_nights["monthly"].keys())

    if st.session_state["start_pressed"]:
        if len(st.session_state["months_detected"]) == 1:
            month, doc = create_document(
                st.session_state["guest_nights"],
                st.session_state["date_year"],
                st.session_state["months_detected"][0],
            )
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)

            st.download_button(
                label=f"Download IFA_{month}.docx",
                data=buffer,
                file_name=f"IFA_{month}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

        elif len(st.session_state["months_detected"]) > 1:
            st.write("Select the months for which you want to generate documents.")
            # Multi-select widget for months
            selected_months = st.multiselect(
                "Select months",
                st.session_state["months_detected"],
                # default=st.session_state["selected_months"],
            )
            st.session_state["selected_months"] = selected_months
            # Only show the button if some months are selected
            if selected_months:
                if st.button("Generate document for selected months"):
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(
                        zip_buffer, "a", zipfile.ZIP_DEFLATED
                    ) as zip_file:
                        for month in selected_months:
                            _, doc = create_document(
                                st.session_state["guest_nights"],
                                st.session_state["date_year"],
                                month,
                            )
                            doc_buffer = BytesIO()
                            doc.save(doc_buffer)
                            doc_buffer.seek(0)
                            zip_file.writestr(
                                f"IFA_{st.session_state['date_year']}_{month}.docx",
                                doc_buffer.read(),
                            )
                    zip_buffer.seek(0)
                    st.download_button(
                        label="Download All Documents (ZIP)",
                        data=zip_buffer,
                        file_name="documents.zip",
                        mime="application/zip",
                    )

        else:
            st.warning("No data detected in the Felhomatrac Excel file.")

else:
    st.warning("Please upload the Felhomatrac Excel file to proceed.")
