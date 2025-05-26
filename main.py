from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication
import sys
from navigation import Navigation

def main():
    app = QApplication(sys.argv)
    win = Navigation()
    win.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()