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
                self.assertEqual(json.load(file), {"assets: []"})

    #TC2, Directory exists but file is missing
    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"

            result = init_storage(path)

            self.assertTrue(result)
            self.assertTrue(path.parent.is_file())

    #TC3, File already exists
    def test_existing_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"
            original = '{"assets": []}'
            path.write_text(original, encoding="utf-8")
