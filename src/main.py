from re import U
import sys
from PyQt5.QtWidgets import QApplication

from ui import UI

def main():
    app = QApplication(sys.argv)
    window = UI()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()