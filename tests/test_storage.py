import json
import tempfile
import unittest
from pathlib import Path

from campus_access import requests, storage


class TestStorage(unittest.TestCase):

    def setUp(self):
        requests.reset_requests()
        self.temp_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)
        self.folder = Path(self.temp_directory.name)
        self.file_path = self.folder / "requests.json"

    def test_save_and_reload_requests(self):
        requests.create_request("FELLOW-01", "student")
        requests.create_request("FELLOW-02", "visitor")

        storage.save_requests(self.file_path)
        requests.reset_requests()
        storage.load_requests(self.file_path)

        self.assertEqual(len(requests.REQUESTS), 2)
        self.assertEqual(requests.get_request("A001")["card_type"], "student")
        self.assertEqual(requests.get_request("A002")["card_type"], "visitor")

    def test_id_remains_unique_after_reload(self):
        requests.create_request("FELLOW-01", "student")
        storage.save_requests(self.file_path)

        requests.reset_requests()
        storage.load_requests(self.file_path)

        new_request = requests.create_request("FELLOW-02", "staff")
        self.assertEqual(new_request["id"], "A002")

    def test_missing_file_starts_empty(self):
        requests.create_request("FELLOW-01", "student")

        storage.load_requests(self.folder / "missing.json")

        self.assertEqual(requests.REQUESTS, [])

    def test_corrupt_json_does_not_clear_current_data(self):
        requests.create_request("FELLOW-01", "student")
        self.file_path.write_text("{broken JSON", encoding="utf-8")

        with self.assertRaises(ValueError):
            storage.load_requests(self.file_path)

        self.assertEqual(len(requests.REQUESTS), 1)
        self.assertEqual(requests.REQUESTS[0]["id"], "A001")

    def test_missing_key_does_not_replace_current_data(self):
        requests.create_request("FELLOW-01", "student")

        invalid_data = [{
            "id": "A002",
            "fellow_id": "FELLOW-02",
            "card_type": "staff",
            "status": "requested",
        }]
        self.file_path.write_text(
            json.dumps(invalid_data), encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            storage.load_requests(self.file_path)

        self.assertEqual(len(requests.REQUESTS), 1)
        self.assertEqual(requests.REQUESTS[0]["id"], "A001")

    def test_duplicate_ids_are_rejected(self):
        record = {
            "id": "A001",
            "fellow_id": "FELLOW-01",
            "card_type": "student",
            "status": "requested",
            "approved_by": None,
        }

        self.file_path.write_text(
            json.dumps([record, record.copy()]), encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            storage.load_requests(self.file_path)

    def test_invalid_card_type_is_rejected(self):
        record = {
            "id": "A001",
            "fellow_id": "FELLOW-01",
            "card_type": "guest",
            "status": "requested",
            "approved_by": None,
        }

        self.file_path.write_text(
            json.dumps([record]), encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            storage.load_requests(self.file_path)

    def test_invalid_status_is_rejected(self):
        record = {
            "id": "A001",
            "fellow_id": "FELLOW-01",
            "card_type": "student",
            "status": "waiting",
            "approved_by": None,
        }

        self.file_path.write_text(
            json.dumps([record]), encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            storage.load_requests(self.file_path)

    def test_non_list_json_is_rejected(self):
        self.file_path.write_text(
            json.dumps({"id": "A001"}), encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            storage.load_requests(self.file_path)

    def test_failed_save_raises_error(self):
        requests.create_request("FELLOW-01", "student")

        # A directory cannot be used as a regular JSON file.
        directory_path = self.folder / "destination"
        directory_path.mkdir()

        with self.assertRaises(OSError):
            storage.save_requests(directory_path)


if __name__ == "__main__":
    unittest.main()
