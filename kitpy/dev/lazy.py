# -*- coding: utf-8 -*-
import importlib
import logging
from typing import Optional
from types import ModuleType

from kitpy.singleton import Singleton


class LazyLoader(Singleton):
    MODULES = dict()

    @classmethod
    def load(cls, name: str) -> Optional['ModuleType']:
        logger.debug(f"lazy import {name}")
        if name not in cls.MODULES:
            with cls._lock:
                if name not in cls.MODULES:
                    module: Optional['ModuleType'] = None
                    e = ''
                    try:
                        module = importlib.import_module(name)
                    except ImportError as e:
                        logger.error(e)
                    cls.MODULES[name] = {
                        'module': module,
                        'e': e
                    }
        return cls.MODULES[name]['module']


logger = logging.getLogger(__name__)
load = LazyLoader.load
