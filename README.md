Run via gui.py for gui, run via main.py for cmd only. Will include cleaned up requirements.txt once I fully finish the tool. 
You should be able to add your own image for your resolutions for better detecting I just use a image resizer i didn't actaully crop it for all the resolutions. 
Tested on 3840x2160 and 1920 x 1080 mainly, works perfectly for me at 30 offset about whatever is 30 higher than the width. Add optional slider for adjustment. 
Resolution should update itself, when starting or pressing start script. If it doesn't there is a json file that is created you can adjust your resolution there as well as add new supported resolution and create your own folder add your own sample images and so on.

for now here is the list of python module i have. I am not using all of it of course. 
# requirements.txt

altgraph==0.17.4
attrs==23.1.0
auto-py-to-exe==2.42.0
AutoGUIX==0.0.4
Automat==22.10.0
bottle==0.12.25
bottle-websocket==0.2.9
certifi==2023.11.17
cffi==1.16.0
charset-normalizer==3.3.2
click==8.1.7
cmake-converter @ file:///C:/Scripts/python
colorama==0.4.6
constantly==23.10.4
contourpy==1.2.0
cprinter==0.12
customtkinter==5.2.1
cycler==0.12.1
Cython==3.0.6
darkdetect==0.8.0
Deprecated==1.2.14
dill==0.3.7
distlib==0.3.7
docker==7.0.0
Eel==1.0.0a1
flatten-everything==0.41
fonttools==4.46.0
future==0.18.3
gevent==23.9.1
gevent-websocket==0.10.1
greenlet==3.0.2
hyperlink==21.0.0
idna==3.6
Imagegrab==0.0.3
incremental==22.10.0
iniconfig==2.0.0
isort==5.12.0
jmespath==1.0.1
json2==0.8.0
keyboard==0.13.5
keyboard-api==1.0.0
kiwisolver==1.4.5
load==2020.12.3
lxml==4.9.3
Markdown==3.5.1
matplotlib==3.8.2
mccabe==0.7.0
MouseInfo==0.1.3
mss==9.0.1
nodeenv==1.8.0
Nuitka==0.6.16
numpy==1.26.2
opencv-log==1.4.0
opencv-python==4.8.1.78
opencv-python-headless==4.8.1.78
ordered-set==4.1.0
packaging==23.2
pandas==2.1.3
pefile==2023.2.7
pilkit==3.0
Pillow==10.1.0
platformdirs==4.1.0
pluggy==1.3.0
psutil==5.9.6
py2exe2msi==0.0.2
PyAutoGUI==0.9.54
pyclick==0.0.2
pycparser==2.21
pydi==0.3.2
PyDirectInput==1.0.4
pyflakes==3.1.0
PyGetWindow==0.0.9
pyinstaller==6.3.0
pyinstaller-hooks-contrib==2023.10
PyMonCtl==0.7
PyMsgBox==1.0.9
pynput==1.7.6
pyoxidizer==0.24.0
pyparsing==3.1.1
pyperclip==1.8.2
PyQt5==5.15.10
PyQt5-Qt5==5.15.2
PyQt5-sip==12.13.0
pyqt5ac==1.2.1
pyqt5plus==0.1.180513.2115
PyRect==0.2.0
PyScreeze==0.1.30
pytesseract==0.3.10
pytest==7.4.3
python-dateutil==2.8.2
python3-xlib==0.15
python3base92==1.0.3.post1
pytweening==1.0.7
pytz==2023.3.post1
pywin32==306
pywin32-ctypes==0.2.2
PyWinBox==0.6
PyWinCtl==0.3
PyYAML==6.0.1
qtgui==0.0.1
regex==2023.10.3
requests==2.31.0
scipy==1.11.4
screeninfo==0.8.1
setproctitle==1.3.3
setuptools==69.0.2
simplejson==3.19.2
SimplePool==0.1
sip==6.8.1
six==1.16.0
tkinter-tooltip==2.1.0
tomlkit==0.12.3
touchtouch==0.11
twisted-iocpsupport==1.0.4
typing_extensions==4.8.0
tzdata==2023.3
urllib3==2.0.7
wheel==0.42.0
whichcraft==0.6.1
wrapt==1.16.0
xlib==0.21
zope.event==5.0
zope.interface==6.1
zstandard==0.22.0