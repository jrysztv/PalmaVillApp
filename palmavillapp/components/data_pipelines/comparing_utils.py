import pandas as pd

from fuzzywuzzy import process

from palmavillapp.components.constants import GREEN_MESSAGE, RED_MESSAGE, YELLOW_MESSAGE


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
