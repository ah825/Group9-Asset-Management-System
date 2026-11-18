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
