# -*- coding: utf-8 -*-
import time
import logging


class Count:
    def __init__(self,
                 message='Codes Cost Seconds: ${cost}',
                 prec=6,
                 log=True,
                 show=True,
                 name: str = __name__):
        self.message = message
        self._prec = prec
        self._log = log
        self._show = show
        self._name = name

        self.start = 0.
        self.stop = 0.
        self.cost = 0.

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, type, value, traceback):
        self.stop = time.perf_counter()
        self.cost = round(self.stop - self.start, self._prec)

        if not self._show:
            return

        self.message = self.message.replace('${cost}', str(self.cost))
        if self._log:
            logging.getLogger(self._name).info(self.message)
        else:
            print(self.message)


class Format:
    SHORT = '%Y-%m-%d'
    LONG = '%Y-%m-%d %H-%M-%S'
    GENERAL_LONG = '%Y-%m-%d %H:%M:%S'
    NUMONLY_SHORT = '%Y%m%d'
    NUMONLY_LONG = '%Y%m%d%H%M%S'


def now(fmt: str = Format.LONG) -> str:
    return strftime(fmt)


def strftime(fmt: str = Format.LONG, struct_time=None, timestamp=None) -> str:
    if struct_time is None:
        if timestamp is None:
            timestamp = time.time()
        struct_time = time.localtime(timestamp)
    return time.strftime(fmt, struct_time)


def unix() -> int:
    """
    Return the current time in seconds since the Epoch.
    Fractions of a second may be present if the system clock provides them.

    Returns:
        int
    """
    return int(time.time())


# Alias
localtime = time.localtime
sleep = time.sleep
