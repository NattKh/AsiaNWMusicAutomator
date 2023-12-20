import time
from get_window import get_window_by_process_name, get_window_by_title
import saving
from customprint import custom_print
import ctypes
from ctypes import wintypes
import json

def create_supported_resolutions_file():
    supported_resolutions = [
        "1280x720", "1366x768", "1600x900", "1920x1080",
        "2560x1440", "3440x1440", "3840x2160", "4096x2160",
        "5120x2880", "7680x4320", "5120x2160", "3840x1600",
        "2560x1080", "3840x1200", "3840x1080"
    ]
    
    with open("supported_resolutions.json", "w") as file:
        json.dump(supported_resolutions, file, indent=4)


# Constants from the Windows API
SM_CXSIZEFRAME = 32
SM_CYSIZEFRAME = 33
SM_CYCAPTION = 4

def get_window_border_size():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    border_width = user32.GetSystemMetrics(SM_CXSIZEFRAME)
    border_height = user32.GetSystemMetrics(SM_CYSIZEFRAME)
    title_bar_height = user32.GetSystemMetrics(SM_CYCAPTION)
    return border_width, border_height, title_bar_height

def load_supported_resolutions():
    try:
        with open("supported_resolutions.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def find_closest_resolution(resolution, supported_resolutions):
    def resolution_distance(res):
        res_width, res_height = map(int, res.split('x'))
        return abs(res_width - resolution[0]) + abs(res_height - resolution[1])

    closest = None
    min_distance = float('inf')
    for res in supported_resolutions:
        distance = resolution_distance(res)
        if distance < min_distance:
            min_distance = distance
            closest = res
    return closest

def monitor_resolution(interval=5):
    supported_resolutions = load_supported_resolutions()
    while True:
        process_name = "NewWorld.exe"
        pre_resolution = get_window_by_process_name(process_name)

        if not pre_resolution:
            title = "New World"
            pre_resolution = get_window_by_title(title)

        if pre_resolution:
            border_width, border_height, title_bar_height = get_window_border_size()
            adjusted_resolution = (pre_resolution[0] - 2 * border_width, pre_resolution[1] - title_bar_height)
            closest_resolution = find_closest_resolution(adjusted_resolution, supported_resolutions)

            if closest_resolution:
                current_resolution = tuple(map(int, closest_resolution.split('x')))
                existing_data = saving.load_resolution_data() or {}
                
                # Update resolution only if it's different from the existing resolution
                if current_resolution != existing_data.get("resolution"):
                    #custom_print(f"Adjusted to closest supported resolution: {closest_resolution}, Current resolution: {current_resolution}")
                    existing_data["resolution"] = current_resolution
                    saving.save_resolution_data(existing_data)
                else:
                    custom_print(f"Current resolution {current_resolution} is already set. No update needed.")

        time.sleep(interval)

if __name__ == "__main__":
    monitor_resolution()
