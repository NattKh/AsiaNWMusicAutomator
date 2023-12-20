# customprint.py
from PyQt5.QtCore import QObject, pyqtSignal

is_game_playing = False
#global variable for game playing

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
    global last_printed_message
    # Convert the message to string if it's not already a string
    message_str = str(message) if not isinstance(message, str) else message

    if message_str != last_printed_message:
        print(message_str)
        last_printed_message = message_str
        emitter.emit_message(message_str)  # Emit the message as a string
