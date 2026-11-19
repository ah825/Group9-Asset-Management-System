import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch
from src.storage import save_asset

class TestSaveAssetBlackbox(unittest.TestCase):

    #TC1, Missing required fields
    def test_missing_required_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) /"assets.json"

            with path.open("w", encoding="utf-8") as file:
                json.dump({"assets": []}, file)

            asset = {
                "asset_id": 1,
                "name": "Dell Laptop",
                "category": "Electronics",
                "value": 750,
                "status": "Available",
                #missing location
            }

            result = save_asset(asset, path)
            self.assertFalse(result)

            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            self.assertEqual(data["assets"], [])



    #TC2, Input is not a directory
    def test_not_a_dict(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"

            with path.open("w", encoding="utf-8") as file:
                json.dump({"assets": []}, file)

            asset = "Dell Laptop"

            result = save_asset(asset, path)
            self.assertFalse(result)
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            self.assertEqual(data["assets"], [])


    #TC3, Duplicate AssetID
    def test_duplicate_assets(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"

            existing_asset = {
                "asset_id": 1,
                "name": "Dell Laptop",
                "category": "Electronics",
                "value": 750,
                "status": "Available",
                "location": "Office"
            }

            with path.open("w", encoding="utf-8") as file:
                json.dump({"assets": [existing_asset]}, file)

            new_asset = existing_asset.copy()
            new_asset["name"] = "HP Laptop"

            result = save_asset(new_asset, path)


    #TC4, Missing sotrage file
    def test_missing_storage_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"

            asset = {
                "asset_id": 2,
                "name": "Keyboard",
                "category": "Electronics",
                "value": 50,
                "status": "Available",
                "location": "Office"
            }

            result = save_asset(asset, path)
            self.assertFalse(result)
            self.assertFalse(path.exists())


    #TC5, Invalid JSON
    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"

            invalid_content = "{invalid_json}"

            with path.open("w", encoding="utf-8") as file:
                file.write(invalid_content)

            asset = {
                "asset_id": 3,
                "name": "Monitor",
                "category": "Electronics",
                "value": 200,
                "status": "Available",
                "location": "Office"
            }

            result = save_asset(asset, path)
            self.assertFalse(result)

            with path.open("r", encoding="utf-8") as file:
                self.assertEqual(file.read(), invalid_content)


    #TC6, Filesystem Error
    def test_filesystem_error(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"

            with path.open("w", encoding="utf-8") as file:
                json.dump({"assets": []}, file)

            asset = {
                "asset_id": 4,
                "name": "Mouse",
                "category": "Electronics",
                "value": 25,
                "status": "Available",
                "location": "Office"
            }

            with patch("src.storage.os.replace", side_effect=OSError):
                result = save_asset(asset, path)
            self.assertFalse(result)



    #TC7, save valid asset
    def test_valid_asset(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"

            with path.open("w", encoding="utf-8") as file:
                json.dump({"assets": []}, file)

            asset = {
                "asset_id": 1,
                "name": "Dell Laptop",
                "category": "Electronics",
                "value": 750,
                "status": "Available",
                "location": "Office"
            }

            result = save_asset(asset, path)
            self.assertTrue(result)

            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            self.assertEqual(data["assets"], [asset])