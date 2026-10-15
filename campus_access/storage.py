
"""Save and load campus access-card requests using JSON."""

import json
from pathlib import Path

from campus_access import requests


def save_requests(path):
    """Save all requests to a JSON file."""
    path = Path(path)

    requests.validate_dataset(requests.REQUESTS)

    temporary_path = path.with_name(path.name + ".tmp")

    try:
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump(requests.REQUESTS, file, indent=2)
            file.write("\n")

        # Replace the destination only after writing the temporary file.
        temporary_path.replace(path)

    except (OSError, TypeError, ValueError):
        try:
            temporary_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def load_requests(path):
    """Load and validate requests without damaging current data on failure."""
    path = Path(path)

    if not path.exists():
        requests.reset_requests()
        return

    try:
        with path.open("r", encoding="utf-8") as file:
            loaded_records = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {path}: "
            f"line {error.lineno}, column {error.colno}."
        ) from error

    except UnicodeDecodeError as error:
        raise ValueError(
            f"The file {path} is not valid UTF-8 text."
        ) from error

    # Validate everything before changing the current collection.
    requests.validate_dataset(loaded_records)
    requests.reset_requests(loaded_records)
