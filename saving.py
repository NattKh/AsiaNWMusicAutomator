import json
import os
from customprint import custom_print

# Function to load resolution data from JSON file
def load_resolution_data():
    try:
        with open("resolution_data.json", "r") as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return None

# Load supported resolutions from JSON file
def load_supported_resolutions():
    try:
        with open("supported_resolutions.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Function to save resolution data to JSON file
def save_resolution_data(data, offset=None):
    supported_resolutions = load_supported_resolutions()
    resolution_str = f"{data['resolution'][0]}x{data['resolution'][1]}"

    if resolution_str in supported_resolutions:
        # If offset is provided, add it to the data
        if offset is not None:
            data['offset'] = offset

        with open("resolution_data.json", "w") as file:
            json.dump(data, file)
    else:
        custom_print(f"Resolution {resolution_str} is not supported. Not saving.")
# New function to save current GUI settings
def save_gui_settings(resolution, offset):
    data = {'resolution': resolution}
    save_resolution_data(data, offset)

# Function to load GUI settings
def load_gui_settings():
    data = load_resolution_data()
    if data:
        resolution = data.get('resolution', [1920, 1080])  # Default resolution
        offset = data.get('offset', 30)  # Default offset
        return resolution, offset
    else:
        return [1920, 1080], 30  # Default values

def get_image_path(folder_type, image_name):
    data = load_resolution_data()
    if not data or 'resolution' not in data or 'image_paths' not in data:
        custom_print("Error: Resolution data or image paths are not available.")
        return None

    resolution_str = f"{data['resolution'][0]}x{data['resolution'][1]}"
    folder_path = data['image_paths'].get(folder_type)
    if folder_path and resolution_str in folder_path:
        image_path = os.path.join(folder_type, resolution_str, image_name)
        return image_path
    else:
        custom_print(f"Error: No folder for resolution {resolution_str} in {folder_type}.")
        return None

def update_image_paths():
    base_dirs = ['images/buttons', 'images/play_area']
    resolution_dirs = {}

    for base_dir in base_dirs:
        if os.path.exists(base_dir):
            for item in os.listdir(base_dir):
                item_path = os.path.join(base_dir, item)
                if os.path.isdir(item_path):
                    resolution_dirs.setdefault(base_dir, []).append(item)

    data = load_resolution_data() or {}
    data['image_paths'] = resolution_dirs
    save_resolution_data(data)
