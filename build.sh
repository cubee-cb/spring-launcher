#!/bin/bash

#pyinstaller --windowed --icon ./res/icon.png --name "Spring" -F spring.py
pyinstaller --onefile --add-data "res/*:res/" --icon "./res/icon.png" --name "spring" spring.py
