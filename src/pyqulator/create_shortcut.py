import shutil
from os import makedirs, path
from platform import system


def main():
    if system() == "Linux":
        try:
            destination_dir = path.expanduser("~/.local/share/applications")
            makedirs(destination_dir, exist_ok=True)
            source = path.join(path.dirname(__file__), "Pyqulator.desktop")
            destination = path.expanduser("~/.local/share/applications/Pyqulator.desktop")
            shutil.copy(source, destination)
            print("Shortcut created!")
        except Exception as e:
            print(f"Shortcut was not created: {e}")
