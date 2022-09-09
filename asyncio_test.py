
import asyncio


class Display:
    def __init__(self):
        self._current: asyncio.Task = None

    def _show(self, text):
        print(f"display: {text}")
    
    def _blank(self):
        print("display is now blank")

    async def _post_blank(self):
        await asyncio.sleep(2)
        self._blank()

    async def display_message(self, text):
        if self._current:
            self._current.cancel()

        self._show(text)
        self._current = asyncio.ensure_future(self._post_blank())


async def main():
    d = Display()
    await d.display_message("hello")
    await asyncio.sleep(1)
    await d.display_message("world")
    
    await asyncio.sleep(10)


asyncio.run(main())