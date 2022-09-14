from time import localtime
from display import *

class Clock():
    def __init__(self, display):
        self._display: Display = display
        self._on = False

    def start(self):
        asyncio.create_task(self._time_loop())

    def toggle(self):
        self._on = not self._on
        self._update_time()

    async def _time_loop(self):
        while True:
            self._update_time()
            await asyncio.sleep(1)

    def _update_time(self):
        self._display.set_time(localtime() if self._on else None)

