# -*- coding: utf-8 -*-
import importlib
import typing
import logging
from types import ModuleType

from kitpy.abcs import Singleton


class LazyLoader(Singleton):
    MODULES = dict()
    LOG = logging.getLogger(__name__)

    @staticmethod
    def load(name: str) -> typing.Optional['ModuleType']:
        LazyLoader.LOG.debug(f'load {name}')
        if name not in LazyLoader.MODULES:
            with LazyLoader._lock:
                if name not in LazyLoader.MODULES:
                    module: typing.Optional['ModuleType'] = None
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
