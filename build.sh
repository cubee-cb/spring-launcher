#!/bin/bash

#pyinstaller --windowed --icon ./res/icon.png --name "Spring" -F spring.py
pyinstaller --onefile --add-data "res/*:res/" --name "spring" spring.py
