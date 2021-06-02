# -*- coding: utf-8 -*-
import threading
import time


class AdvancedThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._running = threading.Event()
        self.setDaemon(True)
        self.created()

    def run(self) -> None:
        self._running.set()
        self.mounted()
        self.mounting()
        self.unmounted()

    def stop(self) -> None:
        self._running.clear()
        self.stopped()

    def mounting(self) -> None:
        while self._running.isSet():
            self.call()

    def created(self) -> None: ...

    def mounted(self) -> None: ...

    def unmounted(self) -> None: ...

    def stopped(self) -> None: ...

    def call(self) -> None:
        time.sleep(1)
