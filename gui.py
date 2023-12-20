import sys
import threading
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QLabel, QSpinBox, QSlider, QShortcut
from PyQt5.QtCore import pyqtSignal, QObject, QTimer, Qt
from PyQt5.QtGui import QTextCursor, QKeySequence
import subprocess
from key_manager import KeyManager
from customprint import emitter, custom_print
import time
import saving  # Import your saving module

# Import the main function from main.py
import main
from helpers.local_timer import Timer

class ScriptThread(threading.Thread):
    def __init__(self, output_signal, key_manager):
        threading.Thread.__init__(self)
        self.output_signal = output_signal
        self.key_manager = key_manager
        self._running = True

    def run(self):
        print("ScriptThread KeyManager instance: ", id(self.key_manager))
        try:
            sys.stdout.write = self.custom_write
            while True:
                if self._running:
                    print("ScriptThread is running")
                    self.key_manager.main_loop()
                else:
                    print("ScriptThread is stopped")
                    # Add any logic here for when the thread is stopped
                    break  # Exit the while loop when _running is False
        finally:
            sys.stdout.write = sys.__stdout__.write
            print("Exiting ScriptThread run method")

    def custom_write(self, text):
        self.output_signal.emit(text)

    def stop(self):
        if self.key_manager:
            self.key_manager.stop()
            self._running = False
            print("Script thread stopping")

        
class MainWindow(QMainWindow):
    output_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()
        emitter.message_signal.connect(self.update_output)
        self.key_manager = KeyManager()  # Create only one instance
        self.script_thread = None
        self.key_manager.signals.update_signal.connect(self.update_info)
        print("MainWindow KeyManager instance: ", id(self.key_manager))  # Debugging print statement


    def update_info(self, data):
        if "current_resolution" in data:
            self.resolution_label.setText(f"Current Resolution: {data['current_resolution']}")
        if "play_area_path" in data:
            self.play_area_label.setText(f"Play Area Path: {data['play_area_path']}")
        if "buttons_path" in data:
            self.buttons_path_label.setText(f"Buttons Path: {data['buttons_path']}")
        if "play_area_resolution" in data:
            self.play_area_resolution_label.setText(f"Play Area Resolution: {data['play_area_resolution']}")
        if "match_info" in data:
            self.match_info_label.setText(f"Match Info: {data['match_info']}")


    def initUI(self):
        self.setWindowTitle('Control')
        self.setGeometry(100, 100, 400, 300)

        # Make the window always stay on top
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        # Set window transparency (90% opaque)
        self.setWindowOpacity(0.9)

        # Create a layout
        layout = QVBoxLayout()

          # Create QLabel widgets to display information with default text
        self.resolution_label = QLabel("Current Resolution: No Data Available", self)
        self.play_area_label = QLabel("Play Area Path: No Data Available", self)
        self.buttons_path_label = QLabel("Buttons Path: No Data Available", self)
        self.play_area_resolution_label = QLabel("Play Area Resolution: No Data Available", self)
        self.match_info_label = QLabel("Match Info: No Data Available", self)
        # Button to save settings
        self.save_button = QPushButton('Save Settings', self)
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        # Button to load settings
        self.load_button = QPushButton('Load Settings', self)
        self.load_button.clicked.connect(self.load_settings)
        layout.addWidget(self.load_button)

        # Arrange labels in the layout
        layout.addWidget(self.resolution_label)
        layout.addWidget(self.play_area_label)
        layout.addWidget(self.buttons_path_label)
        layout.addWidget(self.play_area_resolution_label)
        layout.addWidget(self.match_info_label)

        # Arrange other widgets in the layout
        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        # SpinBox for offset value
        self.game_playing_label = QLabel("Game Playing: No", self)
        layout.addWidget(self.game_playing_label)

        # Slider for x_offset value
        self.x_offset_slider = QSlider(Qt.Horizontal, self)
        self.x_offset_slider.setMinimum(0)  # Set minimum value
        self.x_offset_slider.setMaximum(100)  # Set maximum value
        self.x_offset_slider.setValue(30)  # Default value or load from config
        self.x_offset_slider.valueChanged.connect(self.update_x_offset)
        layout.addWidget(QLabel("X Offset Adjustment"))
        layout.addWidget(self.x_offset_slider)

        # Label to display the current x_offset value
        self.x_offset_value_label = QLabel("Current X Offset: 30")
        layout.addWidget(self.x_offset_value_label)


        # QTimer to update game status
        self.game_status_timer = QTimer(self)
        self.game_status_timer.timeout.connect(self.update_game_status)
        self.game_status_timer.start(1000)  # Update every second

        # Start Script button
        self.start_button = QPushButton('Start Script', self)
        self.start_button.clicked.connect(self.start_script)
        layout.addWidget(self.start_button)

        # Stop Script button
        self.stop_button = QPushButton('Stop Script', self)
        self.stop_button.clicked.connect(self.stop_script)
        layout.addWidget(self.stop_button)
        # Define shortcuts
        self.start_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.start_shortcut.activated.connect(self.start_script)

        self.stop_shortcut_b = QShortcut(QKeySequence("Ctrl+B"), self)
        self.stop_shortcut_b.activated.connect(self.stop_script)

        self.stop_shortcut_w = QShortcut(QKeySequence("Ctrl+W"), self)
        self.stop_shortcut_w.activated.connect(self.stop_script)

        # Set the layout on the container widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.output_received.connect(self.update_output)  # Connect signal to slot

    def start_script(self):
        if self.script_thread and self.script_thread.is_alive():
            custom_print("Script thread is already running")
        else:
            self.script_thread = ScriptThread(self.output_received, self.key_manager)
            self.script_thread.start()
            self._running = True
            custom_print("Script thread is starting")

    def stop_script(self):
        if self.script_thread and self.script_thread.is_alive():
            self.script_thread.stop()
            custom_print("Script thread stop requested")
            self.script_thread = None
            self._running = False


    def update_output(self, text):
        cursor = self.output.textCursor()  # Get the QTextCursor from QTextEdit
        cursor.movePosition(QTextCursor.End)  # Move the cursor to the end
        self.output.setTextCursor(cursor)  # Set the text cursor in the QTextEdit
        self.output.insertPlainText(text)  # Insert the text

    def update_game_status(self):
        from customprint import is_game_playing
        self.game_playing_label.setText(f"Game Playing: {'Yes' if is_game_playing else 'No'}")

    def update_x_offset(self, value):
        if self.script_thread and self.script_thread.is_alive():
            self.script_thread.key_manager.update_x_offset(value)
        self.x_offset_value_label.setText(f"Current X-Offset(Width for Green Bar Capture): {value}")
    def save_settings(self):
        current_resolution = self.key_manager.current_resolution  # Assuming this is stored in key_manager
        current_offset = self.x_offset_slider.value()
        saving.save_gui_settings(current_resolution, current_offset)
        custom_print("Settings saved.")

    def load_settings(self):
        resolution, offset = saving.load_gui_settings()
        self.x_offset_slider.setValue(offset)
        # Update any other GUI elements or key_manager attributes with loaded resolution
        self.key_manager.current_resolution = resolution
        self.resolution_label.setText(f"Current Resolution: {resolution}")
        custom_print("Settings loaded.")


app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
sys.exit(app.exec_())

