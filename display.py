import asyncio
from display_hw import *
from elapsed import *

class Display():
    def __init__(self):
        print("display start")
        self._hw = DisplayHardware()
        self._current: asyncio.Task = None
        self._duration = 1.5

    def show_welcome(self):
        # Show "Hi" but with a lowercase I using the left segment
        self._show_temporary([0b00000000, 0b01110110, 0b00010000, 0b00000000])

    def show_ir(self):
        # Show a dot on the rightmost digit
        self._show_temporary([0b00000000, 0b00000000, 0b00000000, 0b10000000])

    def show_volume(self, volume):
        elapsed(lambda: self._show_temporary(self._text("%3d " % volume)))

    def show_volume_set(self, volume):
        segments = self._text("%3d " % volume)
        segments[3] |= 128 # add dot on rightmost digit
        self._show_temporary(segments)

    def show_mute(self, muted):
        if muted:
            self._show_temporary(self._text("nu  "))
        else:
            self._show_temporary(self._text("so  "))

    def show_mute_set(self, muted):
        if muted:
            self._show_temporary(self._text("nute"))
        else:
            self._show_temporary(self._text("soun"))

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

        self._current = asyncio.create_task(self._post_blank(segments, duration))

    async def _post_blank(self, segments, duration):
        self._hw.show_segments(segments)
        await asyncio.sleep(duration)
        self._hw.blank()

if __name__ == "__main__":
    d = Display()
    d.show_volume(85)
