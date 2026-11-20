from storage import init_storage
from storage import init_storage, save_asset


init_storage()

from src.storage import validate_asset

asset = {
    "asset_id": 1,
    "name": "   ",
    "category": "Electronics",
    "value": 750,
    "status": "Available",
    "location": "Office"
}

print(validate_asset(asset))