

VALID_STATUSES = {"requested", "approved", "issued", "returned"}


def _find_request(requests, request_id):
    """Find a request by ID, ignoring letter case and surrounding spaces."""
    if not isinstance(request_id, str):
        return None

    request_id = request_id.strip().upper()

    if not request_id:
        return None

    for request in requests:
        if str(request.get("id", "")).strip().upper() == request_id:
            return request

    return None


def approve_request(requests, request_id, approved_by):
    """Approve a requested card and record the approver."""
    request = _find_request(requests, request_id)

    if request is None:
        return False, "Request not found."

    if request.get("status") != "requested":
        return False, "Only requested cards can be approved."

    if not isinstance(approved_by, str) or not approved_by.strip():
        return False, "Approver ID must be a nonempty string."

    # Validate everything before changing the request.
    request["approved_by"] = approved_by.strip()
    request["status"] = "approved"

    return True, "Request approved successfully."


def issue_card(requests, request_id):
    """Issue a card only after its request has been approved."""
    request = _find_request(requests, request_id)

    if request is None:
        return False, "Request not found."

    if request.get("status") != "approved":
        return False, "Only approved cards can be issued."

    approved_by = request.get("approved_by")

    if not isinstance(approved_by, str) or not approved_by.strip():
        return False, "A valid approver is required before issuing."

    request["status"] = "issued"

    return True, "Card issued successfully."


def return_card(requests, request_id):
    """Return an issued card and mark the request as returned."""
    request = _find_request(requests, request_id)

    if request is None:
        return False, "Request not found."

    if request.get("status") != "issued":
        return False, "Only issued cards can be returned."

    request["status"] = "returned"

    return True, "Card returned successfully."
