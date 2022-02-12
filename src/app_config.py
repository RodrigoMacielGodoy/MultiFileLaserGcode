from email.policy import default
from json import load
import os
from typing import Any
from settings import Settings, ConfigObj

class MetaAppConfig(type):
    def __getattr__(self, __name: str) -> Any:
        return getattr(AppConfig.settings, __name, None)

class AppConfig(metaclass=MetaAppConfig):
    local_path = os.path.join(os.path.expanduser("~"), ".multiGcodes")
    settings = None

    @staticmethod
    def init() -> None:
        AppConfig.settings = Settings(os.path.join(AppConfig.local_path, "appConfig.json"))

        ret = AppConfig.settings.load()
        default_settings = {
            "ui":{
                "a": True
            }
        }
        if not ret:
            AppConfig.settings.from_dict(default_settings)
            AppConfig.settings.save()
    
    @staticmethod
    def save() -> None:
        AppConfig.settings.save()
    
    @staticmethod
    def reload() -> None:
        AppConfig.settings.load()

    @staticmethod
    def setConfig(name: str, value: Any) -> None:
        tree = name.split(".")
        __name = tree.pop(-1)
        if len(tree) == 0:
            AppConfig.settings.setField(name, value)
            return True

        attr = getattr(AppConfig.settings, tree.pop(0))
        if attr is None:
            return False

        while len(tree) > 1:
            attr = getattr(attr, tree.pop(0))
            if attr is not ConfigObj:
                return False
        
        attr.setField(__name, value)
        return True
