import asyncio
import tm1637

CLK = 15
DIO = 14

class Display():
    def __init__(self):
        self._tm = tm1637.TM1637(clk=CLK, dio=DIO)
        self._current: asyncio.Task = None

        self._show_temporary(" Hi ", 1.5)

    def show_ir(self):
        pass

    def show_volume(self, volume):
        pass

    def show_volume_set(self, volume):
        pass

    def _show_temporary(self, text, duration):
        if self._current:
            self._current.cancel()

        self._show(text)
        self._current = asyncio.ensure_future(self._post_blank())

    async def _post_blank(self, duration):
        await asyncio.sleep(duration)
        self._blank()

    def _show(self, text):
        self.tm.show(text)

    def _blank(self):
        self.tm.show('    ')