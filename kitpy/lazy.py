# -*- coding: utf-8 -*-
import importlib
import logging
from typing import Optional
from types import ModuleType

from kitpy.abcs import Singleton


class LazyLoader(Singleton):
    MODULES = dict()
    LOG = logging.getLogger(__name__)

    @staticmethod
    def load(name: str) -> Optional['ModuleType']:
        LazyLoader.LOG.debug(f'load {name}')
        if name not in LazyLoader.MODULES:
            with LazyLoader._lock:
                if name not in LazyLoader.MODULES:
                    module: Optional['ModuleType'] = None
                    e = ''
                    try:
                        module = importlib.import_module(name)
                    except ImportError as e:
                        LazyLoader.LOG.error(e)
                    LazyLoader.MODULES[name] = {
                        'module': module,
                        'e': e
                    }
        return LazyLoader.MODULES.get(name)['module']


load = LazyLoader.load
