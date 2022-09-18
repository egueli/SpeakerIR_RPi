import evdev
from evdev import ecodes, KeyEvent
from commands import *
from typing import Iterator, Optional
import asyncio
import time

class IRCommandSource:
    def __init__(self):
        self._device = evdev.InputDevice('/dev/input/by-path/platform-ir-receiver@4-event')

    async def get_commands(self) -> Iterator[Command]:
        async for event in self._device.async_read_loop():
            yield self._process_event(event)

    def _process_event(self, event) -> Optional[Command]:
        if event.type != ecodes.EV_KEY:
            return None

        is_hold = event.value == KeyEvent.key_hold
        is_down = event.value == KeyEvent.key_down
        
        if not is_hold and not is_down:
            return None

        timestamp = event.timestamp()
        if event.code == ecodes.KEY_VOLUMEUP:
            return VolumeUp(timestamp)
        elif event.code == ecodes.KEY_VOLUMEDOWN:
            return VolumeDown(timestamp)
        elif not is_hold and event.code == ecodes.KEY_MUTE:
            return Mute(timestamp)
        elif not is_hold and event.code == ecodes.KEY_TV:
            return SetInput(timestamp)
        elif not is_hold and event.code == ecodes.KEY_BLUE:
            return ToggleClock(timestamp)

async def test_run():
    ir = IRCommandSource()
    async for command in ir.get_commands():
        if not command: continue
        print(repr(command))

if __name__ == "__main__":
    asyncio.ensure_future(test_run())
    loop = asyncio.get_event_loop()
    print("now running event loop")
    loop.run_forever()
