from gpioone_setup import *

if __name__ == "__main__":

    s = SetupExample(help="This provides a quick example to place text on a standard 1602A LCD.")

    s.rv("RS", "Command or Text flag")
    s.rv("E", "Execute current data")
    s.rv("D4", "Data4 - We do four bits at a time to save pins")
    s.rv("D5", "Data5")
    s.rv("D6", "Data6")
    s.rv("D7", "Data7")
                 
    s.setup()

    GPIO.setmode(GPIO.BCM)

    lcd_display = LcdDisplay(s.RS,s.E,s.D4,s.D5,s.D6,s.D7)

    while 1:

        lcd_display.line_1("This LCD Display")
        lcd_display.line_2("is very nice")

        sleep(3)

        lcd_display.line_1("And the code")
        lcd_display.line_2("is easy to use")

        sleep(3)
    
    GPIO.cleanup()
