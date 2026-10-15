
"""Tests for campus access-card workflow rules."""

import copy
import unittest

from campus_access.workflow import (
    approve_request,
    issue_card,
    return_card,
)


class TestAccessCardWorkflow(unittest.TestCase):
    def setUp(self):
        """Create isolated test requests for each test."""
        self.request = {
            "id": "A001",
            "fellow_id": "F001",
            "card_type": "student",
            "status": "requested",
            "approved_by": None,
        }
        self.requests = [self.request]

    def test_new_request_starts_requested(self):
        self.assertEqual(self.request["status"], "requested")
        self.assertIsNone(self.request["approved_by"])

    def test_valid_approver_can_approve(self):
        approve_request(self.requests, "A001", "M01")

        self.assertEqual(self.request["status"], "approved")
        self.assertEqual(self.request["approved_by"], "M01")

    def test_empty_approver_is_rejected(self):
        for approver in ("", "   "):
            with self.subTest(approver=repr(approver)):
                before = copy.deepcopy(self.request)

                with self.assertRaises(ValueError):
                    approve_request(self.requests, "A001", approver)

                self.assertEqual(self.request, before)

    def test_issuing_before_approval_is_rejected(self):
        before = copy.deepcopy(self.request)

        with self.assertRaises(ValueError):
            issue_card(self.requests, "A001")

        self.assertEqual(self.request, before)

    def test_approved_request_can_be_issued(self):
        approve_request(self.requests, "A001", "M01")
        issue_card(self.requests, "A001")

        self.assertEqual(self.request["status"], "issued")
        self.assertEqual(self.request["approved_by"], "M01")

    def test_issued_request_can_be_returned(self):
        approve_request(self.requests, "A001", "M01")
        issue_card(self.requests, "A001")
        return_card(self.requests, "A001")

        self.assertEqual(self.request["status"], "returned")

    def test_returning_twice_is_rejected(self):
        approve_request(self.requests, "A001", "M01")
        issue_card(self.requests, "A001")
        return_card(self.requests, "A001")
        before = copy.deepcopy(self.request)

        with self.assertRaises(ValueError):
            return_card(self.requests, "A001")

        self.assertEqual(self.request, before)

    def test_unknown_request_id_is_rejected(self):
        before = copy.deepcopy(self.request)

        with self.assertRaises(KeyError):
            approve_request(self.requests, "A999", "M01")

        self.assertEqual(self.request, before)

    def test_returned_card_cannot_be_issued_again(self):
        approve_request(self.requests, "A001", "M01")
        issue_card(self.requests, "A001")
        return_card(self.requests, "A001")
        before = copy.deepcopy(self.request)

        with self.assertRaises(ValueError):
            issue_card(self.requests, "A001")

        self.assertEqual(self.request, before)

    def test_approving_twice_is_rejected_without_changes(self):
        approve_request(self.requests, "A001", "M01")
        before = copy.deepcopy(self.request)

        with self.assertRaises(ValueError):
            approve_request(self.requests, "A001", "M02")

        self.assertEqual(self.request, before)

    def test_issued_card_cannot_be_issued_twice(self):
        approve_request(self.requests, "A001", "M01")
        issue_card(self.requests, "A001")
        before = copy.deepcopy(self.request)

        with self.assertRaises(ValueError):
            issue_card(self.requests, "A001")

        self.assertEqual(self.request, before)

    def test_return_before_issuing_is_rejected(self):
        before = copy.deepcopy(self.request)

        with self.assertRaises(ValueError):
            return_card(self.requests, "A001")

        self.assertEqual(self.request, before)


if __name__ == "__main__":
    unittest.main()
