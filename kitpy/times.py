# -*- coding: utf-8 -*-
import time
import logging


class Time:
    DATE = "%Y-%m-%d"
    TIME = "%Y-%m-%d %H-%M-%S"
    DEFAULT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def now(fmt=DEFAULT, file=False) -> str:
        if file:
            fmt = Time.TIME
        return time.strftime(fmt, time.localtime(time.time()))

    @staticmethod
    def unix() -> int:
        return int(time.time())

    @staticmethod
    def strftime(fmt=DEFAULT, timestamp=None, file=False) -> str:
        if timestamp is None:
            timestamp = time.time()
        if file:
            fmt = Time.TIME
        return time.strftime(fmt, time.localtime(timestamp))

    @staticmethod
    def localtime(secs):
        return time.localtime(secs)

    @staticmethod
    def sleep(second: float):
        time.sleep(second)


class Count:
    def __init__(self,
                 message='Codes Cost Seconds: {cost}',
                 prec=6,
                 logger=True,
                 show=True):
        self.message = message
        self.prec = prec
        self.logger = logger
        self.show = show
        self.start = 0.
        self.stop = 0.
        self.cost = 0.

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, type, value, traceback):
        self.stop = time.perf_counter()
        self.cost = round(self.stop - self.start, self.prec)
        if self.show:
            if self.logger:
                log = logging.getLogger(__name__)
                log.info(self.message.replace('{cost}', str(self.cost)))
            else:
                print(self.message.replace('{cost}', str(self.cost)))
