#!/usr/bin/python3

# Run setup_ir.sh with root priviledges before running this.

import http.client
import json
import traceback
import asyncio
from display import Display
import time
from commands import *
from ir import *

class Application:
	def __init__(self):
		self._conn = http.client.HTTPConnection("192.168.0.106")
		self._display = Display()
		self._ir = IRCommandSource()

	async def run(self):
		self._display.show_welcome()
		async for command in self._ir.get_commands():
			if not command: continue

			try:
				self._display.show_ir()
				print(repr(command))
				# if command is VolumeUp:
				# 	elapsed(lambda: self._change_volume(2))
			except Exception:
				print(traceback.format_exc())

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
		current_volume = self._get_volume()
		self._display.show_volume(current_volume)
		new_volume = current_volume + amount
		self._set_volume(new_volume)
		self._display.show_volume_set(new_volume)

	def _on_vol_down(self):
		elapsed(lambda: self._change_volume(-2))

	def _on_mute(self):
		pass

	def _on_tv(self):
		pass

	def _on_blue(self):
		pass

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