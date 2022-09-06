import evdev

device = evdev.InputDevice('/dev/input/by-path/platform-ir-receiver@18-event')
for event in device.read_loop():
	print(repr(event))
	if event.type == evdev.ecodes.EV_KEY:
		print(repr(evdev.events.KeyEvent(event)))


