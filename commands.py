class Command():
	pass

class VolumeUp(Command):
	pass

class VolumeDown(Command):
    pass

class Mute(Command):
    pass

class SetInput(Command):
    pass

class ToggleClock(Command):
    pass

class DeviceNotOnException(Exception):
    pass