import os
from window import Window
from file_config_widget import FileConfigWidget

class WindowManager(object):
    def __init__(self) -> None:
        self.window = Window()
        self.window.show()

