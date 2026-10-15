
"""Command-line interface for the Campus Access Card Manager."""

from pathlib import Path

from campus_access import requests, storage, workflow


# --------------------------------------------------
# Configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "requests.json"


# --------------------------------------------------
# Display helpers
# --------------------------------------------------

def print_header(title):
    """Display a consistent section heading."""
    print()
    print("=" * 64)
    print(f"  {title}")
    print("=" * 64)


def pause():
    """Wait for the user before returning to the menu."""
    input("\nPress Enter to return to the main menu...")


def display_menu():
    """Display the main application menu."""
    print_header("🎓 CAMPUS ACCESS CARD MANAGER")
    print("  Manage campus access-card requests with ease.")
    print("-" * 64)
    print("  1. 📝 Create a new request")
    print("  2. 📋 View all requests")
    print("  3. 🔍 Search for a request")
    print("  4. ✅ Approve a request")
    print("  5. 🎫 Issue an access card")
    print("  6. ↩️  Return an access card")
    print("  7. 💾 Save and exit")
    print("-" * 64)


def display_request_table(records):
    """Display requests in aligned columns."""
    if not records:
        print("\n📭 No access-card requests found.")
        return

    columns = [
        ("ID", "id"),
        ("FELLOW ID", "fellow_id"),
        ("CARD TYPE", "card_type"),
        ("STATUS", "status"),
        ("APPROVED BY", "approved_by"),
    ]

    rows = []
    for record in records:
        rows.append([
            str(record["id"]),
            str(record["fellow_id"]),
            str(record["card_type"]),
            str(record["status"]),
            str(record["approved_by"] or "—"),
        ])

    widths = []
    for index, (heading, _) in enumerate(columns):
        widths.append(
            max(len(heading), *(len(row[index]) for row in rows))
        )

    separator = "+" + "+".join(
        "-" * (width + 2) for width in widths
    ) + "+"

    print()
    print(separator)
    print(
        "|"
        + "|".join(
            f" {heading:<{widths[index]}} "
            for index, (heading, _) in enumerate(columns)
        )
        + "|"
    )
    print(separator)

    for row in rows:
        print(
            "|"
            + "|".join(
                f" {value:<{widths[index]}} "
                for index, value in enumerate(row)
            )
            + "|"
        )

    print(separator)
    print(f"Total requests: {len(records)}")


def display_request_details(record):
    """Display the details of one request."""
    print_header("📄 REQUEST DETAILS")
    print(f"  Request ID : {record['id']}")
    print(f"  Fellow ID  : {record['fellow_id']}")
    print(f"  Card type  : {record['card_type'].title()}")
    print(f"  Status     : {record['status'].replace('_', ' ').title()}")
    print(f"  Approved by: {record['approved_by'] or 'Not yet approved'}")


# --------------------------------------------------
# Persistence
# --------------------------------------------------

def save_current_data():
    """Save current requests and report any storage errors."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        storage.save_requests(DATA_FILE)
        print("💾 Requests saved successfully.")
        return True

    except (OSError, ValueError, TypeError) as error:
        print(f"❌ Could not save requests: {error}")
        print("⚠️ Your latest changes may not be saved to disk.")
        return False


def load_saved_data():
    """Load saved requests before displaying the menu."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        storage.load_requests(DATA_FILE)
        print(
            f"📂 Loaded {len(requests.REQUESTS)} saved request(s)."
        )
        return True

    except (OSError, ValueError, TypeError) as error:
        print(f"\n❌ Could not load saved requests: {error}")
        print("⚠️ The application will stop to protect existing data.")
        return False


# --------------------------------------------------
# Request operations
# --------------------------------------------------

def create_new_request():
    """Collect details and create an access-card request."""
    print_header("📝 CREATE A NEW REQUEST")

    fellow_id = input("Enter fellow ID: ").strip()

    print("\nAvailable card types:")
    print("  1. Visitor")
    print("  2. Student")
    print("  3. Staff")

    card_choices = {
        "1": "visitor",
        "2": "student",
        "3": "staff",
    }

    choice = input("\nChoose a card type (1-3): ").strip()

    if choice not in card_choices:
        print("❌ Invalid choice. Please select 1, 2, or 3.")
        return

    card_type = card_choices[choice]

    try:
        record = requests.create_request(fellow_id, card_type)

        print("\n" + "-" * 48)
        print("✅ REQUEST CREATED SUCCESSFULLY")
        print("-" * 48)
        print(f"  Request ID : {record['id']}")
        print(f"  Fellow ID  : {record['fellow_id']}")
        print(f"  Card type  : {record['card_type'].title()}")
        print(f"  Status     : {record['status'].title()}")
        print("-" * 48)

        save_current_data()

    except (ValueError, KeyError) as error:
        print(f"❌ Could not create request: {error}")


def view_all_requests():
    """Display all stored requests."""
    print_header("📋 ALL ACCESS-CARD REQUESTS")
    display_request_table(requests.REQUESTS)


def search_request():
    """Find and display a request by ID."""
    print_header("🔍 SEARCH FOR A REQUEST")

    request_id = input(
        "Enter request ID (for example, A001): "
    ).strip().upper()

    try:
        record = requests.get_request(request_id)
        display_request_details(record)

    except (ValueError, KeyError) as error:
        print(f"\n❌ {error}")


def approve_access_request():
    """Approve a requested card."""
    print_header("✅ APPROVE AN ACCESS-CARD REQUEST")

    request_id = input("Enter request ID: ").strip().upper()
    approved_by = input("Enter approving staff member's name: ").strip()

    confirm = input(
        f"\nApprove request {request_id} under '{approved_by}'? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("ℹ️ Approval cancelled.")
        return

    success, message = workflow.approve_request(
        requests.REQUESTS,
        request_id,
        approved_by,
    )

    if success:
        print(f"\n✅ {message}")
        save_current_data()
    else:
        print(f"\n❌ {message}")


def issue_access_card():
    """Issue a card after approval."""
    print_header("🎫 ISSUE AN ACCESS CARD")

    request_id = input("Enter request ID: ").strip().upper()

    confirm = input(
        f"\nConfirm issuing the card for {request_id}? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("ℹ️ Card issuance cancelled.")
        return

    success, message = workflow.issue_card(
        requests.REQUESTS,
        request_id,
    )

    if success:
        print(f"\n✅ {message}")
        save_current_data()
    else:
        print(f"\n❌ {message}")


def return_access_card():
    """Mark an issued card as returned."""
    print_header("↩️ RETURN AN ACCESS CARD")

    request_id = input("Enter request ID: ").strip().upper()

    confirm = input(
        f"\nConfirm returning the card for {request_id}? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("ℹ️ Card return cancelled.")
        return

    success, message = workflow.return_card(
        requests.REQUESTS,
        request_id,
    )

    if success:
        print(f"\n✅ {message}")
        save_current_data()
    else:
        print(f"\n❌ {message}")


# --------------------------------------------------
# Application entry point
# --------------------------------------------------

def main():
    """Load data and run the interactive menu."""
    print_header("🎓 CAMPUS ACCESS CARD MANAGER")
    print("Welcome! Preparing your access-card request manager...")

    if not load_saved_data():
        return 1

    actions = {
        "1": create_new_request,
        "2": view_all_requests,
        "3": search_request,
        "4": approve_access_request,
        "5": issue_access_card,
        "6": return_access_card,
    }

    while True:
        display_menu()
        choice = input("Select an option (1-7): ").strip()

        if choice == "7":
            print_header("💾 SAVING AND EXITING")

            if save_current_data():
                print("👋 Thank you for using Campus Access Card Manager!")
                return 0

            retry = input(
                "Saving failed. Retry before exiting? (y/n): "
            ).strip().lower()

            if retry == "y":
                continue

            print("⚠️ Exiting without confirming that data was saved.")
            return 1

        action = actions.get(choice)

        if action is None:
            print("❌ Invalid selection. Please choose a number from 1 to 7.")
            continue

        try:
            action()
        except (OSError, ValueError, KeyError, TypeError) as error:
            print(f"\n❌ An unexpected operation error occurred: {error}")

        pause()


if __name__ == "__main__":
    raise SystemExit(main())
