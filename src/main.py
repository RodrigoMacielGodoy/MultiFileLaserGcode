from re import U
import sys
from PyQt5.QtWidgets import QApplication

from window_manager import WindowManager

def main():
    app = QApplication(sys.argv)
    window_manager = WindowManager()
    app.exec()

if __name__ == "__main__":
    main()