import RPi.GPIO as GPIO
from gpioone import *
from time import sleep

class RgbDistanceReporter:
    """
    Create a primitive range display. Use a RGB LED to show approximately 
    how close things are:

    Bright Red - very close
    Not so Bright Red - close
    Bright Blue - Medium Close
    Bright Green - Far

    Brightness dims for each category as we get further away.
    """
    def __init__(self, red_pin, green_pin, blue_pin):
        self.near_threshold = 1.0
        self.medium_threshold = 3.0
        self.max_distance = 10.0
        
        self.led = RgbLed(red_pin, green_pin, blue_pin)

        # Blink to let us know it's on
        for x in range(0,3):
            self.led.set_green_state(GPIO.HIGH)
            sleep(0.2)
            self.led.set_green_state(GPIO.LOW)
            sleep(0.05)


        self.led.start_intensity_mode()

    def get_inverse_percent(self, min, max, actual):
        ip =  100.0 - ((actual - min) / (max - min) * 100.0)
        if ip < 20:
            ip = 20
        return ip

        
    def report(self, distance):
        red = 0
        green = 0
        blue = 0
        
        if distance <= self.near_threshold:
            red = self.get_inverse_percent(0.0, self.near_threshold, distance)
        elif distance <= self.medium_threshold:
            blue = self.get_inverse_percent(self.near_threshold, self.medium_threshold, distance)
        else:
            green = self.get_inverse_percent(self.medium_threshold, self.max_distance, distance)
        self.led.set_red_intensity(red)
        self.led.set_green_intensity(green)
        self.led.set_blue_intensity(blue)

class LcdReporter:
    def __init__(self, rs, e, d4, d5, d6, d7):
        self.lcd_display = LcdDisplay(rs,e,d4,d5,d6,d7)

    def report(self, distance):
        self.lcd_display.line_1("%0.2f meters" % distance)
        decimal_feet = distance * 3.3
        feet = int(decimal_feet)
        decimal_inches = decimal_feet - feet
        inches = decimal_inches * 12
        self.lcd_display.line_2("%d ft, %0.2f in" % (feet, inches))
        
class SegmentReporter:
    def __init__(self, latch, clock, data, s1, s2, s3, s4):
        self.first = s1
        self.second = s2
        self.third = s3
        self.fourth = s4

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
    GPIO.setmode(GPIO.BCM)

    if False:
        r_io_pin = 4
        g_io_pin = 5
        b_io_pin = 6

        reporter = RgbDistanceReporter(r_io_pin, g_io_pin, b_io_pin)

    elif False:
        reporter = SegmentReporter(20, 16, 21, 18, 19, 23, 24)
    else:
        rs = 4
        e = 5
        d4 =6
        d5 = 22
        d6 = 25
        d7 = 21
        reporter = LcdReporter(rs, e, d4, d5, d6, d7)
        
    ultrasonic_echo = 20
    ultrasonic_trigger = 16
    max_distance = 10.0

    us = Ultrasonic(ultrasonic_echo, ultrasonic_trigger, max_distance, reporter)
    us.run()

    GPIO.cleanup()