from rangefinder import *
from shift_register import *
class SegmentReporter:
    def __init__(self):
        latch = 20 # 21
        clock = 16 # 20
        data = 21 # 16

        self.first = 18
        self.second = 19
        self.third = 23
        self.fourth = 24

        GPIO.setup(self.first, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.second, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.third, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.fourth, GPIO.OUT, initial=GPIO.HIGH)
        
        self.shift_register = ShiftRegister(data, clock, latch)

    def report(self, distance):
        whole, fraction = str(distance).split(".")
        dp = len(whole) - 1
        text = whole + fraction

        sleep_time = 0.001
        
        for i in range(100):
            self.shift_register.character(text[0], decimal_point=(dp==0) )
            GPIO.output(self.first, GPIO.LOW)
            sleep(sleep_time)
            GPIO.output(self.first, GPIO.HIGH)

            self.shift_register.character(text[1], decimal_point=(dp==1) )
            GPIO.output(self.second, GPIO.LOW)
            sleep(sleep_time)
            GPIO.output(self.second, GPIO.HIGH)#

            self.shift_register.character(text[2], decimal_point=(dp==2) )
            GPIO.output(self.third, GPIO.LOW)
            sleep(sleep_time)
            GPIO.output(self.third, GPIO.HIGH)

            self.shift_register.character(text[3], decimal_point=(dp==3) )
            GPIO.output(self.fourth, GPIO.LOW)
            sleep(sleep_time)
            GPIO.output(self.fourth, GPIO.HIGH)

        
if __name__ == "__main__":
#    r_io_pin = 4
#    g_io_pin = 5
#    b_io_pin = 6

#    reporter = RgbDistanceReporter(r_io_pin, g_io_pin, b_io_pin)


    ultrasonic_echo = 25
    ultrasonic_trigger = 22

    max_distance = 10.0

    us = Ultrasonic(ultrasonic_echo, ultrasonic_trigger, max_distance, SegmentReporter())
    us.run()

    GPIO.cleanup()
