

def _find_request(requests, request_id):
    """Find an existing request by ID, ignoring surrounding spaces and case."""
    if not isinstance(request_id, str) or not request_id.strip():
        raise ValueError("Request ID must be a nonempty string.")

    normalized_id = request_id.strip().upper()

    for request in requests:
        if str(request.get("id", "")).strip().upper() == normalized_id:
            return request

    raise KeyError(f"Request '{normalized_id}' was not found.")


def approve_request(requests, request_id, approved_by):
    """Approve a requested card and record the approver."""
    request = _find_request(requests, request_id)

    if request.get("status") != "requested":
        raise ValueError("Only requested cards can be approved.")

    if not isinstance(approved_by, str) or not approved_by.strip():
        raise ValueError("Approver ID must be a nonempty string.")

    # Validate first; mutate only after every check passes.
    request["status"] = "approved"
    request["approved_by"] = approved_by.strip()

    return request


def issue_card(requests, request_id):
    """Issue a card only after it has been approved."""
    request = _find_request(requests, request_id)

    if request.get("status") != "approved":
        raise ValueError("Only approved cards can be issued.")

    approved_by = request.get("approved_by")

    if not isinstance(approved_by, str) or not approved_by.strip():
        raise ValueError("The card must have a valid approver before issuing.")

    request["status"] = "issued"

    return request


def return_card(requests, request_id):
    """Return a card only when it is currently issued."""
    request = _find_request(requests, request_id)

    if request.get("status") != "issued":
        raise ValueError("Only issued cards can be returned.")

    request["status"] = "returned"

    return request

