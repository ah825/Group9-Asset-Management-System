import json
import tempfile
import unittest
from pathlib import Path

from src.storage import init_storage

class TestStorageBlackbox(unittest.TestCase):

    #TC1, Directory and file are missing
    def test_missing_directory_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "data" / "assets.json"

            result = init_storage(path)

            self.assertTrue(result)
            self.assertTrue(path.parent.is_dir())
            self.assertTrue(path.is_file())

            with path.open("r", encoding="utf-8") as file:
                self.assertEqual(json.load(file), {"assets": []})

    #TC2, Directory exists but file is missing
    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"

            result = init_storage(path)

            self.assertTrue(result)
            self.assertTrue(path.is_file())

    #TC3, File already exists
    def test_existing_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"
            original = '{"assets": []}'
            path.write_text(original, encoding="utf-8")

    #TC4, Existing file contains asset records
    def test_existing_file_with_assets(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"

            original = '{"assets": [{asset_id": "A001"}]}'
            path.write_text(original, encoding="utf-8")

            result = init_storage(path)

            self.assertTrue(result)
            self.assertEqual(path.read_text(encoding="utf-8"), original)


    #TC5, Existing file contains invalid JSON
    def test_existing_invalid_json(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"

            original = "{invalid json}"
            path.write_text(original, encoding="utf-8")

            result = init_storage(path)

            self.assertTrue(result)
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    #TC6, a file blocks directory creation
    def test_directory_creation_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            blocker = Path(temp) / "data"
            blocker.write_text("blocking directory", encoding="utf-8")

            path = blocker / "assets.json"
            result = init_storage(path)
            self.assertFalse(result)

    #TC7, file blocks creation of storage directory
    def test_nested_directory_creation_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            blocker = Path(temp) / "blocked"
            blocker.write_text("blocking directory", encoding="utf-8")

            path = blocker / "nested" / "assets.json"

            result = init_storage(path)
            self.assertFalse(result)