# This is a harness to run from source, if using the installed package use:
# from gpioone import *
from gpioone_setup import * 

from time import sleep


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    s = SetupExample(help="""Read data from an MCP3008 Analog-to-Digital chip.

To connect the chip, the actual data uses SPI, so we must set up those chips in addition to the normal chip fed with the envirnoment variable. In this case we wnat to set SPIMOSI to pin 11 (Din) the SPIMISO to pin 12 (Dout) and SPISCLK to pin 13(CLK). See the datasheet for more info on hooking up pins.

""")

    s.rv("CHIP_SELECT", "Chip select pin")

    s.setup()
    
    mcp = MCP3008(s.CHIP_SELECT)
    while 1:
        for i in range(8):
            print("INPUT %s: %d%%" % (i, mcp.get(input=i) * 100))
            sleep(0.1)
        print("")
        sleep(1.0)
