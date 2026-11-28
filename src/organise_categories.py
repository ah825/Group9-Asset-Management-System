import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def organise_categories():
    file_path = f"{PROJECT_ROOT}/data/assets.json"

    with open(file_path, 'r') as file:
        data = json.load(file)
        print(data)

print(organise_categories())