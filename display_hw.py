import tm1637

CLK = 27
DIO = 17

class DisplayHardware():
    def __init__(self):
        self._tm = tm1637.TM1637(clk=CLK, dio=DIO)
    
    def show_segments(self, segments):
        print("display show segments")
        self._tm.write(segments)

    def blank(self):
        print("display blank")
        self._tm.show('    ')
