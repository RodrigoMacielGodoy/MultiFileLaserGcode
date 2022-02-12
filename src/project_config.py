from PyQt5.QtWidgets import QFileDialog

from typing import Any
from settings import Settings

class ProjectConfig(Settings):
    _instance = None

    def __new__(cls, path: str="") -> Any:
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
            cls._instance.init(path)
        return cls._instance

    def __init__(self, path: str = ""):
        pass

    def _init_(self, path: str = ""):
        super().__init__(path)

