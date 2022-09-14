import asyncio
from display_hw import *
from elapsed import *
import hashlib

class Display():
    def __init__(self):
        self._hw = DisplayHardware()
        self._current: asyncio.Task = None
        self._duration = 1.5
        self._blank_segments = [0, 0, 0, 0]

    def show_welcome(self):
        # Show "Hi" but with a lowercase I using the left segment
        self._show_temporary([0b00000000, 0b01110110, 0b00010000, 0b00000000])

    def show_ir(self):
        self._show_temporary(add_ok([0, 0, 0, 0]))

    def show_volume(self, volume):
        elapsed(lambda: self._show_temporary(self._text("%3d " % volume)))

    def show_volume_set(self, volume):
        segments = add_ok(self._text("%3d " % volume))
        self._show_temporary(segments)

    def show_mute(self, muted):
        if muted:
            self._show_temporary(self._text("nu  "))
        else:
            self._show_temporary(self._text("so  "))

    def show_mute_set(self, muted):
        if muted:
            self._show_temporary(add_ok(self._text("nute")))
        else:
            self._show_temporary(add_ok(self._text("soun")))

    def show_tv_input_set(self):
        self._show_temporary(add_ok(self._text(" tv ")))

    def show_error_invalid_state(self):
        self._show_temporary([0b0111111, 0b01110001, 0b01110001, 0b0000000]) # "Off "

    def show_error_numeric(self, code):
        self._show_temporary(self._text(f"E{code}"))

    def show_error_other(self, exception: Exception):
        message = f"{exception.__class__}:{exception}".encode("utf-8")
        code = int(hashlib.md5(message).hexdigest()[:8], 16) % 1000
        print(f'Hashing "{message}" to fault code {code}')
        segments = self._text(f"F{code:03}")
        self._show_temporary(segments)

    def set_time(self, time):
        if not time:
            self._blank_segments = [0, 0, 0, 0]
        else:            
            h = time.tm_hour
            m = time.tm_min
            self._blank_segments = add_dot(self._text(f"{h:2}{m:02}"), 1)
        
        if self._current is None:
            self._blank()

    def _text(self, text):
        text = f"{text:>4}" # align right by adding padding spaces
        return self._hw.encode_string(text)

    def _show_temporary(self, segments, duration = None):
        if not duration:
            duration = self._duration
            
        if self._current:
            self._current.cancel()
            self._current = None

        self._hw.show_segments(segments)
        self._current = asyncio.create_task(self._post_blank(duration))

    async def _post_blank(self, duration):
        await asyncio.sleep(duration)
        self._blank()
        self._current = None

    def _blank(self):
        self._hw.show_segments(self._blank_segments)

def add_ok(segments):
    return add_dot(segments, 3)

def add_dot(segments, position):
    segments[position] |= 128
    return segments

if __name__ == "__main__":
    d = Display()
    d.show_volume(85)
