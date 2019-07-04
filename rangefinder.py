import RPi.GPIO as GPIO
from gpioone import Ultrasonic
import rgb_led
from time import sleep

GPIO.setmode(GPIO.BCM)

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
        
        self.led = rgb_led.RgbLed(red_pin, green_pin, blue_pin)

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
        

if __name__ == "__main__":
    r_io_pin = 4
    g_io_pin = 5
    b_io_pin = 6

    reporter = RgbDistanceReporter(r_io_pin, g_io_pin, b_io_pin)


    ultrasonic_echo = 25 # 21
    ultrasonic_trigger = 22 # 20

    max_distance = 10.0

    us = Ultrasonic(ultrasonic_echo, ultrasonic_trigger, max_distance, reporter)
    us.run()

    GPIO.cleanup()
