# -*- coding: utf-8 -*-
"""Cache Interface

"""
import abc
from typing import Any


class Cache(abc.ABC):
    """Abstract Cache Class

    Extends this class to create a ``Cache`` class.

    MUST overridden methods: clear, update, value

    """
    def __init__(self):
        ...

    @abc.abstractmethod
    def clear(self) -> None: ...

    @abc.abstractmethod
    def update(self, value: Any) -> None: ...

    @property
    @abc.abstractmethod
    def value(self) -> Any: ...
