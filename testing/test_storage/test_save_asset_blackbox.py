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


    #WB TC1, Default storage path
    def test_default_storage_path(self):
        with tempfile.TemporaryDirectory() as temp:
            data_dir = Path(temp) / "data"
            data_dir.mkdir()
            path = data_dir / "assets.json"

            with path.open("w", encoding="utf-8") as file:
                json.dump({"assets": []}, file)

            asset = {
                "asset_id": 10,
                "name": "Keyboard",
                "category": "Electronics",
                "value": 50,
                "status": "Available",
                "location": "Office"
            }

            with patch("src.storage.PROJECT_ROOT", Path(temp)):
                result = save_asset(asset)
            self.assertTrue(result)

            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            self.assertEqual(data["assets"], [asset])


    #WB TC2, JSON root isnt directory
    def test_invalid_json_root(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"

            with path.open("w", encoding="utf-8") as file:
                json.dump(["Laptop", "Mouse"], file)

            asset = {
                "asset_id": 11,
                "name": "Keyboard",
                "category": "Electronics",
                "value": 50,
                "status": "Available",
                "location": "Office"
            }

            result = save_asset(asset, path)

            self.assertFalse(result)

            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            self.assertEqual(data, ["Laptop", "Mouse"])


    #WB TC3, invalid asset structure
    def test_invalid_asset_structure(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"

            invalid_data = {"assets": "not a list"}
            with path.open("w", encoding="utf-8") as file:
                json.dump(invalid_data, file)

            asset = {
                "asset_id": 12,
                "name": "Monitor",
                "category": "Electronics",
                "value": 200,
                "status": "Available",
                "location": "Office"
            }

            result = save_asset(asset, path)
            self.assertFalse(result)

            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            self.assertEqual(data, invalid_data)

    #WB TC4, duplicate ID after another asset
    def test_duplicate_id_after_asset(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"

            existing_assets = [
                {
                    "asset_id": 1,
                    "name": "Laptop",
                    "category": "Electronics",
                    "value": 750,
                    "status": "Available",
                    "location": "Office"
                },
                {
                    "asset_id": 2,
                    "name": "Monitor",
                    "category": "Electronics",
                    "value": 200,
                    "status": "Available",
                    "location": "Office"
                }
            ]

            with path.open("w", encoding="utf-8") as file:
                json.dump({"assets": existing_assets}, file)

            new_asset = existing_assets[1].copy()
            new_asset["name"] = "Another Monitor"

            result = save_asset(new_asset, path)
            self.assertFalse(result)
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            self.assertEqual(data["assets"], existing_assets)



    #WB TC5, Temp file cleanup failure
    def test_temp_file_cleanup_error(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "assets.json"

            with path.open("w", encoding="utf-8") as file:
                json.dump({"assets": []}, file)

            asset = {
                "asset_id": 20,
                "name": "Mouse",
                "category": "Electronics",
                "value": 25,
                "status": "Available",
                "location": "Office"
            }

            with patch("src.storage.Path.unlink",
                    side_effect=OSError("cleanup failed")):
                result = save_asset(asset, path)

            self.assertTrue(result)

            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            self.assertEqual(data["assets"], [asset])