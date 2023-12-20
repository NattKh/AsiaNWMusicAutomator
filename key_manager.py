from cv2 import imread, imshow, cvtColor, COLOR_BGRA2BGR, waitKey, destroyAllWindows, matchTemplate, TM_CCOEFF_NORMED
from numpy import ndarray, array, where
from time import sleep
import mss.tools
from helpers.local_timer import *
from press_key.press_key import PressKey
from press_key.press_keyboard_key import PressKeyboardKey
from press_key.press_mouse_key import PressMouseKey
from saving import load_resolution_data
import saving
import resolution_monitor
import threading
import os
from customprint import custom_print, is_game_playing as is_game_playing
from PyQt5.QtCore import QObject, pyqtSignal
import tkinter as tk
from tkinter import simpledialog
import screeninfo
import time

class KeyManagerSignals(QObject):
    update_signal = pyqtSignal(dict)

class KeyManager:
    def __init__(self, loop_sleep=0.1, x_offset=60, game_monitor=1, use_virtual_keys=False):
        self.signals = KeyManagerSignals()  # Initialize signals first
        resolution_monitor.create_supported_resolutions_file()  # Create supported resolutions file


        # Initialize attributes
        self.last_printed_message = None
        self.loop_sleep = loop_sleep
        self.game_monitor = game_monitor
        self.use_virtual_keys = use_virtual_keys
        self.timer = Timer(duration_in_milliseconds=5000)
        self.monitor = None
        self.play_areas = {}
        self.press_key = None
        self.image = None
        self.is_game_playing = False

        # Initialize current_resolution
        existing_data = saving.load_resolution_data()
        self.current_resolution = existing_data.get('resolution') if existing_data else (1920, 1080)  # Default resolution
        # Initialize x_offset
        self.x_offset = x_offset  # Set a default value or load from configuration

        # Initialize _running and start the resolution monitoring thread
        self._running = True
        self.resolution_thread = threading.Thread(target=self.monitor_resolution_wrapper)
        self.resolution_thread.daemon = True
        self.resolution_thread.start()
        self._stop_requested = False

        # Load existing data
        existing_data = saving.load_resolution_data()
        if existing_data and 'resolution' in existing_data:
            self.current_resolution = existing_data['resolution']
        else:
            # Handle case where resolution is not available or incorrect
            custom_print("Warning: No valid resolution data found.")
        if not self.current_resolution:
            self.current_resolution = self.prompt_for_resolution()


        self.use_virtual_keys = existing_data.get("use_virtual_keys", False) if existing_data else False
        # Initialize paths and other attributes
        self.init_paths_and_attributes()

    def init_paths_and_attributes(self):
        if self.current_resolution:
            resolution_str = f"{self.current_resolution[0]}x{self.current_resolution[1]}"
            self.play_area_path = os.path.join('images', 'play_area', resolution_str)
            self.buttons_path = os.path.join('images', 'buttons', resolution_str)
            self.get_play_areas()  # Update play areas based on the new resolution
            self.emit_data()
        else:
            self.play_area_path = self.buttons_path = None


        # Initialize other attributes and call methods that might use emit_data
        self.get_play_areas()
        self.get_press_keys()
        self.emit_data()


    def prompt_for_resolution(self):
        """ Prompt the user to enter a resolution. """
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        resolution = simpledialog.askstring("Resolution", "Enter your resolution (e.g., 1920x1080):")
        root.destroy()

        if resolution and 'x' in resolution:
            width, height = resolution.split('x')
            return int(width), int(height)
        else:
            return None  # Handle invalid input

    def update_image_paths(self):
        data = saving.load_resolution_data()
        self.current_resolution = data.get('resolution')
        resolution_str = f"{self.current_resolution[0]}x{self.current_resolution[1]}" if self.current_resolution else "default"

        self.play_area_path = os.path.join('images', 'play_area', resolution_str)
        self.buttons_path = os.path.join('images', 'buttons', resolution_str)
        custom_print(f"Play area path: {self.play_area_path}")  # Debug print
        custom_print(f"Buttons path: {self.buttons_path}")  # Debug print
        self.emit_data()
        
    def request_stop(self):
        self._stop_requested = True  # Signal to stop the main loop

    def monitor_updater(self):
        while self._running:
            existing_data = saving.load_resolution_data()
            if existing_data and 'resolution' in existing_data:
                if tuple(existing_data['resolution']) != tuple(self.current_resolution):
                    self.current_resolution = existing_data['resolution']
                    self.init_paths_and_attributes()  # Reinitialize paths and other settings
                    custom_print(f"Resolution updated to: {self.current_resolution}")
                    resolution_monitor.monitor_resolution(interval=5)
                    self.emit_data()
            time.sleep(5)  # Check every 5 seconds, adjust as needed

    def monitor_resolution_wrapper(self):
        resolution_monitor.monitor_resolution(interval=5)
        self.emit_data()
        self.monitor_updater()

    def check_and_update_play_areas(self):
        existing_data = saving.load_resolution_data()
        if existing_data and 'resolution' in existing_data:
            if tuple(existing_data['resolution']) != tuple(self.current_resolution):
                self.current_resolution = existing_data['resolution']
                self.init_paths_and_attributes()
                custom_print(f"Resolution updated to: {self.current_resolution}")
                self.emit_data()

    def step_one(self) -> None:
        # Call methods to set up play areas and press keys
        self.get_play_areas()
        self.get_press_keys()

    def reset(self):
        # Reset variables to their initial states
        self.play_areas = {}
        self.press_key = None
        self.image = None
        


    def check_for_key_presses(self) -> None:
        for key in self.press_key:
            self.press_key[key].check_press_key_trigger(master_image=self.image)

    def get_play_areas(self):
        area_keys = ['novice', 'skilled', 'expert']
        self.play_areas = {}
        all_files_found = True

        for key in area_keys:
            image_path = os.path.join(self.play_area_path, f'{key}.png')
            if os.path.exists(image_path):
                self.play_areas[key] = imread(image_path)
            else:
                custom_print(f"File not found: {image_path}")
                all_files_found = False
        custom_print(f"Play areas updated for resolution {self.current_resolution}. All files found: {all_files_found}")
        self.emit_data()


    def get_press_keys(self):
        keys = ['w', 'a', 's', 'd', 'space', 'mouse']
        file_mappings = {
            'space': 'space_bar.png',
            'mouse': 'both_mouse_buttons.png'
        }
        self.press_key = {}
        all_files_found = True

        for key in keys:
            image_file = file_mappings.get(key, f'{key}.png')
            image_path = os.path.join(self.buttons_path, image_file)
            self.emit_data()
            if os.path.exists(image_path):
                if key == 'mouse':
                    self.press_key['key_mouse'] = PressMouseKey(
                        image=imread(image_path),
                        button=['left', 'right'],
                        timer_milliseconds=200,
                        use_vk=self.use_virtual_keys,
                        master_timer=self.timer
                    )
                else:
                    self.press_key[f'key_{key}'] = PressKeyboardKey(
                        letter=key,
                        timer_milliseconds=200,
                        image=imread(image_path),
                        use_vk=self.use_virtual_keys,
                        master_timer=self.timer
                    )
            else:
                custom_print(f"File not found: {image_path}")
                all_files_found = False

        custom_print(f"Press keys updated for resolution {self.current_resolution}. All files found: {all_files_found}")



    def find_monitor_rect(self) -> None:
        for difficulty in self.play_areas:
            with mss.mss() as screen_shot:
                monitor: dict[str, int] = screen_shot.monitors[self.game_monitor]
                master_image: ndarray = array(screen_shot.grab(monitor))
                master_image: ndarray = cvtColor(master_image, COLOR_BGRA2BGR)

                slave_image: ndarray = self.play_areas[difficulty]

                res_s: float = matchTemplate(master_image, slave_image, TM_CCOEFF_NORMED)
                threshold: float = 0.8
                loc: ndarray = where(res_s >= threshold)

                if len(loc[0]) > 0:
                    # Set the x_offset to the width of the found template image plus a small buffer
                    self.x_offset = slave_image.shape[1] + 30  # Adding a 10-pixel buffer for example
                    
                    self.monitor: dict[str, int] = {
                        'left': loc[1][0],
                        'top': loc[0][0],
                        'height': slave_image.shape[0],
                        'width': self.x_offset
                    }
                    self.timer.activate()
                    custom_print(f"Found match for {difficulty} and set x_offset to {self.x_offset}")
                    self.emit_data()
                    return
                else:
                    #custom_print(f"No match found for {difficulty}.")
                    return



    def update_monitor_area(self, additional_offset=0):
        # Ensure the latest resolution data is loaded
        existing_data = saving.load_resolution_data()
        if existing_data and 'resolution' in existing_data:
            if tuple(existing_data['resolution']) != tuple(self.current_resolution):
                self.current_resolution = existing_data['resolution']
                self.init_paths_and_attributes()

        # Attempt to find the monitor area
        for difficulty in self.play_areas:
            with mss.mss() as screen_shot:
                monitor = screen_shot.monitors[self.game_monitor]
                master_image = array(screen_shot.grab(monitor))
                master_image = cvtColor(master_image, COLOR_BGRA2BGR)

                slave_image = self.play_areas[difficulty]
                res_s = matchTemplate(master_image, slave_image, TM_CCOEFF_NORMED)
                threshold = 0.8
                loc = where(res_s >= threshold)

                if len(loc[0]) > 0:
                    # Adding a 30-pixel buffer plus the additional offset from the GUI
                    self.x_offset = slave_image.shape[1] + 30 + additional_offset
                    self.monitor = {'left': loc[1][0], 'top': loc[0][0], 'height': slave_image.shape[0], 'width': self.x_offset}
                    self.timer.activate()
                    custom_print(f"Found match for {difficulty} and set x_offset to {self.x_offset}")
                    self.emit_data()
                    self.is_game_playing = True  # Game is being played
                    return  # Found a match, no need to continue
                else:
                    custom_print(f"No match found for {difficulty}.")
                    self.emit_data()
        # No match found for any difficulty
        custom_print("No match found in any play area.")



    def update_x_offset(self, new_offset):
        self.x_offset = new_offset
        custom_print(f"x_offset updated to {new_offset}")

    def setup_play_areas(self):
        self.get_play_areas()

    def find_monitor_rectangle(self):
        if self.monitor is None:
            self.find_monitor_rect()

    def main_loop(self):
        self._running = True  # Ensure loop can run
        try:
            while self._running:
                self.check_and_update_play_areas()  # Check and update resolution and play areas

                # Reload resolution data in case it has changed
                existing_data = saving.load_resolution_data()
                self.emit_data()

                if existing_data and 'resolution' in existing_data:
                    if tuple(existing_data['resolution']) != tuple(self.current_resolution):
                        self.current_resolution = existing_data['resolution']
                        self.init_paths_and_attributes()

                if not self.timer.active:
                    self.update_monitor_area()

                if self.timer.active:
                    with mss.mss() as screen_shot:
                        if self.monitor:
                            self.image = array(screen_shot.grab(self.monitor))
                            self.image = cvtColor(self.image, COLOR_BGRA2BGR)
                            self.check_for_key_presses()
                # Check the running flag at the end of the loop
                if not self._running:
                    custom_print("self running set to false breaking loop")
                    self._running = False
                    break
        except KeyboardInterrupt:
            pass  # Handle KeyboardInterrupt if necessary
        finally:
            # Perform any necessary cleanup here
            custom_print("Exiting main loop")
            self._running = False


    def stop(self):
        self._running = False  # Method to stop the main loop


    def emit_data(self):
        data = {
            "current_resolution": self.current_resolution,
            "play_area_path": self.play_area_path,
            "buttons_path": self.buttons_path,
            "play_area_resolution": self.get_play_area_resolution(),  # Assuming this method exists
            "match_info": self.get_match_info()  # Assuming this method exists
        }
        self.signals.update_signal.emit(data)

    def get_play_area_resolution(self):
        if self.play_areas:
            # Example: assuming the first key has the representative resolution
            first_key = next(iter(self.play_areas))
            image = self.play_areas[first_key]
            return f"{image.shape[1]}x{image.shape[0]}"  # Width x Height
        else:
            return "Resolution not available"


    def get_match_info(self):
        if self.monitor:
            return f"Match found at {self.monitor['left']}, {self.monitor['top']} with offset {self.x_offset}"
        else:
            return "No match found"


if __name__ == "__main__":
    key_manager = KeyManager()
    key_manager.main_loop()
