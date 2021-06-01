# -*- coding: utf-8 -*-
from typing import AnyStr

from kitpy.singleton import Singleton
from kitpy import path


class Project(Singleton):
    def __init__(self,
                 root: str,
                 config = 'config',
                 data = 'data'):
        self._root = root
        self._config = config
        self._data = data

    @property
    def root(self) -> str:
        return path.normpath(self._root)

    @property
    def config(self) -> str:
        return path.normpath(path.join(self._root, self._config))

    @property
    def data(self) -> str:
        return path.normpath(path.join(self._root, self._data))

    def workspace(self, name: AnyStr) -> AnyStr:
        """
        Returns relative path that based on work space

        Args:
            name (AnyStr): the relative path

        Returns:
            AnyStr: the final path
        """
        return path.normpath(path.join(self._root, name))

    def set_root(self, root: str) -> None:
        self._root = root

    def set_root_file(self, _file: str, extra='') -> None:
        self._root = path.join(path.fd(_file), extra)

    def set_config(self, config: str) -> None:
        self._config = config

    def set_data(self, data: str) -> None:
        self._data = data


PROJECT = Project('./')
ROOT = PROJECT.root
CONFIG = PROJECT.config
DATA = PROJECT.data

set_root = PROJECT.set_root
set_root_file = PROJECT.set_root_file
set_config = PROJECT.set_config
set_data = PROJECT.data
workspace = PROJECT.workspace
