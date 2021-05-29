# -*- coding: utf-8 -*-
from typing import Any

from kitpy.singleton import Singleton


class Flags(Singleton):
    """Global Parameters Manager

    This is a Singleton Class
    """
    def __getattribute__(self, key: str, default: Any = None) -> Any:
        try:
            return super().__getattribute__(key)
        except AttributeError:
            return default

    def get(self, key: str, default: Any = None) -> Any:
        """Get the value of an argument

        If not found, return default
        """
        return self.__getattribute__(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set the value of an argument"""
        self.__setattr__(key, value)


FLAGS = Flags()
