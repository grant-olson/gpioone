import RPi.GPIO as GPIO
from time import sleep

class SegmentDisplay:
    # Wire up shift register in this order!
    A = 1 << 0 # Top vertical
    B = 1 << 1 # Top Right Side
    C = 1 << 2 # Bottom Right Side
    D = 1 << 3 # Bottom Vertical
    E = 1 << 4 # Bottom left side    
    F = 1 << 5 # Top left side
    G = 1 << 6 # Middle Vertical
    DP = 1 << 7 # Decimal Point

    DISPLAY = {
        "0": A + B + C + D + E + F,
        "1": B + C,
        "2": A + B + G + E + D,
        "3": A + B + C + D + G,
        "4": F + G + B + C,
        "5": A + F + G + C + D,
        "6": F + E + G + D + C,
        "7": A + B + C,
        "8": A + B + C + D + E + F + G,
        "9": A + B + G + F + C,

        " ": 0,

        "A": A + B + F + G + E + C,
        "B": A + B + C + D + E + F + G,
        "C": A + F + E + D,
        "D": B + C + D + G + E,
        "E": A + F + G + E + D,
        "F": A + F + G + E,
        "G": A + B + F + G + C + D,
        "H": F + B + G + E + C,
        "I": F + E,
        "J": B + C + D + E,
        "L": F + E + D,
        "N": E + G + C,
        "O": E + G + C + D,
        "P": A + B + G + F + E,
        "R": E + G,
        "S": A + F + G + C + D,
        "T": D + F + E + G,
        "U": E + D + C,
        "V": E + D + C,
        "Y": F + G + B + C,
        
        
        "?": A + B + G + E + DP,
        "!": B + DP,
        ".": DP
        }

    @staticmethod
    def value(character, decimal_point=False):
        if len(character) != 1:
            raise "Only one char!"
        if character in SegmentDisplay.DISPLAY:
            v = SegmentDisplay.DISPLAY[character.upper()]
        else:
            v = SegmentDisplay.DISPLAY["?"]
        if decimal_point:
            v += SegmentDisplay.DP
        return v
        
class ShiftRegister:
    """
    Interface for a shift register such as 74HC595 or clone
    """
    def __init__(self, data, clock, latch):
        self.data = data
        self.clock = clock
        self.latch = latch

        GPIO.setup(self.latch, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.clock, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.data, GPIO.OUT, initial=GPIO.LOW)

        self.clear()

    def clear(self):
        self.low
        for i in range(0,8):
            self.clock_tick()
        self.trigger_latch()
        
    def clock_tick(self):
        GPIO.output(self.clock, GPIO.HIGH)
        GPIO.output(self.clock, GPIO.LOW)

    def trigger_latch(self):
        GPIO.output(self.latch, GPIO.HIGH)
        GPIO.output(self.latch, GPIO.LOW)

    def high(self):
        GPIO.output(self.data, GPIO.HIGH)
        
    def low(self):
        GPIO.output(self.data, GPIO.LOW)

    # Load up a number, with pin 0 being LSB and 7 being MSB
    def number(self, n):
        for i in range(7,-1,-1):
            bit = 1 << i
            if (bit & n) > 0:
                self.high()
            else:
                self.low()
            self.clock_tick()
        self.trigger_latch()

    def character(self, c, decimal_point=False):
        self.number(SegmentDisplay.value(c,decimal_point=decimal_point))

