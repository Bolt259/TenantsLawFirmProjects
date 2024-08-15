import json

# Step 1: Read the JSON file into a dictionary
def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Step 2: Edit the specific values in the dictionary
def edit_json(data, key, value):
    data[key] = value
    return data

# Step 3: Write the updated dictionary back to the JSON file
def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        
def func():
    """_summary_
    """
