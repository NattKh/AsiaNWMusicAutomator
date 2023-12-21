# customprint.py
from PyQt5.QtCore import QObject, pyqtSignal

is_game_playing = False
#global variable for game playing
# Global variable to control message printing
is_print_enabled = True  # Initially set to True

class CustomPrintEmitter(QObject):
    message_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def emit_message(self, message):
        self.message_signal.emit(message)

# Global instance of the emitter
emitter = CustomPrintEmitter()

last_printed_message = None

def custom_print(message):
    global last_printed_message, is_print_enabled

    message_str = str(message) if not isinstance(message, str) else message

    if message_str != last_printed_message:
        if is_print_enabled:
            print(message_str)
            emitter.emit_message(message_str)
        last_printed_message = message_str

# Function to toggle the print functionality
def toggle_print():
    global is_print_enabled
    is_print_enabled = not is_print_enabled
