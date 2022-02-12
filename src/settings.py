import json
import os
from json import JSONDecodeError
from os.path import exists
from typing import Any

class ConfigObj(object):
    def __init__(self, parent, **kwargs) -> None:
        self.__parent = parent
        self.__atributes = {}
        for k, v in kwargs.items():
            if type(v) is dict:
                v = ConfigObj(self.__parent, **v)          
            self.__atributes[k] = v

    def __getattr__(self, __name: str) -> Any:
        if __name in self.__atributes:
            return self.__atributes[__name]
        return None

    def setField(self, name: str, value: Any) -> None:
        self.__atributes[name] = value

    def to_dict(self) -> dict:
        new_data = {}
        for k, v in self.__atributes.items():
            if type(v) is ConfigObj:
                v = v.to_dict()
            new_data[k] = v
        return new_data

    def has(self, field_name: str) -> bool:
        return field_name in self.__atributes

class Settings(object):
    """docstring for Settings"""
    def __init__(self, path: str=""):
        super(Settings, self).__init__()
        self.__path = path
        self.__atributes = {}

    def setField(self, name: str, value: Any) -> None:
        if type(value) is dict:
            value = ConfigObj(self, **value)
        self.__atributes[name] = value

    def from_dict(self, sett: dict) -> None:
        for k,v in sett.items():
            self.setField(k,v)

    def load(self, path:str="") -> bool:
        if path == "":
            path = self.__path
        try:
            with open(path, "r") as f:
                settings = json.load(f)

            for key, value in settings.items():
                self.setField(key, value)
            return True
        except (OSError, JSONDecodeError) as ex:
            return False

    def save(self, path:str="", create=True) -> None:
        if path == "":
            path = self.__path

        if not exists(os.path.dirname(path)):
            if create:
                os.mkdir(os.path.dirname(path))
            else:
                raise FileNotFoundError

        with open(path, "w") as f:
            json.dump(self.toDict(), f, indent=4, sort_keys=True)

    def has(self, field_name: str) -> bool:
        return hasattr(self, field_name)

    def toDict(self) -> dict:
        new_data = {}
        for k,v in self.__atributes.items():
            if "_Settings" in k:
                continue
            if type(v) is ConfigObj:
                v = v.to_dict()
            new_data[k] = v
        return new_data

    def __getattr__(self, __name: str) -> Any:
        if __name in self.__atributes:
            return self.__atributes[__name]
        return None