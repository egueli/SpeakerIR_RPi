#!/usr/bin/python3

# Run setup_ir.sh with root priviledges before running this.

import traceback
import asyncio
from display import Display
from elapsed import *
from commands import *
from ir import *
from musiccast import *

class Application:
	def __init__(self):
		self._display = Display()
		self._ir = IRCommandSource()
		self._musiccast = MusicCast()

	async def run(self):
		self._display.show_welcome()
		async for command in self._ir.get_commands():
			if not command: continue

			try:
				self._display.show_ir()
				print(repr(command))
				if isinstance(command, VolumeUp):
					elapsed(lambda: self._change_volume(2))
				if isinstance(command, VolumeDown):
					elapsed(lambda: self._change_volume(-2))
			except Exception:
				print(traceback.format_exc())

	def _change_volume(self, amount):
		try:
			current_volume = self._musiccast.get_volume()
			self._display.show_volume(current_volume)
			new_volume = current_volume + amount
			print(f"volume: {current_volume} => {new_volume}")
			try:
				self._musiccast.set_volume(new_volume)
				self._display.show_volume_set(new_volume)
			except YXCNonZeroResponseCodeException as e:
				if e.code == 5:
					# the power might be off; power on and retry
					self._musiccast.power_on()
					self._musiccast.set_volume(new_volume)
					self._display.show_volume_set(new_volume)
					
		except YXCNonZeroResponseCodeException as e:
			self._display.show_error(str(e.code))
			raise e

	def _on_mute(self):
		pass

	def _on_tv(self):
		pass

	def _on_blue(self):
		pass

if __name__ == "__main__":
	print("SpeakerIR starting")
	app = Application()
	print("app initialized")
	asyncio.ensure_future(app.run())
	loop = asyncio.get_event_loop()
	print("now running event loop")
	loop.run_forever()
	print("app has stopped. Thank you for playing Wing Commander!")