import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def init_storage(file_path=None):
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

    except FileNotFoundError:
        #Preserve existing file
        return True

    except OSError as error:
        print("Unable to create storage {error}")
        return False