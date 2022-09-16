#!/usr/bin/python3

# Run setup_ir.sh with root priviledges before running this.

import traceback
import asyncio
import time
from display import Display
from elapsed import *
from commands import *
from ir import *
from musiccast import *
from clock import *

class Application:
	def __init__(self):
		self._display = Display()
		self._ir = IRCommandSource()
		self._musiccast = MusicCast()
		self._clock = Clock(self._display)

	async def run(self):
		self._display.show_welcome()
		self._clock.start()
		async for command in self._ir.get_commands():
			if not command: continue
			delta = time.time() - command.timestamp
			if delta > 0.5:
				print(f"discarding {command}, too old")
				continue

			try:
				print(f"=== {command}")
				if isinstance(command, ToggleClock):
					# This a "simple" command that will have effect immediately.
					# So don't show the IR confirmation.
					self._clock.toggle()
				else:
					self._display.show_ir()
					if isinstance(command, VolumeUp):
						elapsed(lambda: self._change_volume(1))
					elif isinstance(command, VolumeDown):
						elapsed(lambda: self._change_volume(-1))
					elif isinstance(command, Mute):
						elapsed(lambda: self._toggle_mute())
					elif isinstance(command, SetInput):
						elapsed(lambda: self._set_input())
			except DeviceNotOnException:
				print(traceback.format_exc())
				self._display.show_error_invalid_state()
			except YXCNonZeroResponseCodeException as e:
				print(traceback.format_exc())
				self._display.show_error_numeric(e.code)
			except Exception as e:
				print(traceback.format_exc())
				self._display.show_error_other(e)

	def _change_volume(self, amount):
		self._ensure_on()
		current_volume = self._musiccast.get_volume()
		self._display.show_volume(current_volume)
		new_volume = current_volume + amount
		print(f"volume: {current_volume} => {new_volume}")
		self._musiccast.set_volume(new_volume)
		self._display.show_volume_set(new_volume)

	def _toggle_mute(self):
		self._ensure_on()
		is_muted = self._musiccast.get_is_muted()
		self._display.show_mute(is_muted)
		new_is_muted = not is_muted
		print(f"muted: {is_muted} => {new_is_muted}")
		self._musiccast.set_muted(new_is_muted)
		self._display.show_mute_set(new_is_muted)

	def _set_input(self):
		self._musiccast.power_on()
		# My TV is connected to Optical1 input
		self._musiccast.set_input("optical1")
		# My "A" speakers are big and far from the TV, and will be off.
		self._musiccast.set_speaker("a", False)
		# My "B" speakers are near the TV and will be on.
		self._musiccast.set_speaker("b", True)
		self._display.show_tv_input_set()

	def _on_blue(self):
		pass

	def _ensure_on(self):
		if not self._musiccast.is_on():
			raise DeviceNotOnException()

if __name__ == "__main__":
	print("SpeakerIR starting")
	app = Application()
	print("app initialized")
	asyncio.ensure_future(app.run())
	loop = asyncio.get_event_loop()
	print("now running event loop")
	loop.run_forever()
	print("app has stopped. Thank you for playing Wing Commander!")