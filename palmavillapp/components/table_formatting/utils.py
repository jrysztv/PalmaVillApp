from palmavillapp.components.constants import GREEN_MESSAGE, RED_MESSAGE, YELLOW_MESSAGE


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
