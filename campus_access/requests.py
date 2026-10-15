
import re

REQUESTS = []

CARD_TYPES = {"visitor", "student", "staff"}
STATUSES = {"requested", "approved", "issued", "returned"}

REQUIRED_KEYS = {
    "id",
    "fellow_id",
    "card_type",
    "status",
    "approved_by",
}


def validate_request_id(request_id):
    """Validate IDs in the format A001, A002, and so on."""
    if not isinstance(request_id, str):
        raise ValueError("Request ID must be a string.")

    if re.fullmatch(r"A[0-9]{3,}", request_id) is None:
        raise ValueError(
            "Request ID must start with A and contain at least three ASCII digits."
        )

    if int(request_id[1:]) < 1:
        raise ValueError("Request ID number must be greater than zero.")

    return request_id


def validate_request_record(record):
    """Validate one complete request dictionary."""
    if not isinstance(record, dict):
        raise ValueError("Each request must be a dictionary.")

    if set(record.keys()) != REQUIRED_KEYS:
        raise ValueError(
            "Request must contain exactly: id, fellow_id, card_type, "
            "status, approved_by."
        )

    validate_request_id(record["id"])

    fellow_id = record["fellow_id"]
    if not isinstance(fellow_id, str) or not fellow_id.strip():
        raise ValueError("Fellow ID must be a non-empty string.")

    card_type = record["card_type"]
    if not isinstance(card_type, str) or card_type not in CARD_TYPES:
        raise ValueError("Invalid card type.")

    status = record["status"]
    if not isinstance(status, str) or status not in STATUSES:
        raise ValueError("Invalid request status.")

    approved_by = record["approved_by"]
    if approved_by is not None:
        if not isinstance(approved_by, str) or not approved_by.strip():
            raise ValueError(
                "Approved by must be None or a non-empty staff name."
            )

    return True


def validate_dataset(records):
    """Validate a complete list of requests and reject duplicate IDs."""
    if not isinstance(records, list):
        raise ValueError("Saved requests must be a list.")

    seen_ids = set()

    for record in records:
        validate_request_record(record)

        request_id = record["id"]
        if request_id in seen_ids:
            raise ValueError(f"Duplicate request ID: {request_id}")

        seen_ids.add(request_id)

    return True


def reset_requests(records=None):
    """Reset request data; useful for tests and validated storage loading."""
    global REQUESTS

    if records is None:
        REQUESTS = []
        return

    validate_dataset(records)

    # Copy each dictionary to avoid retaining the caller's dictionary objects.
    REQUESTS = [record.copy() for record in records]


def create_request(fellow_id, card_type):
    """Validate input, generate a unique ID, and create a request."""
    if not isinstance(fellow_id, str) or not fellow_id.strip():
        raise ValueError("Fellow ID must be a non-empty string.")

    if not isinstance(card_type, str):
        raise ValueError("Card type must be a string.")

    normalized_card_type = card_type.strip().lower()
    if normalized_card_type not in CARD_TYPES:
        raise ValueError(
            "Invalid card type. Choose visitor, student, or staff."
        )

    # Validate existing data before generating another ID.
    validate_dataset(REQUESTS)

    # Use the highest existing number, so deleting an earlier request
    # does not cause its ID to be reused.
    highest_number = 0

    for record in REQUESTS:
        number = int(record["id"][1:])
        if number > highest_number:
            highest_number = number

    request_id = f"A{highest_number + 1:03d}"

    new_request = {
        "id": request_id,
        "fellow_id": fellow_id.strip(),
        "card_type": normalized_card_type,
        "status": "requested",
        "approved_by": None,
    }

    validate_request_record(new_request)
    REQUESTS.append(new_request)

    return new_request


def get_request(request_id):
    """Return a request by ID or raise KeyError if it does not exist."""
    validate_request_id(request_id)

    for record in REQUESTS:
        if record["id"] == request_id:
            return record

    raise KeyError(f"Request not found: {request_id}")
