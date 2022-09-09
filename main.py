#!/usr/bin/python3

# Run setup_ir.sh with root priviledges before running this.

import evdev
from evdev import ecodes, KeyEvent
import http.client
import json
import traceback
import asyncio
from display import Display

conn = http.client.HTTPConnection("192.168.0.106")

def get_volume():
	conn.request("GET", "/YamahaExtendedControl/v1/main/getStatus")
	res = conn.getresponse()
	res_body = res.read()
	yxc_status = json.loads(res_body)
	return yxc_status['volume']

def set_volume(volume):
	conn.request("GET", f"/YamahaExtendedControl/v1/main/setVolume?volume={volume}")
	res = conn.getresponse()
	res_body = res.read()
	yxc_status = json.loads(res_body)
	response_code = yxc_status['response_code']
	if response_code != 0:
		raise Exception(f"non-zero response code, got {response_code}")

def change_volume(amount):
	set_volume(get_volume() + amount)

def on_vol_up():
	change_volume(2)

def on_vol_down():
	change_volume(-2)

def on_mute():
	pass

def on_tv():
	pass

def on_blue():
	pass


device = evdev.InputDevice('/dev/input/by-path/platform-ir-receiver@18-event')

def process_event(event):
	if event.type != ecodes.EV_KEY:
		return

	if event.value not in [KeyEvent.key_down, KeyEvent.key_hold]:
		return

	if event.code == ecodes.KEY_VOLUMEUP:
		on_vol_up()
	elif event.code == ecodes.KEY_VOLUMEDOWN:
		on_vol_down()
	elif event.code == ecodes.KEY_MUTE:
		on_mute()
	elif event.code == ecodes.KEY_TV:
		on_tv()
	elif event.code == ecodes.KEY_BLUE:
		on_blue()
		# print("time %15f type %3d code %3d value %d" % (event.timestamp(), event.type, event.code, event.value))

async def main():
	d = Display()
	ir_event_loop()

async def ir_event_loop():
	for event in device.read_loop():
		try:
			process_event(event)
		except Exception:
			print(traceback.format_exc())

asyncio.ensure_future(main())
loop = asyncio.get_event_loop()
loop.run_forever()