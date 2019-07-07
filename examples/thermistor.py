# This is a harness to run from source, if using the installed package use:
# from gpioone import *
from gpioone_setup import * 

from time import sleep
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    s = SetupExample(help="""Get temerature via ADC and Thermistor. In general take the ADC reading at the midpoint of a thermistor and 10k resistor wired in series.""")

    s.rv("CHIP_SELECT", "Chip select pin")
    s.rv("THERMISTOR", "Reading pin on ADC chip.")
    
    s.setup()
    
    mcp = MCP3008(s.CHIP_SELECT)
    thermistor = Thermistor(mcp, s.THERMISTOR)
   
    while 1:
        print "Temp: %0.2f C %0.2f F" % (thermistor.c(), thermistor.f())
        
        sleep(1.0)
