# AsiaNWMusicAutomator

AsiaNWMusicAutomator is a sophisticated screen capture and image recognition tool, optimized for various screen resolutions and equipped with both a graphical user interface and a command-line option.

## Description

This tool is designed for screen capture and image recognition tasks, leveraging an image resizer script to optimize for multiple screen resolutions. Originally tailored for 4k resolution screen grabs, it features a user-friendly GUI as well as command-line functionality to suit diverse user preferences.

## Features

- **Process Name Randomizer**: Each program start features a unique process name.
- **Dynamic Resolution Handling**: Automatically updates the screen resolution on startup and script restart.
- **Custom Resolution Support**: Users can add images for different screen resolutions. Add your resolution to the JSON file and create a folder in the 'images' directory for buttons and play areas.
- **Adjustable Offset**: Includes a slider for fine-tuning the offset parameter.
- **Manual Configuration**: Adjust screen resolutions and add new ones through a JSON file. Complete reference images are required for each resolution.
- **Save & Load Settings**: Using the GUI buttons.

## Supported Resolutions

- 1600x1200
- 1680x1050
- 1856x1392
- 1920x1080 (Tested, works well)
- 1920x1440
- 2048x1536
- 2560x1080
- 2560x1440
- 2560x1600
- 3840x2160 (Tested, works perfectly)

*Feel free to add your own resolution and share your experience. Contributions of reference images can help enhance support for various resolutions.*

## Installation

1. Clone the repository:
git clone https://github.com/NattKh/AsiaNWMusicAutomator.git

2. Navigate to the cloned directory:
3. Install the required packages:

## Usage

- **For GUI**: Run `gui.py`.
- **For Command-Line Interface**: Run `main.py`.

## Building Executable

To compile `gui.py` into an executable using PyInstaller:

1. Install PyInstaller if not already installed:
2. Run PyInstaller:
The executable will be located in the `dist` folder.

## Credits

Based on the foundation laid by [GundirQuid's repository](https://github.com/GundirQuid/newWorldBard).

