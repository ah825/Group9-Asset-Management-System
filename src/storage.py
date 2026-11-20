import json
from pathlib import Path
import os
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parent.parent

#Create storage file function
def init_storage(file_path=None):
    # makes sure that data is initialised in the correct place
    if file_path is None:
        path = PROJECT_ROOT / "data" / "assets.json"
    else:
        path = Path(file_path)

    try:
        #Create storage directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)

        #Create new storage file  if it doesn't exist
        with path.open("x", encoding="utf-8") as file:
            json.dump({"assets": []}, file, indent=4)

        return True

    except FileExistsError:
        #Preserve existing file
        if not path.is_file():
            return False

        return True


    except OSError as error:
        print(f"Unable to create storage: {error}")
        return False







#Save asset function
def save_asset(asset, file_path=None):
    required_fields = {
        "asset_id",
        "name",
        "category",
        "value",
        "status",
        "location"
    }

    # checks input is dict
    if not isinstance(asset, dict):
        return False

    # checks all fields are present
    if not required_fields.issubset(set(asset.keys())):
        return False

    #uses default path unless one is given
    if file_path is None:
        path = PROJECT_ROOT / "data" / "assets.json"
    else:
        path = Path(file_path)

    #reads data into Directory
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

    #returns false if file can't be read or if it contains invalid JSON
        if not isinstance(data, dict):
            return False

        if not isinstance(data.get("assets"), list):
            return False

    except (OSError, json.decoder.JSONDecodeError):
        return False

    #checks for duplicate asset id
    for existing_asset in data["assets"]:
        if existing_asset.get("asset_id") == asset["asset_id"]:
            return False


    #appends the asset to the file
    data["assets"].append(asset)
    temp_path = None

    #creates a temporary file thats in the same directory
    try:
        with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=path.parent,
                delete=False
        #writes updated asset records
        ) as temp_file:
            temp_path = Path(temp_file.name)
            json.dump(data, temp_file, indent=4)

        #replaces the original file after temp file is written
        os.replace(temp_path, path)
        return True

    #error handling
    except (OSError, TypeError, ValueError):
        return False

    #cleans up leftover temp file
    finally:
        if temp_path is not None:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass




def validate_asset(asset):
    required_fields = {
        "asset_id",
        "name",
        "category",
        "value",
        "status",
        "location"
    }

    #Check if asset is dict
    if not isinstance(asset, dict):
        return False, "Invalid asset input"

    #Check that all fields exist
    if not required_fields.issubset(set(asset.keys())):
        return False, "Invalid asset input"

    #Asset ID must be positive int
    if type(asset["asset_id"]) is not int or asset["asset_id"] <= 0:
        return False, "Invalid asset input"

    #Asset value must be non-negative num
    if type(asset["value"]) not in (int, float) or asset["value"] < 0:
        return False, "Invalid asset input"

    #Text fields must be non-empty str
    text_fields = ["name", "category", "status", "location"]
    for field in text_fields:
        if not isinstance(asset[field], str) or not asset[field].strip():
            return False, "Invalid asset input"

    return True, None


#user asset input
def add_asset():
    print("\n Add Asset")

    #Gets values from user
    asset = {
        "asset_id": input("Enter asset ID: "),
        "name": input("Enter asset name: "),
        "category": input("Enter asset category: "),
        "value": input("Enter asset value: "),
        "status": input("Enter asset status: "),
        "location": input("Enter asset location: "),
    }

    try:
        #converts into int and float
        asset["asset_id"] = int(asset["asset_id"])
        asset["value"] = float(asset["value"])
    except ValueError:
        print("Invalid asset input")
        return False

    #checks converted values
    valid, error = validate_asset(asset)

    if not valid:
        print(error)
        return False

    if save_asset(asset):
        print("Successfully saved asset")
        return True

    print("unable to save asset")
    return False
