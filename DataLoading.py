import os
import json

def storeDict(data_dict, filename):
    filename = os.path.basename(filename)
    if filename == '' or filename.startswith('.'):
        raise ValueError("Invalid filename")

    os.makedirs('data', exist_ok=True)

    with open(os.path.join('data', filename), 'w') as f:
        json.dump(data_dict, f)

def LoadDict(filename):
    with open(filename, 'r') as f:
        return json.load(f)