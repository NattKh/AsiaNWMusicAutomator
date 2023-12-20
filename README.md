Run via gui.py for gui, run via main.py for cmd only. Will include cleaned up requirements.txt once I fully finish the tool. 
You should be able to add your own image for your resolutions for better detecting I just use a image resizer i didn't actaully crop it for all the resolutions. 
Tested on 3840x2160 and 1920 x 1080 mainly, works perfectly for me at 30 offset about whatever is 30 higher than the width. Add optional slider for adjustment. 
Resolution should update itself, when starting or pressing start script. If it doesn't there is a json file that is created you can adjust your resolution there as well as add new supported resolution and create your own folder add your own sample images and so on.
for now here is the list of python module i have. I am not using all of it of course. 
Used this repo as a base for this project.
Credit to him
https://github.com/GundirQuid/newWorldBard
# requirements.txt

mss==9.0.1
numpy==1.26.2
opencv-python==4.8.1.78
PyDirectInput==1.0.4
PyGetWindow==0.0.9
PyQt5==5.15.10
PyQt5-Qt5==5.15.2
PyQt5-sip==12.13.0
PyRect==0.2.0

