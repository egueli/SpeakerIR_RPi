#!/usr/bin/python3

# Configure with:
# ir-keytable -D 100 -P 100
# sudo ir-keytable --write=acer.toml

import evdev
from evdev import ecodes, KeyEvent
import http.client
import json

conn = http.client.HTTPConnection("192.168.0.106")

def change_volume(amount):
	conn.request("GET", "/YamahaExtendedControl/v1/main/getStatus")
	res = conn.getresponse()
	res_body = res.read()
	yxc_status = json.loads(res_body)
	repr(yxc_status)

def on_vol_up():
	change_volume(1)

def on_vol_down():
	change_volume(-1)

def on_mute():
	pass

def on_tv():
	pass

def on_blue():
	pass


device = evdev.InputDevice('/dev/input/by-path/platform-ir-receiver@18-event')

for event in device.read_loop():
	if event.type != ecodes.EV_KEY:
		continue

	if event.value not in [KeyEvent.key_down, KeyEvent.key_hold]:
		continue

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
