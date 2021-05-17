# -*- coding: utf-8 -*-
import typing

from kitpy.abcs import Singleton


class Flags(Singleton):
    """Global Parameters Manager

    This is a Singleton Class"""
    def __init__(self):
        self.ROOT = ''
        self.CONFIG_PATH = ''
        self.CFG = dict()

    def __getattribute__(self, key, default=None) -> typing.Any:
        try:
            return super().__getattribute__(key)
        except AttributeError:
            return default

    def get(self, key, default=None) -> typing.Any:
        """Get the value of an argument

          If not found, return default
        """
        return self.__getattribute__(key, default)

    def set(self, key, value):
        """Set the value of an argument"""
        self.__setattr__(key, value)


FLAGS = Flags()
