import RPi.GPIO as GPIO
from math import atan2

class Joystick:
    """
    An interface to analog joysticks. This requires a working ADC connection.

    We attempt to perform simple calibration by default by assuming the 
    joystick is centered when the object is initialized.

    After that we can get normalized x/y readings, angle in degrees, or
    human readible cardinal directions.

    The optional button requires a connection to a GPIO pin and not the ADC.
    """
    def __init__(self, adc, adc_x_pin, adc_y_pin, button_pin=None, calibrate=True):
        self.adc = adc
        self.adc_x_pin = adc_x_pin
        self.adc_y_pin = adc_y_pin
        self.button_pin = button_pin

        if self.button_pin:
            GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Calibrate by assuming joystick isn't in use and
        # centered
        if calibrate:
            self.x_center = self.adc.get(self.adc_x_pin, percent=False)
            self.y_center = self.adc.get(self.adc_y_pin, percent=False)
        else:
            self.x_center = 512
            self.y_center = 512

    def raw_x(self):
        return self.adc.get(self.adc_x_pin, percent=False)

    def raw_y(self):
        return self.adc.get(self.adc_y_pin, percent=False)

    def vectorize(self,raw_value, center):
        if raw_value >= center:
            relative = raw_value - center
            vector = float(relative) / (1023 - center)
        else:
            vector = - (float(center - raw_value) / center)
        return vector
    
    def x(self):
        return self.vectorize(self.raw_x(), self.x_center)
        
    def y(self):
        return self.vectorize(self.raw_y(), self.y_center)

    def angle(self):
        x = self.x()
        y = self.y()

        # Don't return angle if we haven't moved far enough
        if abs(x) < 0.1 and abs(y) < 0.1:
            return None
        
        angle = atan2(x,-y) * 57.2958
        return angle

    def direction(self,four_dir=False):
        """
        Human readible cardinal directions.
        Defaults to eight directions, but can be set to four
        """
        a = self.angle()
        if a is None:
            return None

        if four_dir:
            if a >= -45 and a <= 45:
                return "UP"
            elif a >= 45 and a <= 135:
                return "RIGHT"
            elif a >= 135 or a <= -135:
                return "DOWN"
            elif a >= -135 and a <= -45:
                return "LEFT"
            else:
                raise RuntimeError("Couldn't figure out %f" % a)
        else:
            if a >= -22.5 and a <= 22.5:
                return "UP"
            elif a >= 22.5 and a <= 67.5:
                return "UP-RIGHT"
            elif a >= 67.5 and a <= 112.5:
                return "RIGHT"
            elif a >= 112.5 and a <= 157.5:
                return "DOWN-RIGHT"
            elif a >= 157.5 or a <= -157.5:
                return "DOWN"
            elif a >= -157.5 and a <= -112.5:
                return "DOWN-LEFT"
            elif a >= -112.5 and a <= -67.5:
                return "LEFT"
            elif a >= -67.5 and a <= -22.5:
                return "UP-LEFT"
            else:
                raise RuntimeError("Couldn't figure out %f" % a)
            
    def button(self):
        if self.button_pin is None:
            return None
        else:
            return GPIO.input(self.button_pin) == 0

        
