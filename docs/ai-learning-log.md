AI Learning Log — Engineer B

Project: Campus Access Card System
Module: campus_access/workflow.py
Tests: tests/test_workflow.py

Learning Cycle 1: State Transitions

My question: Why must a card be approved before issuing?

AI explanation: State transitions ensure that operations follow the correct sequence: requested → approved → issued → returned.

My prediction: Issuing a card with status requested should raise a ValueError without changing the request.

My experiment: I tested issuing a card before approval and completed the valid workflow.

Verification: [Record the actual test results.]

My final decision: I accepted the approach because it prevents invalid operations and maintains the correct workflow.

Learning Cycle 2: Preserving Request Records

My question: How can I ensure failed operations do not change request data?

AI explanation: Validate the request's current state before modifying any fields.

My prediction: Returning a card that has not been issued should raise a ValueError, leaving the request unchanged.

My experiment: I saved a copy of the request, attempted the invalid operation, and compared the record with the saved copy.

Verification: [Record the actual test results.]

My final decision: I accepted the advice. I learned that validation must happen before modification to preserve data when an operation fails.

Learning Cycle 3: Evaluating AI Advice and Edge Cases

My question: Does returning request.copy() prevent changes to the original request?

AI explanation: A shallow copy creates a separate dictionary for the return value, but it does not undo changes already made to the original dictionary.

My prediction: The original request and returned copy would both reflect a successful approval.

My experiment: I inspected the request in the shared list and the returned dictionary after approval. I also tested returning an already returned card.

Verification: [Record the actual observations and test results.]

My final decision: I rejected the idea that request.copy() alone protects the original record. I learned to validate before modifying data and to test invalid repeated operations.

Final Reflection

I learned how to enforce workflow rules, preserve request records when operations fail, and use automated tests to verify expected behaviour. I also learned to evaluate AI suggestions critically instead of accepting them without testing.

Test command: python3 -m unittest discover -s tests -v

Actual test result: [Ran 12 tests in 0.001s]

Outstanding issues: [None]
