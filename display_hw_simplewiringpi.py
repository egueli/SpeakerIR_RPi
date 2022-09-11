from wiringpi import wiringPiSetupGpio, pinMode, digitalRead, digitalWrite, GPIO

CLK = 27
DIO = 17

class DisplayHardware():
    def __init__(self):
        wiringPiSetupGpio()
        self.clk = CLK
        self.dio = DIO

        pinMode(self.clk, GPIO.OUTPUT)
        pinMode(self.dio, GPIO.OUTPUT)
        digitalWrite(self.clk, 0)
        digitalWrite(self.dio, 0)
    
    def show_segments(self, segments):
        print("display show segments")
        digitalWrite(self.clk, GPIO.HIGH)
        digitalWrite(self.dio, GPIO.HIGH)
        digitalWrite(self.dio, GPIO.LOW)
        digitalWrite(self.clk, GPIO.LOW)

    def blank(self):
        pass
        
