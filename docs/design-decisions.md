Campus Access Card Request Manager — Design Decisions

1. Project Overview

Campus Access Card Request Manager is a Python command-line application that manages access-card requests for visitors, students, and staff.

The application allows users to create requests, approve them, issue cards, record returns, and save request data for future use.

This document records the design decisions agreed upon by Engineer A and Engineer B to help us build compatible modules, avoid conflicting assumptions, and make the application easier to test and maintain.

2. Programming Tools

We decided to use:

Python 3 for the application.

Lists and dictionaries to manage request records in memory.

JSON to save and reload requests.

unittest for automated testing.

Git and GitHub for version control, collaboration, and code review.

We will use only Python's standard library. No external packages or database are required.

3. Request Data Structure

Each request will be stored as a dictionary containing exactly five fields:

Field

Purpose

Example

id

Unique request identifier

"A001"

fellow_id

Identifier of the person requesting a card

"F001"

card_type

Type of access card requested

"student"

status

Current stage of the request

"requested"

approved_by

Identifier of the approving staff member

None

A new request starts with the status requested and approved_by set to None.

The allowed card types are visitor, student, and staff. Card types will be normalized to lowercase after removing unnecessary surrounding spaces.

We chose this structure because dictionaries allow us to access and update individual fields clearly, while lists allow us to manage multiple requests.

4. Request IDs

Every request will have a unique ID following this format:

First request: A001

Second request: A002

Third request: A003

The application will determine the next ID from existing valid IDs instead of relying only on the number of requests currently in memory.

This is important because requests may be loaded from a JSON file after the application restarts. The ID generator must not reuse an existing ID.

IDs must use the letter A followed by ASCII digits (0–9). Malformed IDs and duplicate IDs in saved data must be rejected.

5. Input Validation and Errors

We decided to validate input before creating or modifying a request.

The application must reject:

Blank or invalid fellow IDs.

Unsupported card types.

Unknown request IDs.

Invalid staff approver identifiers.

Malformed or duplicate request IDs in saved data.

Unsupported workflow transitions.

Invalid or corrupted JSON data.

Functions will raise ValueError when supplied values or requested operations violate the agreed rules.

The CLI should catch expected errors and display helpful messages so users can correct their input instead of the application crashing unnecessarily.

6. Request Workflow

All requests must follow this sequence:

requested → approved → issued → returned

The following rules apply:

A new request starts as requested.

Only a requested record can be approved.

Approval requires a nonblank staff identifier.

Only an approved request with a valid approver can be issued.

Only an issued card can be returned.

A returned card is in its final state and cannot be issued or returned again.

We chose these rules to prevent cards from being issued without approval or moving through the process in the wrong order.

Important decision: An invalid operation must not partially modify a request. The function must check the required conditions before changing the stored record.

7. Responsibilities of Each Engineer

Engineer A — Request Management

Engineer A is responsible for:

Creating requests.

Validating fellow IDs and card types.

Generating unique request IDs.

Looking up individual requests.

Saving and loading requests using JSON.

Writing request validation and persistence tests.

Suggested interfaces:

create_request(fellow_id, card_type)
get_request(request_id)
save_requests(path)
load_requests(path)

Engineer B — Workflow Management

Engineer B is responsible for:

Approving requests.

Issuing access cards.

Recording card returns.

Enforcing valid workflow transitions.

Implementing and testing the CLI workflow.

Suggested interfaces:

approve_request(requests, request_id, approved_by)
issue_card(requests, request_id)
return_card(requests, request_id)

These signatures are the agreed interface for the current implementation. If either engineer needs to change a signature, both engineers must discuss and update the relevant tests and callers.

8. Shared Request Data

Engineer A's campus_access/requests.py owns the shared in-memory list named REQUESTS.

Engineer B's workflow functions will receive that list as an argument and update the appropriate request dictionary in place.

For example, the CLI should pass requests.REQUESTS to the workflow functions.

When loading saved requests, Engineer A should update the existing list in place rather than reassigning the REQUESTS variable. This preserves the identity of the shared list for any code that holds a reference to it.

Lookup functions should return a copy of the request when callers only need to inspect it. This helps prevent accidental changes to stored data through a lookup result.

9. JSON Persistence

The application will use JSON files to preserve request data between runs.

We decided that:

Saving requests must write valid request data.

Loading must validate the complete saved dataset before replacing the existing list.

Duplicate IDs, missing fields, unsupported statuses, and malformed JSON must be rejected.

A failed load must not erase or partially replace existing valid requests.

A missing file may start a fresh session only when that behaviour is consistent with the agreed application startup and storage rules.

The application must never silently treat a corrupted file as an empty dataset.

10. Automated Testing

Both engineers will write tests using Python's built-in unittest framework.

Engineer A will test request creation, validation, ID generation, lookup, saving, and loading.

Engineer B will test approvals, issuance, returns, invalid transitions, and preservation of records after rejected operations.

The team will test valid and invalid inputs, including:

Creating a valid request.

Rejecting a blank fellow ID or invalid card type.

Generating unique IDs after loading saved data.

Rejecting corrupted JSON and duplicate IDs.

Rejecting issue-before-approval.

Rejecting a blank approver.

Completing the full workflow.

Rejecting repeated operations on returned cards.

Confirming failed operations leave records unchanged.

The combined test command is:

python -m unittest discover -s tests -v

We will only report tests as passing after running them and checking the actual output.

11. Git and GitHub Workflow

Each engineer will work on a separate feature branch:

Engineer A: feat/1-request-validation

Engineer B: feat/2-access-workflow

Each engineer will commit their own implementation, tests, and relevant documentation, then open a pull request.

The other engineer will review the pull request, provide at least two meaningful observations, and request corrections where necessary. The author will address the feedback before approval.

We will not merge a pull request until the relevant tests and integration checks have been completed. We will follow the repository's agreed merge process and avoid direct feature development on main.

12. AI-Assisted Learning

AI may be used to explain concepts, review design choices, identify edge cases, and help interpret test failures.

Each engineer is responsible for understanding the implementation, testing suggestions independently, and recording their learning cycles in docs/ai-learning-log.md.

AI-generated suggestions will not be accepted automatically. We will compare them against the project requirements, run appropriate tests, and record our final decisions honestly.

13. Decisions Still Requiring Team Confirmation

Before the final integration, both engineers should confirm:

Whether the CLI saves automatically, saves through a menu option, or uses both approaches.

How a missing JSON file should be handled during startup.

Whether returned request records remain in the active list or are archived.

How the CLI handles unexpected input without terminating.

Whether all agreed function signatures match the actual code and tests.

Any agreed changes should be recorded in this document so both engineers work from the same expectations.

14. Final Design Principle

Our main priority is correctness, clear responsibilities, and reliable data.

We want an application that not only works in a successful demonstration but also handles invalid input, failed operations, corrupted saved data, and integration issues safely.

Each engineer should be able to explain their code, demonstrate their tests, and describe why the team's design decisions were made.