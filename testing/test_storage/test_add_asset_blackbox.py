import unittest
from src.storage import validate_asset
from unittest.mock import patch
from src.storage import add_asset

class test_add_asset_blackbox(unittest.TestCase):

    #TC1, missing fields
    def test_missing_required_fields(self):
        asset = {
            "asset_id": 2,
            "name": "HP Laptop",
            "category": "Electronics",
            "value": 650,
            "status": "Available"
        }

        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))

    #TC2, input not a dict
    def test_not_a_dictionary(self):
        asset = "Dell Laptop"

        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))


    #TC3, test invalid asset ID
    def test_zero_or_negative_asset_id(self):
        asset = {
            "asset_id": 0,
            "name": "Dell Laptop",
            "category": "Electronics",
            "value": 750,
            "status": "Available",
            "location": "Office"
        }

        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))

        #check negative ID
        asset["asset_id"] = -5
        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))


    #TC4, invalid ID type
    def test_invalid_asset_id_type(self):
        asset = {
            "asset_id": "ABC",
            "name": "Dell Laptop",
            "category": "Electronics",
            "value": 750,
            "status": "Available",
            "location": "Office"
        }

        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))

        #check decimal ID
        asset["asset_id"] = 2.5
        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))

        #check boolean ID
        asset["asset_id"] = True
        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))


    #TC5, negative asset values
    def test_negative_asset_value(self):
        asset = {
            "asset_id": 3,
            "name": "Dell Laptop",
            "category": "Electronics",
            "value": -100,
            "status": "Available",
            "location": "Office"
        }

        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))

        #check negative decimal value
        asset["value"] = -50.5
        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))


    #TC6, invalid value
    def test_invalid_asset_value_type(self):
        asset = {
            "asset_id": 4,
            "name": "Dell Laptop",
            "category": "Electronics",
            "value": "ABC",
            "status": "Available",
            "location": "Office"
        }

        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))

        #check boolean value
        asset["value"] = True
        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))

        #check list value
        asset["value"] = [100]
        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))


    #TC7, non-finite asset val
    def test_non_finite_asset_value(self):
        asset = {
            "asset_id": 5,
            "name": "Dell Laptop",
            "category": "Electronics",
            "value": float("nan"),
            "status": "Available",
            "location": "Office"
        }

        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))

        #check positive infinity
        asset["value"] = float("inf")
        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))

        #check negative infinity
        asset["value"] = float("-inf")
        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))


    #TC8, empty fields
    def test_empty_text_fields(self):
        asset = {
            "asset_id": 6,
            "name": "",
            "category": "Electronics",
            "value": 750,
            "status": "Available",
            "location": "Office"
        }

        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))

        #check whitespace-only
        asset["name"] = "   "
        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))


    #TC9, invalid text field type
    def test_invalid_text_field_type(self):
        asset = {
            "asset_id": 7,
            "name": 123,
            "category": "Electronics",
            "value": 750,
            "status": "Available",
            "location": "Office"
        }

        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))

        #check list instead of string
        asset["name"] = ["Dell Laptop"]
        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))

        #heck None instead of string
        asset["name"] = None
        result = validate_asset(asset)
        self.assertEqual(result, (False, "Invalid asset input"))


    #TC10, valid asset
    def test_valid_asset(self):
        asset = {
            "asset_id": 1,
            "name": "Dell Laptop",
            "category": "Electronics",
            "value": 750,
            "status": "Available",
            "location": "Office"
        }

        result = validate_asset(asset)
        self.assertEqual(result, (True, None))





    #TC11, add asset valid input
    def test_add_asset_valid_input(self):
        user_inputs = [
            "10",
            "Dell Laptop",
            "Electronics",
            "750",
            "Available",
            "Office"
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("src.storage.save_asset", return_value=True) as mock_save:
                result = add_asset()
        self.assertTrue(result)

        expected_asset = {
            "asset_id": 10,
            "name": "Dell Laptop",
            "category": "Electronics",
            "value": 750.0,
            "status": "Available",
            "location": "Office"
        }
        mock_save.assert_called_once_with(expected_asset)


    #TC12, invalid asset ID
    def test_add_asset_invalid_numeric_input(self):
        user_inputs = [
            "abc",
            "Dell Laptop",
            "Electronics",
            "750",
            "Available",
            "Office"
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("src.storage.save_asset") as mock_save:
                result = add_asset()

        self.assertFalse(result)
        mock_save.assert_not_called()


    #TC13, input fails validation
    def test_add_asset_validation_failure(self):
        user_inputs = [
            "11",
            "HP Laptop",
            "Electronics",
            "-100",
            "Available",
            "Office"
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("src.storage.save_asset") as mock_save:
                result = add_asset()
        self.assertFalse(result)
        mock_save.assert_not_called()


    #TC14, save fails
    def test_add_asset_save_failure(self):
        user_inputs = [
            "12",
            "Dell Monitor",
            "Electronics",
            "200",
            "Available",
            "Office"
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("src.storage.save_asset", return_value=False) as mock_save:
                result = add_asset()
        self.assertFalse(result)
        mock_save.assert_called_once()