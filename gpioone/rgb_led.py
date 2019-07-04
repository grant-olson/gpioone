import RPi.GPIO as GPIO
from time import sleep
import math

class RgbLed:
    """
    Control an Rgb Led off of three specified GPIO pins.

    You can either toggle the individual leds on and off, or set
    intensity as a percentage between 0 and 100.

    Don't forget to include resistors when wiring it up!
    """
    def __init__(self, red_pin, green_pin, blue_pin):
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin

        GPIO.setup(self.red_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.green_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.blue_pin, GPIO.OUT, initial=GPIO.LOW)

        self.red_pwm = GPIO.PWM(self.red_pin, 100)
        self.green_pwm = GPIO.PWM(self.green_pin, 100)
        self.blue_pwm = GPIO.PWM(self.blue_pin, 100)

        self.cycle_position = 0
        
    # set_rgb_state simply turn leds on and off
    def set_state(self, pin, state):
        GPIO.output(pin, state)
        
    def set_red_state(self, state):
        self.set_state(self.red_pin, state)

    def set_green_state(self, state):
        self.set_state(self.green_pin, state)

    def set_blue_state(self, state):
        self.set_state(self.blue_pin, state)

    # set_rgb_intensity sets percentage
    def set_red_intensity(self, intensity):
        self.red_pwm.ChangeDutyCycle(intensity)

    def set_green_intensity(self, intensity):
        self.green_pwm.ChangeDutyCycle(intensity)
        
    def set_blue_intensity(self, intensity):
        self.blue_pwm.ChangeDutyCycle(intensity)

    def start_intensity_mode(self):
        self.red_pwm.start(0)
        self.blue_pwm.start(0)
        self.green_pwm.start(0)

    def stop_intensity_mode(self):
        self.red_pwm.stop()
        self.blue_pwm.stop()
        self.green_pwm.stop()

    def cycle_position_as_percent(self,offset=0):
        sine = math.sin(float(self.cycle_position + offset) * math.pi / 180.0)
        percent = (sine * 50) + 50
        return percent

    def cycle_intensity(self):
        """
        Create a pleasant color cycle on the LED. Intended to show that 
        an app is still running in a headless environment, where it would
        be called once every round of the main working loop.
        """
        self.cycle_position += 1
        if self.cycle_position >= 360:
            self.cycle_position = 0

        self.set_red_intensity(self.cycle_position_as_percent())
        self.set_blue_intensity(self.cycle_position_as_percent(45))
        self.set_green_intensity(self.cycle_position_as_percent(90))
        
