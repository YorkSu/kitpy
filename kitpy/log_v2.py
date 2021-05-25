# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os
import time

from kitpy.abcs import Singleton


DEFAULT_CFG = {
    'enable': True,
    'level': 'info',
    'fmt': '%(asctime)s.%(msecs)03d [%(levelname)s] >%(name)s: %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
    'file': {
        'enable': True,
        'level': 'info',
        'basename': 'logging',
        'path': 'logs',
        'suffix': '.log',
        'when': 'D',
        'month': True,
        'error_enable': True,
        'error_suffix': '.error',
    },
    'console': {
        'enable': 'true',
        'level': 'info',
    },
}


class FileConfig(object): 
    def __init__(self) -> None:
        self.enable: bool = None
        self.level: str = None
        self.basename: str = None
        self.path: str = None
        self.suffix: str = None
        self.when: str = None
        self.month: bool = None
        self.error_enable: bool = None
        self.error_suffix: str = None


class ConsoleConfig(object):
    def __init__(self) -> None:
        self.enable: bool = None
        self.level: str = None


class LogConfig(object):
    def __init__(self, cfg: dict):
        if not isinstance(cfg, dict):
            cfg = dict()
        self._cfg = cfg

        self.enable: bool = bool(cfg.get('enable'))
        self.level: str = cfg.get('level')
        self.fmt: str = cfg.get('fmt')
        self.datefmt: str = cfg.get('datefmt')

        file = cfg.get('file', {})
        self.file: FileConfig = FileConfig()
        self.file.enable = bool(file.get('enable'))
        self.file.level = file.get('level')
        self.file.basename = file.get('basename')
        self.file.path = file.get('path')
        self.file.suffix = file.get('suffix')
        self.file.when = file.get('when')
        self.file.month = bool(file.get('month'))
        self.file.error_enable = bool(file.get('error_enable'))
        self.file.error_suffix = file.get('error_suffix')
    
        console = cfg.get('console', {})
        self.console: ConsoleConfig = ConsoleConfig
        self.console.enable = bool(console.get('enable'))
        self.console.level = console.get('level')


class TimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """
    Handler for logging to a file, rotating the log file at certain timed
    intervals.

    If backupCount is > 0, when rollover is done, no more than backupCount
    files are kept - the oldest ones are deleted.

    Based on Timed Rotating FileHandler modifications, month-based
    archiving has been added
    """

    def __init__(self,
                 filename,
                 when='h',
                 interval=1,
                 backupCount=0,
                 encoding=None,
                 delay=False,
                 utc=False,
                 atTime=None,
                 month_archiving=False):
        self.month_archiving = month_archiving
        if self.month_archiving:
            dir_name, base_name = os.path.split(filename)
            mon_name = os.path.join(
                dir_name,
                time.strftime('%Y-%m', time.localtime(time.time()))
            )
            if not os.path.exists(mon_name):
                os.mkdir(mon_name)
            filename = os.path.join(
                mon_name,
                base_name
            )

        super().__init__(
            filename,
            when=when,
            interval=interval,
            backupCount=backupCount,
            encoding=encoding,
            delay=delay,
            utc=utc,
            atTime=atTime
        )

    def update_month_archiving(self):
        if self.month_archiving:
            now_month = time.strftime('%Y-%m', time.localtime(time.time()))
            dir_name, base_name = os.path.split(self.baseFilename)
            dir_name, month = os.path.split(dir_name)

            if month == now_month:
                return

            mon_name = os.path.join(
                dir_name,
                now_month
            )
            if not os.path.exists(mon_name):
                os.mkdir(mon_name)
            self.baseFilename = os.path.join(
                mon_name,
                base_name
            )

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        self.update_month_archiving()

        super().doRollover()


class LevelFilter(logging.Filter):
    def __init__(self, less=False, level=logging.WARNING, name=''):
        super().__init__(name)
        self.less = less
        self.level = level

    def filter(self, record: logging.LogRecord) -> bool:
        return self.less == (record.levelno < self.level)


class Log(Singleton):
    LEVEL = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'FATAL': logging.FATAL,
    }
    NOT_INIT = 0
    INITED = 1
    BASE = 2
    STATUS = NOT_INIT

    def __init__(self, cfg: dict, root='./'):
        self._cfg = dict()
        self._root = root

        self.cfg: LogConfig = None
        self.root_logger: logging.Logger = None
        self.formatter: logging.Formatter = None

        self.set_cfg(cfg)

    @classmethod
    def status(cls) -> int:
        return cls.STATUS

    @classmethod
    def is_status(cls, status: int) -> bool:
        return cls.STATUS == status

    @classmethod
    def set_status(cls, status: int) -> None:
        cls.STATUS = status

    @classmethod
    def clear(cls) -> None:
        cls.clear_handlers()
        cls.STATUS = cls.NOT_INIT

    @staticmethod
    def clear_handlers() -> None:
        logging.getLogger().handlers.clear()

    @classmethod
    def get_level(cls, level, default=logging.INFO) -> int:
        if isinstance(level, str):
            return cls.LEVEL.get(level.upper(), default)
        if isinstance(level, int):
            return level
        return default

    @staticmethod
    def get_logger(name: str = None) -> logging.Logger:
        return logging.getLogger(name)

    getLogger = get_logger

    def set_cfg(self, cfg: dict) -> None:
        if not isinstance(cfg, dict):
            cfg = {}
        self._cfg = cfg.get('logging', cfg)
        self.cfg = LogConfig(self._cfg)

    def init(self) -> bool:
        if self.is_status(self.INITED):
            return False

        if self.cfg.enable:
            self._init_logger()
        elif not self.is_status(self.BASE):
            self._init_base_logger()
        else:
            return False

        return True

    @property
    def inited(self) -> bool:
        return self.STATUS != self.NOT_INIT

    def _init_base_logger(self) -> None:
        self.clear_handlers()
        logging.basicConfig(level=logging.DEBUG)
        logging.info('using base logger')
        self.set_status(self.BASE)

    def _init_logger(self) -> None:
        self.clear()

        self.root_logger = self.get_logger()
        self.root_logger.setLevel(self.get_level(self.cfg.level))
        self.formatter = logging.Formatter(
            fmt=self.cfg.fmt,
            datefmt=self.cfg.datefmt,
        )

        self._set_console_handler()
        self._set_file_handler()

        self.set_status(self.INITED)

    def _set_console_handler(self) -> None:
        if not self.cfg.console.enable:
            return
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.get_level(self.cfg.console.level))
        console_handler.setFormatter(self.formatter)
        self.root_logger.addHandler(console_handler)

    def _set_file_handler(self) -> None:
        if not self.cfg.file.enable:
            return

        basename = self._get_basename()

        if self.cfg.file.error_enable:
            rsp_handler = self._get_timed_handler(basename)
            rsp_handler.addFilter(LevelFilter(True))
            self.root_logger.addHandler(rsp_handler)
            err_handler = self._get_timed_handler(basename + self.cfg.file.error_suffix)
            err_handler.addFilter(LevelFilter(False))
            self.root_logger.addHandler(err_handler)
        else:
            handler = self._get_timed_handler(basename)
            self.root_logger.addHandler(handler)

    def _get_timed_handler(self, basename: str) -> TimedRotatingFileHandler:
        handler = TimedRotatingFileHandler(
            basename,
            when=self.cfg.file.when,
            encoding='utf-8',
            month_archiving=self.cfg.file.month
        )
        handler.suffix += self.cfg.file.suffix
        handler.setLevel(self.get_level(self.cfg.file.level))
        handler.setFormatter(self.formatter)
        return handler

    def _get_basename(self) -> str:
        if not os.path.isabs(self.cfg.file.path):
            path = os.path.join(self._root, self.cfg.file.path)
        self._check_path(path)
        return os.path.normpath(os.path.join(path, self.cfg.file.basename))

    def _check_path(self, path) -> None:
        if not os.path.exists(path):
            os.mkdir(path)
