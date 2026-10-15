
import unittest

from campus_access import requests


class TestRequests(unittest.TestCase):

    def setUp(self):
        requests.reset_requests()

    def test_create_valid_request(self):
        result = requests.create_request("FELLOW-01", "student")

        self.assertEqual(result["id"], "A001")
        self.assertEqual(result["fellow_id"], "FELLOW-01")
        self.assertEqual(result["card_type"], "student")
        self.assertEqual(result["status"], "requested")
        self.assertIsNone(result["approved_by"])

    def test_reject_blank_fellow_id(self):
        with self.assertRaises(ValueError):
            requests.create_request("   ", "student")

    def test_reject_non_string_fellow_id(self):
        with self.assertRaises(ValueError):
            requests.create_request(123, "student")

    def test_reject_invalid_card_type(self):
        with self.assertRaises(ValueError):
            requests.create_request("FELLOW-01", "guest")

    def test_reject_non_string_card_type(self):
        with self.assertRaises(ValueError):
            requests.create_request("FELLOW-01", None)

    def test_normalize_card_type(self):
        result = requests.create_request("FELLOW-01", "  STUDENT ")
        self.assertEqual(result["card_type"], "student")

    def test_generate_sequential_ids(self):
        first = requests.create_request("FELLOW-01", "student")
        second = requests.create_request("FELLOW-02", "staff")

        self.assertEqual(first["id"], "A001")
        self.assertEqual(second["id"], "A002")

    def test_next_id_uses_highest_existing_number(self):
        requests.reset_requests([
            {
                "id": "A001",
                "fellow_id": "FELLOW-01",
                "card_type": "student",
                "status": "requested",
                "approved_by": None,
            },
            {
                "id": "A003",
                "fellow_id": "FELLOW-03",
                "card_type": "staff",
                "status": "requested",
                "approved_by": None,
            },
        ])

        result = requests.create_request("FELLOW-04", "visitor")
        self.assertEqual(result["id"], "A004")

    def test_get_existing_request(self):
        created = requests.create_request("FELLOW-01", "visitor")

        found = requests.get_request("A001")

        self.assertEqual(found, created)

    def test_unknown_request_raises_key_error(self):
        with self.assertRaises(KeyError):
            requests.get_request("A001")

    def test_reject_malformed_request_ids(self):
        invalid_ids = [
            "A1",
            "A01",
            "A000",
            "B001",
            "A-01",
            "A１２３",
            "",
            123,
        ]

        for request_id in invalid_ids:
            with self.subTest(request_id=request_id):
                with self.assertRaises(ValueError):
                    requests.validate_request_id(request_id)

    def test_reject_duplicate_ids_in_dataset(self):
        record = {
            "id": "A001",
            "fellow_id": "FELLOW-01",
            "card_type": "student",
            "status": "requested",
            "approved_by": None,
        }

        with self.assertRaises(ValueError):
            requests.validate_dataset([record, record.copy()])

    def test_reject_record_with_missing_key(self):
        record = {
            "id": "A001",
            "fellow_id": "FELLOW-01",
            "card_type": "student",
            "status": "requested",
        }

        with self.assertRaises(ValueError):
            requests.validate_request_record(record)

    def test_reject_invalid_stored_status(self):
        record = {
            "id": "A001",
            "fellow_id": "FELLOW-01",
            "card_type": "student",
            "status": "pending",
            "approved_by": None,
        }

        with self.assertRaises(ValueError):
            requests.validate_request_record(record)


if __name__ == "__main__":
    unittest.main()
