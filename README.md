<<<<<<< HEAD
🎓 Campus Access Card Request Manager

A simple Python-based command-line application for managing campus access-card requests. The system helps campus staff register requests for visitor, student, and staff access cards, approve requests, issue cards, and record returned cards.

This project was built as a collaborative learning challenge to practise Python programming, input validation, automated testing, JSON file handling, Git, GitHub collaboration, and code review.

🚀 Features

Create Requests: Register access-card requests with a fellow ID and card type.

View Requests: Display all requests and view an individual request by ID.

Input Validation: Reject blank fellow IDs, invalid card types, and incorrect inputs.

Automatic Request IDs: Generate unique IDs such as A001, A002, and A003.

Approve Requests: Record the identifier of the staff member approving a request.

Issue Cards: Issue cards only after approval.

Return Cards: Record when issued cards are returned.

Workflow Validation: Enforce the correct sequence: requested → approved → issued → returned.

JSON Persistence: Save requests and reload them when the application restarts.

Error Handling: Reject invalid operations and malformed saved data without silently discarding valid records.

Automated Testing: Use Python's built-in unittest framework to verify application behaviour.

🛠️ Technologies Used

Python 3

Python standard library

Dictionaries and lists

JSON for data persistence

unittest for automated testing

Git and GitHub for version control and collaboration

📋 Requirements

Python 3 installed on your computer.

Git installed for version control.

A GitHub account to access the project repository.

No external Python packages or database are required.

📖 Usage

1. Clone the repository

git clone <repository-url>
cd campus_access_card

Replace <repository-url> with the actual GitHub repository URL.

2. Run the application

python main.py

3. Menu options

When the program starts, the user should be able to choose from the following operations:

Create an access-card request

View all requests

View a request by ID

Approve a request

Issue an access card

Return an access card

Save and reload requests as supported by the application

Exit

Enter the number corresponding to the desired operation. The application should provide clear feedback when an operation succeeds or when an input is invalid.

Note: The menu descriptions should be updated if the final implementation uses different options or combines saving and loading into other operations.

🔄 Request Workflow

Every access-card request must follow this order:

Requested → Approved → Issued → Returned

A new request begins with the status requested.

An authorized staff identifier must be provided during approval.

A card can only be issued after approval.

A card can only be returned after it has been issued.

A returned card cannot be issued or returned again.

Invalid transitions must be rejected, and the request must remain unchanged when an operation fails.

📝 Request Data Structure

Each request contains five fields:

Field

Description

Example

id

Unique request identifier

A001

fellow_id

Identifier of the person requesting a card

F001

card_type

Requested card category

visitor

status

Current workflow status

requested

approved_by

Identifier of the approving staff member

None

Supported card types

visitor

student

staff

Request IDs must remain unique, including after the application saves data, restarts, and reloads existing requests.

💻 Example Input and Output

Create a request

Enter fellow ID: F001
Enter card type: visitor

Request created successfully!

Request ID: A001
Fellow ID: F001
Card Type: visitor
Status: requested
Approved By: None

Approve a request

Enter request ID: A001
Enter approving staff ID: M01

Request A001 approved successfully.
Status: approved
Approved By: M01

Issue a card

Enter request ID: A001

Access card issued successfully.
Status: issued

Return a card

Enter request ID: A001

Access card returned successfully.
Status: returned

These examples illustrate the expected behaviour; the exact wording and layout depend on the final CLI implementation.

🧪 Running the Tests

From the repository root, run:

python -m unittest discover -s tests -v

The tests should cover scenarios such as:

Creating valid requests.

Rejecting blank fellow IDs and invalid card types.

Generating unique IDs after reloading saved data.

Rejecting unknown request IDs.

Saving and loading requests using JSON.

Rejecting malformed JSON and duplicate IDs.

Preventing cards from being issued before approval.

Rejecting blank approver identifiers.

Completing the full request lifecycle.

Confirming that failed operations do not change request data.

A test should only be described as passing after it has actually been executed successfully.

📂 Project Structure

campus_access_card/
│
├── main.py
├── campus_access/
│   ├── __init__.py
│   ├── requests.py
│   └── workflow.py
│
├── tests/
│   ├── test_requests.py
│   └── test_workflow.py
│
├── docs/
│   ├── ai-learning-log.md
│   └── design-decisions.md
│
├── .gitignore
└── README.md

File descriptions:

main.py — Starts the command-line application and displays the menu.

campus_access/requests.py — Handles request creation, validation, unique IDs, lookup, and JSON persistence.

campus_access/workflow.py — Handles request approval, card issuance, and returns.

tests/test_requests.py — Tests request creation, validation, IDs, and storage.

tests/test_workflow.py — Tests workflow transitions and invalid operations.

docs/ai-learning-log.md — Records AI-assisted learning questions, experiments, verification, and decisions.

docs/design-decisions.md — Documents agreed design choices and interfaces.

.gitignore — Excludes generated files and other items that should not be committed.

🤝 Team Collaboration

This project was developed by two engineers with separate responsibilities.

Engineer A — Request Management

Request creation and input validation.

Unique request ID generation.

Individual request lookup.

JSON saving and loading.

Request-related automated tests.

Engineer B — Workflow Management

Request approval.

Access-card issuance and return.

Workflow validation.

Command-line interaction.

Workflow-related automated tests.

Both engineers are responsible for reviewing each other's work, resolving integration issues, writing meaningful tests, and confirming that the combined application works before merging changes into main.

🧠 Learning and Development

The project focuses on understanding and applying core software engineering practices, including:

Writing reusable Python functions.

Working with dictionaries and lists.

Validating inputs and handling exceptions.

Modelling a process using valid state transitions.

Saving and loading data with JSON.

Writing automated tests with unittest.

Using Git branches, commits, pull requests, and code reviews.

Using AI to explain concepts, investigate edge cases, and understand test failures while verifying suggestions independently.

🔮 Possible Enhancements

Future improvements could include:

Adding search and filtering by card type or status.

Improving the display of request records in a table.

Adding timestamps for approval, issuance, and return.

Introducing staff-role or authorization checks.

Adding audit logs for important changes.

Improving backup and recovery for saved JSON data.

👨‍💻 Developers

Engineer A: Ikyaaibo Ephraim Aondofa

Engineer B: Okonkwo Ifunanaya

✅ Final Note

Campus Access Card Request Manager is a practical project for learning how to build reliable Python applications through implementation, testing, collaboration, and review. The goal is not just to make the program run, but to understand the
=======
# campus_access_card
A campus Access Card is a CLI applicqation that issues visitor, student and staff access cards to create a request that will be approved with an authorized staff identifier. 
>>>>>>> origin/feat/1-request-workflow
