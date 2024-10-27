from os import geteuid, makedirs, path
from platform import system


def main():
    if system() == "Linux":
        try:
            if geteuid() == 0:
                destination_dir = "/usr/share/applications"
                desktop_content = """[Desktop Entry]
Type=Application
Name=Pyqulator
Comment=A fully functional calculator
Exec=pyqulator
Icon=accessories-calculator
Terminal=false
Categories=Utility;Calculator;
Comment[ru]=Полнофункциональный калькулятор
Comment[uk]=Повнофункціональний калькулятор
"""
            else:
                destination_dir = "~/.local/share/applications"
                desktop_content = """[Desktop Entry]
Type=Application
Name=Pyqulator
Comment=A fully functional calculator
Exec=python3 -c "from pyqulator.main import main; main()"
Icon=accessories-calculator
Terminal=false
Categories=Utility;Calculator;
Comment[ru]=Полнофункциональный калькулятор
Comment[uk]=Повнофункціональний калькулятор
"""
            destination_dir = path.expanduser(destination_dir)
            makedirs(destination_dir, exist_ok=True)
            destination = path.join(destination_dir, "pyqulator.desktop")

            with open(destination, "w") as desktop_file:
                desktop_file.write(desktop_content)

            print("Shortcut created!")
        except Exception as e:
            print(f"Shortcut was not created: {e}")
    else:
        print("This only works on Linux")


if __name__ == "__main__":
    main()
