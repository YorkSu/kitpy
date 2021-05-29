# -*- coding: utf-8 -*-
"""Top-level package for Kitpy."""
from kitpy import config
from kitpy import convert
from kitpy import flags
from kitpy import log
from kitpy import path
from kitpy import singleton
from kitpy import timez

from kitpy.config import ConfigHandler
from kitpy.config import JsonHandler
from kitpy.config import YamlHandler
from kitpy.convert import AdvancedDict
from kitpy.convert import dict2ad
from kitpy.flags import Flags
from kitpy.flags import FLAGS
from kitpy.log import Log
from kitpy.singleton import Singleton
from kitpy.timez import Count

__author__ = 'York Su'
__email__ = 'york_su@qq.com'
__version__ = '0.2.0'

get_logger = log.get_logger
now = timez.now
sleep = timez.sleep
