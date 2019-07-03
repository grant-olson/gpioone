import RPi.GPIO as GPIO
from time import sleep

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

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    latch = 20 # 21
    clock = 16 # 20
    data = 21 # 16
    
    shift_register = ShiftRegister(data, clock, latch)

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
    
    GPIO.cleanup()
