import shutil
from os import makedirs, path
from platform import system

from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        super().run()
        if system() == "Linux":
            try:
                destination_dir = path.expanduser("~/.local/share/applications")
                makedirs(destination_dir, exist_ok=True)
                source = path.join(path.dirname(__file__), "src/pyqulator/Pyqulator.desktop")
                destination = path.expanduser("~/.local/share/applications/Pyqulator.desktop")
                shutil.copy(source, destination)
            except:  # noqa
                pass


setup(
    cmdclass={
        "install": PostInstallCommand,
    },
)
