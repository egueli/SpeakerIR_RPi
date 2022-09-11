import asyncio
from display_hw import *

class Display():
    def __init__(self):
        print("display start")
        self._hw = DisplayHardware()
        self._current: asyncio.Task = None
        self._duration = 1.5

    def show_welcome(self):
        self._show_temporary([0b00000000, 0b01110110, 0b00010000, 0b00000000])

    def show_ir(self):
        self._show_temporary([0b00000000, 0b10000000, 0b00000000, 0b00000000])
        pass

    def show_volume(self, volume):
        self._show_temporary(self._text("%3d " % volume))

    def show_volume_set(self, volume):
        pass

    def show_error(self, error):
        self._hw.blank()
        self._show_temporary(self._text(f"E{error}"))

    def _text(self, text):
        text = f"{text:>4}" # align right by adding padding spaces
        return self._hw.encode_string(text)

    def _show_temporary(self, segments, duration = None):
        if not duration:
            duration = self._duration
            
        if self._current:
            self._current.cancel()

        self._hw.show_segments(segments)
        self._current = asyncio.create_task(self._post_blank(duration))

    async def _post_blank(self, duration):
        await asyncio.sleep(duration)
        self._hw.blank()

if __name__ == "__main__":
    d = Display()
    d.show_volume(85)
