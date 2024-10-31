# Pyqulator

![Static Badge](https://img.shields.io/badge/License-GNU_GPL_v3-blue)
![Static Badge](https://img.shields.io/badge/PyQt-6-green)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A fully functional calculator written in PyQt 6 and using SymPy for calculations. Qt Designer and Qt Linguist were used to create the interface.

## Features
+ Simple and lightweight
+ Standard, engineer and paper modes
+ Unit converter
+ Save journal as .txt
+ Move line up/down in paper mode
+ Available in 3 languages
+ Remember mode, window size and user settings for next launch

## Usage
```bash
pyqulator
```
### Add a shortcut in Linux
Download the `pyqulator.desktop` file and make it executable:
```bash
wget https://raw.githubusercontent.com/limafresh/pyqulator/main/pyqulator.desktop
chmod +x pyqulator.desktop
```
Just move it to `~/.local/share/` (for one user) or `/usr/share/applications` (for all users).

## Screenshots
*Standard mode*

![Screenshot](https://raw.githubusercontent.com/limafresh/pyqulator/main/screenshots/screenshot1.png)

*Engineer mode*

![Screenshot](https://raw.githubusercontent.com/limafresh/pyqulator/main/screenshots/screenshot2.png)

*Paper mode*

![Screenshot](https://raw.githubusercontent.com/limafresh/pyqulator/main/screenshots/screenshot3.png)

*Unit converter*

![Screenshot](https://raw.githubusercontent.com/limafresh/pyqulator/main/screenshots/screenshot4.png)
