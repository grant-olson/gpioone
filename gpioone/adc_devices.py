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

        
from math import log

class Thermistor:
    def __init__(self, adc, analog_pin, b_value=None):
        if b_value is None:
            print("WARNING. No B Value set!")
            print("WARNING: You should try to get this from manufacturer datasheet.")
            print("WARNING: Guessing 4000 which may or may not provide reasoable results")
            self.b = 4000
        else:
            self.b = b_value
            
        self.adc = adc
        self.analog_pin = analog_pin

    # There is some tricky math here. I used the B equation as listed at:
    #
    # https://www.jameco.com/Jameco/workshop/TechTip/temperature-measurement-ntc-thermistors.html
    #
    # Wikipedia also provides a bunch of information:
    #
    # https://en.wikipedia.org/wiki/Thermistor
    def kelvin(self):
        reading = self.adc.get(input=self.analog_pin, percent=False)
        ln = log((1024.0/reading) - 1)
        inverse_temp = (1.0/298.15) + (1.0/self.b * ln)
        temp = 1.0 / inverse_temp

        return temp

    def k(self):
        self.kelvin()
    
    def centigrade(self):
        return self.kelvin() - 273.15

    def c(self):
        return self.centigrade()
    
    def fahrenheit(self):
        return (self.centigrade() * 9 / 5) + 32

    def f(self):
        return(self.fahrenheit())

