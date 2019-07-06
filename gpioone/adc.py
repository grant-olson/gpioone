import RPi.GPIO as GPIO
import spidev

class MCP300x:
    def __init__(self, chip_select):
        self.chip_select = chip_select
        GPIO.setup(chip_select, GPIO.OUT, initial=GPIO.LOW)
        self.spi = spidev.SpiDev()
        try:
            self.spi.open(0,0)
        except IOError:
            raise RuntimeError("Couldn't attach to SPI. This is disabled by default. Have you enabled it in raspbi-config?")
        self.spi.max_speed_hz = 1350000
    

    def reset(self):
        GPIO.output(self.chip_select, GPIO.HIGH)
        GPIO.output(self.chip_select, GPIO.LOW)

    def shutdown(self):
        """Pause and throw in to low power mode."""
        GPIO.output(self.chip_select, GPIO.HIGH)
        
    def get(self, input=0, percent=True):
        """
        Get the analog value from a given input. by defualt, return
        percent between 0 and 1. Set percent to False to get a number
        between 0-1023.
        """
        # Need to flip chip select every time for chip to listen
        self.reset()

        # The one here triggers listen mode, and the chip listens after that.
        input_byte_1 = 1
        # The real payload: Highest bit is single-ended input, next three
        # are pin 0-7
        input_byte_2 = 128 # single ended
        input_byte_2 += (input << 4) # pin of choice
        #Padding while we wait for answer
        input_byte_3 = 0
        
        value = self.spi.xfer2([input_byte_1, input_byte_2, input_byte_3])

        # The return value is 3 packed bytes, with the last 10 bits
        # being the ADC entry
        #
        # take bits 1 and 2 from byte 2, shift and add
        # byte 3 to get the 10 bit value.
        byte_2 = value[1]
        byte_3 = value[2]
        unpacked = ((byte_2 & 3) << 8) + byte_3

        if percent:
            return float(unpacked) / 1023
        else: # 10 bit value 0-1023
            return unpacked
            

class MCP3008(MCP300x):
    pass

# 4 just has 4 inputs, and ignores the high bit, so the code
# is identical but you won't get values for 4-7
class MCP3004(MCP300x):
    pass

