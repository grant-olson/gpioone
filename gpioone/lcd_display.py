import RPi.GPIO as GPIO
from time import sleep

class LcdDisplay:
    """
    Standard 1602A interface
    """

    def __init__(self, rs, e, d4, d5, d6, d7):
        self.rs = rs
        self.e = e
        self.d4 = d4
        self.d5 = d5
        self.d6 = d6
        self.d7 = d7

        self.sleep_time = 0.0005
        
        GPIO.setup(self.rs, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.e, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.d4, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.d5, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.d6, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.d7, GPIO.OUT, initial=GPIO.LOW)

        for initial_code in [
                0x33, # Initialize
                0x32, # 4 Bit
                0x06, # Cursor Direction
                0x0C, # Turn Cursor off
                0x28, # 2 line display
                0x01 # Clear Display
        ]:
            self.send_data(initial_code)

    def flip_enable(self):
        sleep(self.sleep_time)
        GPIO.output(self.e, GPIO.HIGH)
        sleep(self.sleep_time)
        GPIO.output(self.e, GPIO.LOW)
        sleep(self.sleep_time)

    def bit_set(self, value, bit):
        if (value & bit) == bit:
            return GPIO.HIGH
        else:
            return GPIO.LOW
        
    def send_data(self, value, char=False):
        if char == True:
            GPIO.output(self.rs, GPIO.HIGH)
        else:
            GPIO.output(self.rs, GPIO.LOW)
        
        GPIO.output(self.d4, self.bit_set(value, 0x10))
        GPIO.output(self.d5, self.bit_set(value, 0x20))
        GPIO.output(self.d6, self.bit_set(value, 0x40))
        GPIO.output(self.d7, self.bit_set(value, 0x80))

        self.flip_enable()

        GPIO.output(self.d4, self.bit_set(value, 0x01))
        GPIO.output(self.d5, self.bit_set(value, 0x02))
        GPIO.output(self.d6, self.bit_set(value, 0x04))
        GPIO.output(self.d7, self.bit_set(value, 0x08))

        self.flip_enable()

    def line_1(self, text):
        text = text.ljust(16, " ")
        self.send_data(0x80)
        for char in text:
            self.send_data(ord(char), char=True)
            
    def line_2(self, text):
        text = text.ljust(16, " ")
        self.send_data(0xC0)
        for char in text:
            self.send_data(ord(char), char=True)
            
