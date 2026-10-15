
import copy
import unittest

from campus_access.workflow import (
    approve_request,
    issue_card,
    return_card,
)


class TestAccessCardWorkflow(unittest.TestCase):
    def setUp(self):
        """Create fresh test data before each test."""
        self.request = {
            "id": "A001",
            "fellow_id": "F001",
            "card_type": "student",
            "status": "requested",
            "approved_by": None,
        }

        # Test fixture only; this is not a production request store.
        self.requests = [self.request]

    def test_new_request_starts_as_requested(self):
        self.assertEqual(self.request["status"], "requested")
        self.assertIsNone(self.request["approved_by"])

    def test_valid_approver_can_approve(self):
        success, message = approve_request(
            self.requests, "A001", "M01"
        )

        self.assertTrue(success, message)
        self.assertEqual(self.request["status"], "approved")
        self.assertEqual(self.request["approved_by"], "M01")

    def test_empty_approver_is_rejected_without_changes(self):
        before = copy.deepcopy(self.request)

        success, message = approve_request(
            self.requests, "A001", ""
        )

        self.assertFalse(success)
        self.assertIn("Approver", message)
        self.assertEqual(self.request, before)

    def test_whitespace_approver_is_rejected(self):
        before = copy.deepcopy(self.request)

        success, message = approve_request(
            self.requests, "A001", "   "
        )

        self.assertFalse(success)
        self.assertEqual(self.request, before)

    def test_issue_before_approval_is_rejected(self):
        before = copy.deepcopy(self.request)

        success, message = issue_card(self.requests, "A001")

        self.assertFalse(success)
        self.assertEqual(self.request, before)

    def test_approved_request_can_be_issued(self):
        approve_request(self.requests, "A001", "M01")

        success, message = issue_card(self.requests, "A001")

        self.assertTrue(success, message)
        self.assertEqual(self.request["status"], "issued")

    def test_issued_card_can_be_returned(self):
        approve_request(self.requests, "A001", "M01")
        issue_card(self.requests, "A001")

        success, message = return_card(self.requests, "A001")

        self.assertTrue(success, message)
        self.assertEqual(self.request["status"], "returned")

    def test_card_cannot_be_returned_twice(self):
        approve_request(self.requests, "A001", "M01")
        issue_card(self.requests, "A001")
        return_card(self.requests, "A001")
        before = copy.deepcopy(self.request)

        success, message = return_card(self.requests, "A001")

        self.assertFalse(success)
        self.assertEqual(self.request, before)

    def test_unknown_request_id_is_rejected(self):
        before = copy.deepcopy(self.request)

        success, message = approve_request(
            self.requests, "A999", "M01"
        )

        self.assertFalse(success)
        self.assertIn("not found", message.lower())
        self.assertEqual(self.request, before)

    def test_returned_card_cannot_be_issued_again(self):
        approve_request(self.requests, "A001", "M01")
        issue_card(self.requests, "A001")
        return_card(self.requests, "A001")
        before = copy.deepcopy(self.request)

        success, message = issue_card(self.requests, "A001")

        self.assertFalse(success)
        self.assertEqual(self.request, before)

    def test_request_cannot_be_approved_twice(self):
        approve_request(self.requests, "A001", "M01")
        before = copy.deepcopy(self.request)

        success, message = approve_request(
            self.requests, "A001", "M02"
        )

        self.assertFalse(success)
        self.assertEqual(self.request, before)

    def test_issued_card_cannot_be_issued_twice(self):
        approve_request(self.requests, "A001", "M01")
        issue_card(self.requests, "A001")
        before = copy.deepcopy(self.request)

        success, message = issue_card(self.requests, "A001")

        self.assertFalse(success)
        self.assertEqual(self.request, before)


if __name__ == "__main__":
    unittest.main()

