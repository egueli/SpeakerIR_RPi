import evdev
from evdev import ecodes, KeyEvent
from commands import *
from typing import Iterator, Optional
import asyncio

class IRCommandSource:
    def __init__(self):
        self._device = evdev.InputDevice('/dev/input/by-path/platform-ir-receiver@18-event')

    async def get_commands(self) -> Iterator[Command]:
        async for event in self._device.async_read_loop():
            yield self._process_event(event)

    def _process_event(self, event) -> Optional[Command]:
        if event.type != ecodes.EV_KEY:
            return None

        if event.value not in [KeyEvent.key_down, KeyEvent.key_hold]:
            return None

        if event.code == ecodes.KEY_VOLUMEUP:
            return VolumeUp()
        elif event.code == ecodes.KEY_VOLUMEDOWN:
            return None # TODO
        elif event.code == ecodes.KEY_MUTE:
            return None # TODO
        elif event.code == ecodes.KEY_TV:
            return None # TODO
        elif event.code == ecodes.KEY_BLUE:
            return None # TODO
            # print("time %15f type %3d code %3d value %d" % (event.timestamp(), event.type, event.code, event.value))

async def test_run():
    ir = IRCommandSource()
    async for command in ir.get_commands():
        print(repr(command))

if __name__ == "__main__":
    asyncio.ensure_future(test_run())
    loop = asyncio.get_event_loop()
    print("now running event loop")
    loop.run_forever()
