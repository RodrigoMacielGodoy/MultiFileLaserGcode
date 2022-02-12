from window import MainWindow

class WindowManager(object):
    def __init__(self) -> None:
        self.main_window = MainWindow()
        self.main_window.show()

