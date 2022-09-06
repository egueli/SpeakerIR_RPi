import evdev

device = evdev.InputDevice('/dev/input/by-path/platform-ir-receiver@18-event')
for event in device.read_loop():
	#if event.type == evdev.ecodes.EV_KEY:
		print(repr(event))


