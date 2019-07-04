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
        "T": B + G + C,
        "U": E + D + C,
        "V": E + D + C,
        "Y": F + G + B + C,
        
        
        "?": A + B + G + E
        }

    @staticmethod
    def value(character, decimal_point=False):
        if len(character) <> 1:
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

def led_strip_example(shift_register):
    # Example is hooked up to 8 LEDs with 220 Ohm resistors between
    # anode and Shift Register pins.

    sleep_time = 0.025
    # Count to 255 displaying binary
    for i in range(0,256):
        shift_register.number(i)
        sleep(sleep_time)
    
    # As a demonstration of actual shifting, we only load one bit at a time
    # and trigger the latch. One out of every seven bits is high, so
    # it looks like the light moves down the line of LEDs
    while 1:
        shift_register.high()
        shift_register.clock_tick()
        shift_register.trigger_latch()
        sleep(sleep_time)
        shift_register.low()
        for i in range(0,7):
            shift_register.clock_tick()
            shift_register.trigger_latch()
            sleep(sleep_time)

def segment_example(shift_register):
    for i in range(0,10):
        if i % 2:
            shift_register.number(SegmentDisplay.value(str(i)))
        else:
            shift_register.number(SegmentDisplay.value(str(i), decimal_point=True))
        sleep(0.5)

    counter = 0
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXZY":
        counter += 1
        shift_register.character(c, decimal_point=(counter / 2))
        sleep(0.5)

    shift_register.number(0)


def multi_segment_example(shift_register):
    """
    Use four IO pins to control a 4 digit seven segment display.

    TODO: Chain two shift registers together for the slot control
    logic to free the pins back up.
    """
    first = 18
    second = 19
    third = 23
    fourth = 24

    #19, 18 ,23, 25
    GPIO.setup(first, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(second, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(third, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(fourth, GPIO.OUT, initial=GPIO.HIGH)

    sleep_time = 0.001

    text = "HELP "
    while True:
        for i in range(100):
            shift_register.character(text[0])
            GPIO.output(first, GPIO.LOW)
            sleep(sleep_time)
            GPIO.output(first, GPIO.HIGH)

            shift_register.character(text[1])
            GPIO.output(second, GPIO.LOW)
            sleep(sleep_time)
            GPIO.output(second, GPIO.HIGH)#

            shift_register.character(text[2])
            GPIO.output(third, GPIO.LOW)
            sleep(sleep_time)
            GPIO.output(third, GPIO.HIGH)

            shift_register.character(text[3])
            GPIO.output(fourth, GPIO.LOW)
            sleep(sleep_time)
            GPIO.output(fourth, GPIO.HIGH)

        text = text[1:] + text[0]
    
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    latch = 20 # 21
    clock = 16 # 20
    data = 21 # 16
    
    shift_register = ShiftRegister(data, clock, latch)
#    segment_example(shift_register)
    multi_segment_example(shift_register)
    GPIO.cleanup()
