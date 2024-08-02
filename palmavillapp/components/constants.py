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


GREEN_MESSAGE = "GREEN"
YELLOW_MESSAGE = "YELLOW"
RED_MESSAGE = "RED"

TABLE_TEMPLATE_PATH = "data/table_template.xlsx"
HEADER_TEMPLATE_PATH = "data/header_template.xlsx"
IFA_TEMPLATE_PATH = "data/IFA_template.docx"
