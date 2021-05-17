# -*- coding: utf-8 -*-
import os
import time
import logging
import logging.handlers


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
    INITED = False
    BASE = False

    @staticmethod
    def get_logger(name) -> logging.Logger:
        return logging.getLogger(name)

    @staticmethod
    def get_level(level: str, default=logging.INFO) -> int:
        return Log.LEVEL.get(level.upper(), default)

    @staticmethod
    def clear_handlers() -> bool:
        logger = logging.getLogger()
        logger.handlers.clear()
        return True

    @staticmethod
    def init(cfg: dict = None, root: str = './') -> bool:
        if Log.INITED and not Log.BASE:
            return True

        if cfg is None:
            cfg = {}

        if not isinstance(cfg, dict):
            return False

        cfg = cfg.get('logging', {})

        enable = cfg.get('enable', False)

        if not enable:
            Log.INITED = True
            Log.BASE = True
            Log.clear_handlers()
            logging.basicConfig(level=logging.DEBUG)
            logging.info('using base logger')
            return True

        file_enable = cfg['file']['enable']
        fmt = cfg['fmt']
        datefmt = cfg['datefmt']

        logger_level = Log.get_level(cfg['level']['logger'])
        file_level = Log.get_level(cfg['level']['file'])
        console_level = Log.get_level(cfg['level']['console'])

        Log.clear_handlers()
        Log.BASE = False
        logger = logging.getLogger()
        logger.setLevel(logger_level)
        formatter = logging.Formatter(
            fmt=fmt,
            datefmt=datefmt,
        )

        # console handler
        console = logging.StreamHandler()
        console.setLevel(console_level)
        console.setFormatter(formatter)
        logger.addHandler(console)

        # file handler
        if file_enable:
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

        Log.INITED = True
        return True
