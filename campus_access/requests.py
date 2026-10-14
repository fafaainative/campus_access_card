
import json
from pathlib import Path

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


def create_request(fellow_id, card_type):
    if not isinstance(fellow_id, str) or not fellow_id.strip():
        raise ValueError("Fellow ID must not be blank")

    if not isinstance(card_type, str):
        raise ValueError("Invalid card type")

    card_type = card_type.strip().lower()
    if card_type not in CARD_TYPES:
        raise ValueError("Card type must be visitor, student, or staff")

    numbers = []
    for request in REQUESTS:
        request_id = request["id"]
        if (
            isinstance(request_id, str)
            and request_id.startswith("A")
            and request_id[1:].isdigit()
        ):
            numbers.append(int(request_id[1:]))

    next_number = max(numbers, default=0) + 1
    request_id = f"A{next_number:03d}"

    request = {
        "id": request_id,
        "fellow_id": fellow_id.strip(),
        "card_type": card_type,
        "status": "requested",
        "approved_by": None,
    }

    REQUESTS.append(request)
    return request.copy()


def get_request(request_id):
    for request in REQUESTS:
        if request["id"] == request_id:
            return request.copy()

    raise ValueError(f"Request {request_id} was not found")


def _validate_requests(data):
    if not isinstance(data, list):
        raise ValueError("Saved data must be a list")

    seen_ids = set()

    for request in data:
        if not isinstance(request, dict):
            raise ValueError("Each request must be a dictionary")

        if set(request.keys()) != REQUIRED_KEYS:
            raise ValueError("Request has missing or unexpected fields")

        request_id = request["id"]
        fellow_id = request["fellow_id"]
        card_type = request["card_type"]
        status = request["status"]
        approved_by = request["approved_by"]

        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError("Request ID must not be blank")

        if request_id in seen_ids:
            raise ValueError(f"Duplicate request ID: {request_id}")
        seen_ids.add(request_id)

        if not isinstance(fellow_id, str) or not fellow_id.strip():
            raise ValueError("Fellow ID must not be blank")

        if not isinstance(card_type, str) or card_type not in CARD_TYPES:
            raise ValueError("Invalid saved card type")

        if not isinstance(status, str) or status not in STATUSES:
            raise ValueError("Invalid saved status")

        if status == "requested" and approved_by is not None:
            raise ValueError("Requested cards must not have an approver")

        if status != "requested":
            if not isinstance(approved_by, str) or not approved_by.strip():
                raise ValueError("Processed cards must have an approver")


def save_requests(path):
    destination = Path(path)
    temporary = destination.with_suffix(destination.suffix + ".tmp")

    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        _validate_requests(REQUESTS)

        with temporary.open("w", encoding="utf-8") as file:
            json.dump(REQUESTS, file, indent=2)
            file.write("\n")

        temporary.replace(destination)

    except (OSError, TypeError, ValueError) as error:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise ValueError(f"Could not save requests: {error}") from error


def load_requests(path):
    source = Path(path)

    if not source.exists():
        REQUESTS.clear()
        return

    try:
        with source.open("r", encoding="utf-8") as file:
            data = json.load(file)
        _validate_requests(data)

    except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
        raise ValueError(f"Could not load requests: {error}") from error

    # Update the shared list in place so Engineer B can keep using it.
    REQUESTS[:] = data
