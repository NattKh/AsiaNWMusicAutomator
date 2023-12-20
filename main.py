import saving 
from key_manager import KeyManager
from helpers.settings import USE_VIRTUAL_KEYS, LOOP_SLEEP, GAME_MONITOR, X_OFFSET
from helpers.settings import GAME_TITLE, BUILD_NUMBER_MAJOR, BUILD_NUMBER_MINOR, BUILD_NUMBER_REVISION
import get_window
from customprint import custom_print  # Import custom_print function

def main():
    process_name = "NewWorld.exe"
    resolution = get_window.get_window_by_process_name(process_name)

    if not resolution:
        title = "New World"
        resolution = get_window.get_window_by_title(title)

    if resolution:
        get_window.activate_window_by_process_name(process_name)
        custom_print(f"Detected game resolution: {resolution[0]}x{resolution[1]}")
        
        existing_data = saving.load_resolution_data() or {}
        current_resolution = existing_data.get("resolution")

        if tuple(resolution) != tuple(current_resolution):
            custom_print("Detected resolution is different from existing data.")
            existing_data["resolution"] = tuple(resolution)
            saving.save_resolution_data(existing_data)
        else:
            custom_print("Detected resolution is same as in existing data.")  # Debug print
    else:
        custom_print(f"Game window '{process_name}' not found.")

if __name__ == '__main__':
    updated_data = saving.load_resolution_data()
    key_manager = KeyManager(loop_sleep=LOOP_SLEEP, 
                             x_offset=X_OFFSET,
                             game_monitor=GAME_MONITOR, 
                             use_virtual_keys=USE_VIRTUAL_KEYS)
    custom_print(f'Welcome Setting up.')
    key_manager.main_loop()


    