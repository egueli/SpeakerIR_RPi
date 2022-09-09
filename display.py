import asyncio
import tm1637

CLK = 15
DIO = 14

class Display():
    def __init__(self):
        self._tm = tm1637.TM1637(clk=CLK, dio=DIO)
        self._current: asyncio.Task = None

        self._show_segments_temporary([0b00000000, 0b01110110, 0b00010000, 0b00000000], 1.5)

    def show_ir(self):
        pass

    def show_volume(self, volume):
        pass

    def show_volume_set(self, volume):
        pass

    def _show_segments_temporary(self, text, duration):
        if self._current:
            self._current.cancel()

        self._show_segments(text)
        self._current = asyncio.ensure_future(self._post_blank(duration))

    async def _post_blank(self, duration):
        await asyncio.sleep(duration)
        self._blank()

    def _show_segments(self, text):
        self._tm.write(text)

    def _blank(self):
        self._tm.show('    ')