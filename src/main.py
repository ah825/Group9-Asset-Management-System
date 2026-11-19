from storage import init_storage
from storage import init_storage, save_asset


init_storage()

asset = {
    "asset_id": 1,
    "name": "Dell Laptop",
    "category": "Electronics",
    "value": 750.00,
    "status": "Available",
    "location": "Office"
}

result = save_asset(asset)
print("asset saved:", result)