import json
from pathlib import Path

def init_storage(file_path="data/assets.json"):
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