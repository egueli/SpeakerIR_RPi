#!/usr/bin/python3

# Configure with:
# ir-keytable -D 100 -P 100
# sudo ir-keytable --write=acer.toml

import evdev
from evdev import ecodes, KeyEvent

device = evdev.InputDevice('/dev/input/by-path/platform-ir-receiver@18-event')

for event in device.read_loop():
	if event.type != ecodes.EV_KEY:
		continue

	if event.value not in [KeyEvent.key_down, KeyEvent.key_hold]:
		continue

	if event.code == ecodes.KEY_VOLUMEUP:
		print(f"volume up!   {event.timestamp()}")
	elif event.code == ecodes.KEY_VOLUMEDOWN:
		print(f"volume down! {event.timestamp()}")
	elif event.code == ecodes.KEY_MUTE:
		print(f"mute!        {event.timestamp()}")
	elif event.code == ecodes.KEY_TV:
		print(f"TV!          {event.timestamp()}")
	elif event.code == ecodes.KEY_BLUE:
		print(f"blue!        {event.timestamp()}")
		# print("time %15f type %3d code %3d value %d" % (event.timestamp(), event.type, event.code, event.value))


