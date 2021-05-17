# -*- coding: utf-8 -*-
"""Top-level package for Kitpy."""
from kitpy import abcs
from kitpy import config
from kitpy import flags
from kitpy import lazy
from kitpy import log
from kitpy import paths
from kitpy import times

from kitpy.abcs import Singleton
from kitpy.config import ConfigHandler
from kitpy.flags import FLAGS
from kitpy.lazy import LazyLoader
from kitpy.log import Log
from kitpy.times import Time
from kitpy.times import Count


__author__ = """York Su"""
__email__ = 'york_su@qq.com'
__version__ = '0.1.3'


INIT_UTILS = False
HERE = paths.fd(__file__)
ROOT = ''
CONFIG_PATH = ''
DATA_PATH = ''

get_logger = Log.get_logger
now = Time.now
sleep = Time.sleep
strftime = Time.strftime
lazy_import = LazyLoader.load


def init(project_path=None,
         config_path='config',
         config_file='config.yml',
         data_path='data') -> bool:
    global INIT_UTILS, ROOT, CONFIG_PATH, DATA_PATH
    if project_path is not None:
        ROOT = paths.abs(project_path)
    elif ROOT == '':
        ROOT = paths.dir(paths.dir(HERE))
    CONFIG_PATH = paths.join(ROOT, config_path)
    DATA_PATH = paths.join(ROOT, data_path)
    FLAGS.ROOT = ROOT
    FLAGS.CONFIG_PATH = CONFIG_PATH
    FLAGS.DATA_PATH = DATA_PATH
    FLAGS.CFG = ConfigHandler.load(config_file, CONFIG_PATH)
    Log.init(cfg=FLAGS.CFG, root=ROOT)
    INIT_UTILS = True
    return True


def is_inited() -> bool:
    return INIT_UTILS


def set_here(here: str=None, from_file=None) -> bool:
    global HERE
    if here is None:
        if from_file is None:
            return False
        here = paths.fd(from_file)
    HERE = here
    return True

def set_root(root: str=None, from_file=None, extra_path=None) -> bool:
    global ROOT
    if root is None:
        if from_file is None:
            return False
        file_path = paths.fd(from_file)
        if extra_path is None:
            extra_path = ''
        root = paths.realpath(paths.join(
            file_path,
            extra_path
        ))
    ROOT = root
    FLAGS.ROOT = ROOT
    return True
