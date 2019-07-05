import RPi.GPIO as GPIO

from gpioone import *

if __name__ == "__main__":


    GPIO.setmode(GPIO.BCM)
    lcd_display = LcdDisplay(4,5,6,22,25,21)

    while 1:

        lcd_display.line_1("This LCD Display")
        lcd_display.line_2("is very nice")

        sleep(3)

        lcd_display.line_1("And the code")
        lcd_display.line_2("is easy to use")

        sleep(3)
    
    GPIO.cleanup()

    

    