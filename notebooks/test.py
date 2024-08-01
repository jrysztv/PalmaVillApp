import streamlit as st
import pandas as pd

from fuzzywuzzy import process


def get_matching_name(row, df, column):
    name = row[column].lower()
    choices = df[column].str.lower().str.replace(",", "").tolist()
    match, score = process.extractOne(name, choices)
    return match if score >= 80 else None  # Adjust the score threshold as needed


def check_date_overlap(row_booking, df_felho):
    start_booking = row_booking["first_night"]
    end_booking = row_booking["last_night"]
    overlap = df_felho[
        (df_felho["first_night"] <= end_booking)
        & (df_felho["last_night"] >= start_booking)
    ]
    return not overlap.empty


GREEN_MESSAGE = "Name and date match found"
YELLOW_MESSAGE = "Only date match found. Possibly correct"
RED_MESSAGE = "No match found. Update Felhőmatrac"


def highlight_rows(row):
    pastel_green = "background-color: #d4edda; color: black;"
    pastel_yellow = "background-color: #fff3cd; color: black;"
    pastel_red = "background-color: #f8d7da; color: black;"
    default = [""] * len(row)

    if row["colour_code"] == GREEN_MESSAGE:
        return [pastel_green] * len(row)
    elif row["colour_code"] == YELLOW_MESSAGE:
        return [pastel_yellow] * len(row)
    elif row["colour_code"] == RED_MESSAGE:
        return [pastel_red] * len(row)
    else:
        return default


def compare_data(df_felho, df_booking):
    df_booking[["last_name", "first_name"]] = df_booking["booked_by"].str.split(
        ", ", expand=True
    )

    df_booking.insert(3, "last_name", df_booking.pop("last_name"))

    df_booking.insert(4, "first_name", df_booking.pop("first_name"))
    df_booking = df_booking[df_booking["status"] == "ok"]
    df_felho["full_name"] = df_felho["first_name"] + " " + df_felho["last_name"]
    df_booking["full_name"] = df_booking["first_name"] + " " + df_booking["last_name"]
    df_booking["first_night"] = pd.to_datetime(df_booking["first_night"])
    df_booking["last_night"] = pd.to_datetime(df_booking["last_night"])
    df_felho["first_night"] = pd.to_datetime(df_felho["first_night"])
    df_felho["last_night"] = pd.to_datetime(df_felho["last_night"])
    df_booking["full_name_match"] = df_booking.apply(
        lambda row: get_matching_name(row, df_felho, "full_name"), axis=1
    )
    df_booking["has_name_overlap"] = df_booking["full_name_match"].notna()
    df_booking["has_date_overlap"] = df_booking.apply(
        lambda row: check_date_overlap(row, df_felho), axis=1
    )
    df_booking["colour_code"] = df_booking.apply(
        lambda row: (
            RED_MESSAGE
            if not row["has_date_overlap"]
            else YELLOW_MESSAGE
            if not row["has_name_overlap"]
            else GREEN_MESSAGE
        ),
        axis=1,
    )
    df_booking["colour_sort_key"] = df_booking["colour_code"].map(
        {GREEN_MESSAGE: 1, YELLOW_MESSAGE: 2, RED_MESSAGE: 3}
    )
    # df_booking = df_booking.sort_values(by=["colour_sort_key"], ascending=False)
    # df_booking = df_booking.drop(columns=["colour_sort_key"])
    return df_booking


FELHO_COLUMNS = [
    "guestbook_id",
    "first_night",
    "last_night",
    "last_name",
    "first_name",
    "date_of_birth",
    "id_card",
    "passport",
    "driver_license",
    "other_id",
    "citizenship",
    "country_of_residence",
    "postal_code",
    "address",
    "ifa_status",
    "ifa_relevant_nights",
    "ifa_total",
    "ifa_per_night",
    "reservation",
    "arrival",
    "departure",
    "nights",
    "category",
    "residential_unit",
    "group",
    "place_of_birth",
    "email",
    "company_name",
]

# Second dataframe columns (with related columns commented)
BOOKING_COLUMNS = [
    "reservation_number",  # No related column
    "booked_by",  # No related column
    "guest_names",  # No related column
    "first_night",  # Related to 'first_night' in first list
    "last_night",  # Related to 'last_night' in first list
    "reservation_date",  # No related column
    "status",  # No related column
    "rooms",  # No related column
    "number_of_guests",  # No related column
    "adults",  # No related column
    "children",  # No related column
    "children_ages",  # No related column
    "price",  # No related column
    "commission",  # No related column
    "commission_rate",  # No related column
    "payment_status",  # No related column
    "payment_method",  # No related column
    "notes",  # No related column
    "booking_group",  # No related column
    "booker_country",  # No related column
    "purpose_of_travel",  # No related column
    "device",  # No related column
    "accommodation_type",  # No related column
    "duration_nights",  # No related column
    "cancellation_date",  # No related column
    "address",  # Related to 'address' in first list
    "phone_number",  # No related column
]


# Streamlit app
st.set_page_config(layout="wide")
st.title("Booking and Felhomatrac Update")

col1, col2 = st.columns(2)

with col1:
    uploaded_felho = st.file_uploader(
        "Update Felhomatrac Excel here", type=["xlsx", "xls"]
    )

with col2:
    uploaded_booking = st.file_uploader(
        "Update Booking Excel here", type=["xlsx", "xls"]
    )

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
        - <span style='background-color: #fff3cd; color: black;'>Yellow</span>: Date match found, name match not found.
        - <span style='background-color: #f8d7da; color: black;'>Red</span>: Booking entry missing entirely from felhomatrac.
        """,
            unsafe_allow_html=True,
        )

        st.dataframe(
            styled_df,
            hide_index=True,
            use_container_width=True,
            column_order=[
                "full_name",
                "first_night",
                "last_night",
                "full_name_match",
                "colour_code",
                "colour_sort_key",
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
