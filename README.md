AsiaNWMusicAutomator 
is a sophisticated tool for screen capture and image recognition tasks, optimized for multiple screen resolutions. It features both a user-friendly graphical interface and a command-line option for various user preferences.

Features
Dynamic Resolution Handling: Automatically updates the screen resolution on startup or script restart.
Custom Resolution Support: Users can contribute images for different screen resolutions to improve detection.
Adjustable Offset: An optional slider allows for fine-tuning of the offset parameter.
Manual Configuration: Through a JSON file, users can manually adjust screen resolutions and add new ones.
Installation
Clone the repository:
bash
git clone https://github.com/NattKh/AsiaNWMusicAutomator.git
Navigate to the cloned directory:
bash

cd AsiaNWMusicAutomator
Install the required packages:

pip install -r requirements.txt
Usage
For GUI: Run gui.py.
For Command-Line Interface: Run main.py.
Customization Guide
To customize the tool:

Add new resolutions by creating a folder under the project directory and placing the corresponding sample images.
If the resolution is not automatically detected, adjust it manually in the generated JSON file.
Credits
Based on the foundation laid by GundirQuid's repository.

