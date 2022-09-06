#!/usr/bin/python3

import evdev

device = evdev.InputDevice('/dev/input/by-path/platform-ir-receiver@18-event')

for event in device.read_loop():
	if event.type == evdev.ecodes.EV_KEY:
		print("time %15f type %3d code %3d value %d" % (event.timestamp(), event.type, event.code, event.value))


