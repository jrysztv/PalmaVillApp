import pandas as pd

from dateutil.relativedelta import relativedelta


def calculate_guest_nights_by_age_month(df_felho):
    # Convert columns to datetime
    df_felho["date_of_birth"] = pd.to_datetime(df_felho["date_of_birth"])
    df_felho["first_night"] = pd.to_datetime(df_felho["first_night"])

    df_felho["age_at_first_night"] = df_felho.apply(
        lambda row: calculate_age(row["date_of_birth"], row["first_night"]), axis=1
    )

    # Determine if over 18
    df_felho["over_18"] = df_felho["age_at_first_night"] >= 18
    df_felho["month"] = df_felho["first_night"].dt.month.replace(
        {
            1: "Január",
            2: "Február",
            3: "Március",
            4: "Április",
            5: "Május",
            6: "Június",
            7: "Július",
            8: "Augusztus",
            9: "Szeptember",
            10: "Október",
            11: "November",
            12: "December",
        }
    )
    df_felho["age_category"] = df_felho["over_18"].apply(
        lambda x: "adult" if x else "kid"
    )
    guest_nights = {
        "monthly": (
            df_felho.groupby(["month", "age_category"])["nights"]
            .sum()
            .unstack(fill_value=0)
            .to_dict(orient="index")
        ),
        "date_year": int(df_felho["first_night"].dt.year[0]),
    }
    return guest_nights


def calculate_age(dob, first_night):
    return relativedelta(first_night, dob).years
