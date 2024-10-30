#!/usr/bin/env bash

LIB_DIR=$(python3 -c "from sysconfig import get_paths; print(get_paths()['purelib'])")
BIN_DIR=/usr/local/bin

echo "Copying files to Python directory..."
mkdir -p $LIB_DIR/pyqulator
cp src/pyqulator/*.py $LIB_DIR/pyqulator/
mkdir -p $LIB_DIR/pyqulator/locales
cp src/pyqulator/locales/*.qm $LIB_DIR/pyqulator/locales/

echo "Creating link..."
cat <<EOF > $BIN_DIR/pyqulator
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import sys
from pyqulator.main import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
EOF
chmod +x $BIN_DIR/pyqulator

echo "Creating shortcut..."
cat <<EOF > /usr/share/applications/pyqulator.desktop
[Desktop Entry]
Type=Application
Name=Pyqulator
Comment=A fully functional calculator
Exec=pyqulator
Icon=accessories-calculator
Terminal=false
Categories=Utility;Calculator;
Comment[ru]=Полнофункциональный калькулятор
Comment[uk]=Повнофункціональний калькулятор
EOF
chmod +x /usr/share/applications/pyqulator.desktop

echo "Installation complete"
