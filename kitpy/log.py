# -*- coding: utf-8 -*-
import os
import time
import logging
import logging.handlers

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
                 mode='a+',
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


class Log:
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

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)

    @staticmethod
    def get_level(level, default=logging.INFO) -> int:
        if isinstance(level, str):
            return Log.LEVEL.get(level.upper(), default)
        if isinstance(level, int):
            return level
        return default

    @staticmethod
    def clear() -> bool:
        Log.clear_handlers()
        Log.STATUS = Log.NOT_INIT
        return True

    @staticmethod
    def clear_handlers() -> bool:
        logger = logging.getLogger()
        logger.handlers.clear()
        return True

    @staticmethod
    def init(cfg: dict = None, root: str = './') -> bool:
        if Log.STATUS == Log.INITED:
            return True

        cfg = (cfg, {})[cfg is None]
        if not isinstance(cfg, dict):
            return False
        cfg = cfg.get('logging', cfg)

        enable = bool(cfg.get('enable', False))
        if not enable:
            # Log.STATUS = Log.BASE
            # Log.clear_handlers()
            # logging.basicConfig(level=logging.DEBUG)
            # logging.info('using base logger')
            Log.init_default()
            return True

        Log.init_body(cfg, root)
        # console_enable = bool(cfg['console']['enable'])
        # file_enable = bool(cfg['file']['enable'])
        # logger_level = Log.get_level(cfg['level'])
        # fmt = cfg['fmt']
        # datefmt = cfg['datefmt']
        #
        # Log.clear()
        # logger = logging.getLogger()
        # logger.setLevel(logger_level)
        # formatter = logging.Formatter(
        #     fmt=fmt,
        #     datefmt=datefmt,
        # )
        #
        # # console handler
        # if console_enable:
        #     console_level = Log.get_level(cfg['console']['level'])
        #     console = logging.StreamHandler()
        #     console.setLevel(console_level)
        #     console.setFormatter(formatter)
        #     logger.addHandler(console)
        #
        # # file handler
        # if file_enable:
        #     file_level = Log.get_level(cfg['file']['level'])
        #     basename = cfg['file']['basename']
        #     path = cfg['file']['path']
        #     suffix = cfg['file']['suffix']
        #     when = cfg['file']['when']
        #     month = bool(cfg['file']['month'])
        #     error_enable = cfg['file']['error_enable']
        #     error_suffix = cfg['file']['error_suffix']
        #
        #     if not os.path.isabs(path):
        #         path = os.path.join(root, path)
        #     if not os.path.exists(path):
        #         os.mkdir(path)
        #     basename = os.path.join(
        #         path,
        #         basename
        #     )
        #
        #     if error_enable:
        #         rsp_handler = TimedRotatingFileHandler(
        #             basename,
        #             mode='a+',
        #             when=when,
        #             encoding='utf-8',
        #             month_archiving=month,
        #         )
        #         rsp_handler.suffix += suffix
        #         rsp_handler.addFilter(LevelFilter(True))
        #         rsp_handler.setLevel(file_level)
        #         rsp_handler.setFormatter(formatter)
        #         logger.addHandler(rsp_handler)
        #
        #         err_handler = TimedRotatingFileHandler(
        #             basename + error_suffix,
        #             mode='a+',
        #             when=when,
        #             encoding='utf-8',
        #             month_archiving=month,
        #         )
        #         err_handler.suffix += suffix
        #         err_handler.addFilter(LevelFilter(False))
        #         err_handler.setLevel(file_level)
        #         err_handler.setFormatter(formatter)
        #         logger.addHandler(err_handler)
        #     else:
        #         handler = TimedRotatingFileHandler(
        #             basename,
        #             mode='a+',
        #             when=when,
        #             encoding='utf-8',
        #             month_archiving=month,
        #         )
        #         handler.suffix += suffix
        #         handler.setLevel(file_level)
        #         handler.setFormatter(formatter)
        #         logger.addHandler(handler)
        #
        # Log.STATUS = Log.INITED
        return True

    @staticmethod
    def init_default():
        Log.clear_handlers()
        logging.basicConfig(level=logging.DEBUG)
        logging.info('using base logger')
        Log.STATUS = Log.BASE

    @staticmethod
    def init_body(cfg: dict, root: str = './'):
        console_enable = bool(cfg['console']['enable'])
        file_enable = bool(cfg['file']['enable'])
        logger_level = Log.get_level(cfg['level'])
        fmt = cfg['fmt']
        datefmt = cfg['datefmt']

        Log.clear()
        logger = logging.getLogger()
        logger.setLevel(logger_level)
        formatter = logging.Formatter(
            fmt=fmt,
            datefmt=datefmt,
        )

        # console handler
        if console_enable:
            console_level = Log.get_level(cfg['console']['level'])
            console = logging.StreamHandler()
            console.setLevel(console_level)
            console.setFormatter(formatter)
            logger.addHandler(console)

        # file handler
        if file_enable:
            file_level = Log.get_level(cfg['file']['level'])
            basename = cfg['file']['basename']
            path = cfg['file']['path']
            suffix = cfg['file']['suffix']
            when = cfg['file']['when']
            month = bool(cfg['file']['month'])
            error_enable = cfg['file']['error_enable']
            error_suffix = cfg['file']['error_suffix']

            if not os.path.isabs(path):
                path = os.path.join(root, path)
            if not os.path.exists(path):
                os.mkdir(path)
            basename = os.path.join(
                path,
                basename
            )

            if error_enable:
                rsp_handler = TimedRotatingFileHandler(
                    basename,
                    mode='a+',
                    when=when,
                    encoding='utf-8',
                    month_archiving=month,
                )
                rsp_handler.suffix += suffix
                rsp_handler.addFilter(LevelFilter(True))
                rsp_handler.setLevel(file_level)
                rsp_handler.setFormatter(formatter)
                logger.addHandler(rsp_handler)

                err_handler = TimedRotatingFileHandler(
                    basename + error_suffix,
                    mode='a+',
                    when=when,
                    encoding='utf-8',
                    month_archiving=month,
                )
                err_handler.suffix += suffix
                err_handler.addFilter(LevelFilter(False))
                err_handler.setLevel(file_level)
                err_handler.setFormatter(formatter)
                logger.addHandler(err_handler)
            else:
                handler = TimedRotatingFileHandler(
                    basename,
                    mode='a+',
                    when=when,
                    encoding='utf-8',
                    month_archiving=month,
                )
                handler.suffix += suffix
                handler.setLevel(file_level)
                handler.setFormatter(formatter)
                logger.addHandler(handler)

        Log.STATUS = Log.INITED

        ...


get_logger = Log.get_logger
get_level = Log.get_level
clear = Log.clear
clear_handlers = Log.clear_handlers
init = Log.init
