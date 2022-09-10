#!/usr/bin/python3

# Run setup_ir.sh with root priviledges before running this.

import evdev
from evdev import ecodes, KeyEvent
import http.client
import json
import traceback
import asyncio
from display import Display
import time

class Application:
	def __init__(self):
		self._conn = http.client.HTTPConnection("192.168.0.106")
		self._device = evdev.InputDevice('/dev/input/by-path/platform-ir-receiver@18-event')
		self._display = Display()

	async def run(self):
		self._display.show_welcome()
		await self._ir_event_loop()

	def _get_volume(self):
		self._conn.request("GET", "/YamahaExtendedControl/v1/main/getStatus")
		res = self._conn.getresponse()
		res_body = res.read()
		yxc_status = json.loads(res_body)
		return yxc_status['volume']

	def _set_volume(self, volume):
		self._conn.request("GET", f"/YamahaExtendedControl/v1/main/setVolume?volume={volume}")
		res = self._conn.getresponse()
		res_body = res.read()
		yxc_status = json.loads(res_body)
		response_code = yxc_status['response_code']
		if response_code != 0:
			raise Exception(f"non-zero response code, got {response_code}")

	def _change_volume(self, amount):
		self._set_volume(self._get_volume() + amount)

	def _on_vol_up(self):
		elapsed(lambda: self._change_volume(2))

	def _on_vol_down(self):
		elapsed(lambda: self._change_volume(-2))

	def _on_mute(self):
		pass

	def _on_tv(self):
		pass

	def _on_blue(self):
		pass

	def _process_event(self, event):
		if event.type != ecodes.EV_KEY:
			return

		if event.value not in [KeyEvent.key_down, KeyEvent.key_hold]:
			return

		self._display.show_ir()

		if event.code == ecodes.KEY_VOLUMEUP:
			self._on_vol_up()
		elif event.code == ecodes.KEY_VOLUMEDOWN:
			self._on_vol_down()
		elif event.code == ecodes.KEY_MUTE:
			self._on_mute()
		elif event.code == ecodes.KEY_TV:
			self._on_tv()
		elif event.code == ecodes.KEY_BLUE:
			self._on_blue()
			# print("time %15f type %3d code %3d value %d" % (event.timestamp(), event.type, event.code, event.value))

	async def _ir_event_loop(self):
		async for event in self._device.async_read_loop():
			try:
				self._process_event(event)
			except Exception:
				print(traceback.format_exc())

def elapsed(func):
	start_at = time.time()
	func()
	end_at = time.time()
	duration = end_at - start_at
	print(f"duration: {duration*1000}ms")

if __name__ == "__main__":
	print("SpeakerIR starting")
	app = Application()
	print("app initialized")
	asyncio.ensure_future(app.run())
	loop = asyncio.get_event_loop()
	print("now running event loop")
	loop.run_forever()
	print("app has stopped. Thank you for playing Wing Commander!")