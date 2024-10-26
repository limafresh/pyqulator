import shutil
from os import path
from platform import system

from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        super().run()
        if system() == "Linux":
            try:
                source = path.join(path.dirname(__file__), "Pyqulator.desktop")
                destination = path.expanduser("~/.local/share/applications/Pyqulator.desktop")
                shutil.copy(source, destination)
            except:  # noqa
                pass


setup(
    cmdclass={
        "install": PostInstallCommand,
    },
)
