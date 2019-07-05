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

    s = SetupExample(help="Rangefinder with multiple displays")

    s.rv("ECHO","Echo Pin")
    s.rv("TRIGGER", "Trigger Pin")

    s.ov("RGB_RED", "RGB LED Red Pin")
    s.ov("RGB_GREEN", "RGB LED Green Pin")
    s.ov("RGB_BLUE", "RGB LED Blue Pin")
    
    s.ov("SEGMENT_LATCH", "Latch on Shift Register")
    s.ov("SEGMENT_CLOCK", "Clock on Shift Register")
    s.ov("SEGMENT_DATA", "Data on shift register")
    s.ov("SEGMENT_LED_1", "LED 1 Control Pin")
    s.ov("SEGMENT_LED_2", "LED 2 Control Pin")
    s.ov("SEGMENT_LED_3", "LED 3 Control Pin")
    s.ov("SEGMENT_LED_4", "LED 4 Control Pin")
    
    s.ov("LCD_RS", "LCD command/character flag")
    s.ov("LCD_E", "LCD execute command")
    s.ov("LCD_D4", "LCD Data 4 Pin")
    s.ov("LCD_D5", "LCD Data 5 Pin")
    s.ov("LCD_D6", "LCD Data 6 Pin")
    s.ov("LCD_D7", "LCD Data 7 Pin")

    s.setup()
    
    if hasattr(s,"RGB_RED"):
        r_io_pin = s.RGB_RED
        g_io_pin = s.RGB_GREEN
        b_io_pin = s.RGV_BLUE

        reporter = RgbDistanceReporter(r_io_pin, g_io_pin, b_io_pin)

    elif False:
        reporter = SegmentReporter(
            s.SEGMENT_LATCH, s.SEGMENT_CLOCK, s.SEGMENT_DATA,
            s.SEGMENT_LED_1, s.SEGMENT_LED_2, s.SEGMENT_LED_3, s.SEGMENT_LED_4
        )
    elif hasattr(s,"LCD_E"):
        reporter = LcdReporter(s.LCD_RS, s.LCD_E, s.LCD_D4, s.LCD_D5, s.LCD_D6, s.LCD_D7)
    else:
        raise SystemError("Need either LCD, RGB, or SEGMENT configured")
        
    ultrasonic_echo = 20
    ultrasonic_trigger = 16
    max_distance = 10.0

    us = Ultrasonic(s.ECHO, s.TRIGGER, max_distance, reporter)
    us.run()

    GPIO.cleanup()
