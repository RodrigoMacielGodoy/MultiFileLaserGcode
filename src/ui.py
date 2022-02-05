from PyQt5.QtWidgets import QMainWindow
from main_window_layout import Ui_MainWindow as WindowLayout

class UI(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = WindowLayout()
        self.setupUI()

    def setupUI(self) -> None:
        self.ui.setupUi(self)
        self.ui.listWidget.setAcceptDrops(True)
        self.ui.listWidget.dragEnterEvent = self.list_event_enter
        self.ui.listWidget.dropEvent = self.list_event_drop

    def list_event_enter(self, event) -> bool:
        print("Here")
        if event.mimeData().hasUrls():
            print("Acepted")
            event.accept()
        else:
            event.ignore()

    def list_event_drop(self, event):
        print("Yay")
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f)
