# -*- coding: utf-8 -*-
import threading


class AdvancedThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._running = threading.Event()
        self.setDaemon(True)

    def run(self) -> None:
        self._running.set()
        self.created()
        self.mounted()
        self.unmounted()

    def stop(self) -> None:
        self._running.clear()
        self.stopped()

    def created(self) -> None: ...

    def mounted(self) -> None: ...

    def unmounted(self) -> None: ...

    def stopped(self) -> None: ...
