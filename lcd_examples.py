import RPi.GPIO as GPIO
from gpioone import *

if __name__ == "__main__":

    setup = SetupExample(help="This provides a quick example to place text on a standard 1602A LCD.")

    setup.rv("RS", "Command or Text flag")
    setup.rv("E", "Execute current data")
    setup.rv("D4", "Data4 - We do four bits at a time to save pins")
    setup.rv("D5", "Data5")
    setup.rv("D6", "Data6")
    setup.rv("D7", "Data7")
                 
    setup.setup()

    GPIO.setmode(GPIO.BCM)
    lcd_display = LcdDisplay(RS,E,D4,D5,D6,D7)

    while 1:

        lcd_display.line_1("This LCD Display")
        lcd_display.line_2("is very nice")

        sleep(3)

        lcd_display.line_1("And the code")
        lcd_display.line_2("is easy to use")

        sleep(3)
    
    GPIO.cleanup()
