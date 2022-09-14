import tm1637
from gpiozero import Device

CLK = 27
DIO = 17

BRIGHT = 7
DIM = 2

class DisplayHardware():
    def __init__(self):
        self._tm = tm1637.TM1637(clk=CLK, dio=DIO)
        print("pin factory: " + str(Device._default_pin_factory()))
    
    def show_segments(self, segments):
        self._tm.write(segments)

    def encode_string(self, string):
        return self._tm.encode_string(string)

    def dim(self):
        self._tm.brightness(DIM)

    def bright(self):
        self._tm.brightness(BRIGHT)
