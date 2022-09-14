class Command():
    def __init__(self, timestamp):
        self.timestamp = timestamp
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}@{self.timestamp}"

class VolumeUp(Command):
    def __init__(self, timestamp):
        super().__init__(timestamp)

class VolumeDown(Command):
    def __init__(self, timestamp):
        super().__init__(timestamp)

class Mute(Command):
    def __init__(self, timestamp):
        super().__init__(timestamp)

class SetInput(Command):
    def __init__(self, timestamp):
        super().__init__(timestamp)

class ToggleClock(Command):
    def __init__(self, timestamp):
        super().__init__(timestamp)

class DeviceNotOnException(Exception):
    pass