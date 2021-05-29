# -*- coding: utf-8 -*-
"""Top-level package for Kitpy."""
from kitpy import config
from kitpy import convert
from kitpy import flags
from kitpy import log
from kitpy import path
from kitpy import project
from kitpy import singleton
from kitpy import timez

from kitpy import dev

__author__ = 'York Su'
__email__ = 'york_su@qq.com'
__version__ = '0.2.3'

ConfigHandler = config.ConfigHandler
JsonHandler = config.JsonHandler
YamlHandler = config.YamlHandler

AdvancedDict = convert.AdvancedDict
dict2ad = convert.dict2ad

Flags = flags.Flags
FLAGS = flags.FLAGS

DEFAULT_CFG = log.DEFAULT_CFG
Log = log.Log
getLogger = log.getLogger
get_logger = log.get_logger

PROJECT = project.PROJECT
ROOT = project.ROOT
CONFIG = project.CONFIG
DATA = project.DATA
set_root = project.set_root
set_root_file = project.set_root_file
workspace = project.workspace

AbstractSingleton = singleton.AbstractSingleton
Singleton = singleton.Singleton

Count = timez.Count
TimeFormat = timez.TimeFormat
localtime = timez.localtime
now = timez.now
sleep = timez.sleep
strftime = timez.strftime
unix = timez.unix
