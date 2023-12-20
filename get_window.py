import pyautogui as pyAG
import pygetwindow as gw  # Import pygetwindow library
from customprint import custom_print

screen_width, screen_height = pyAG.size()  # Screen

def cursor_to_screen():
    pyAG.moveTo(screen_width / 2, screen_height / 3)

def get_window_by_process_name(process_name):
    try:
        # Get the window by its process name
        window = gw.getWindowsWithTitle(process_name)[0]
        return window.width, window.height  # Return window width and height as resolution
    except IndexError:
        return None

def get_window_by_title(title):
    try:
        # Get the window by its title (backup method)
        window = pyAG.getWindowsWithTitle(title)[0]
        return window.width, window.height  # Return window width and height as resolution
    except IndexError:
        return None

def activate_window_by_process_name(process_name):
    try:
        # Activate the window by its process name
        window = gw.getWindowsWithTitle(process_name)[0]
        window.activate()
    except IndexError:
        return None

# Usage example:
if __name__ == "__main__":
    process_name = "NewWorld.exe"  # Replace with your game's process name
    resolution = get_window_by_process_name(process_name)

    if not resolution:
        # If the process name doesn't work, try using the title as a backup
        title = "New World"  # Replace with your game's window title
        resolution = get_window_by_title(title)

    if resolution:
        # Activate the game window to ensure it's in focus
        activate_window_by_process_name(process_name)
        custom_print(f"Detected game resolution: {resolution[0]}x{resolution[1]}")
