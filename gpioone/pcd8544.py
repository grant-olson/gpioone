import RPi.GPIO as GPIO
import spidev
import unscii
from time import sleep

class PCD8544(object):
    def __init__(self,dc,reset,font='unscii_8_thin_transposed'):
        self.unscii = unscii.unscii(font)
        self.data_control = dc
        self.reset = reset

        GPIO.setup(self.data_control, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.reset, GPIO.OUT, initial=GPIO.HIGH)
        
        self.spi = spidev.SpiDev()

        self.spi.open(0,0)

        self.spi.no_cs = True
        self.spi.max_speed_hz = 4000000
        
        # Reset LOW resets, mandatory to avoid damaging chip
        GPIO.output(self.reset, GPIO.LOW)
        sleep(0.1)
        GPIO.output(self.reset, GPIO.HIGH)
        sleep(0.1)
        
        self.init_lcd()


 #   def __del__(self):
 #       self.spi.close()
        
    def bits2byte(self,a,b,c,d,e,f,g,h):
        return (
            (a << 7) + (b << 6) + (c << 5) + (d << 4) +
            (e << 3) + (f << 2) + (g << 1) + h )

    def init_lcd(self):

        init_control = [ (0,0,1,0,0,0,0,1), # on/extended instruction
                         (0,0,0,1,0,1,0,0), # set bias
                         (1,0,1,1,1,1,1,1), # Set Vop
                         (0,0,1,0,0,0,0,0), # Not extended instructions
                         (0,0,0,0,1,1,0,0), # display control set normal
        ]

        for c in init_control:
            self.command_bits(*c)

    def command(self,c):
        GPIO.output(self.data_control, GPIO.LOW)
        self.spi.writebytes([c])
        
    def data(self,d):
        GPIO.output(self.data_control, GPIO.HIGH)
        self.spi.writebytes([d])
        
    def clear(self):
        for i in range(84*48//8):
            self.data(0)
            
    def data_bits(self,a,b,c,d,e,f,g,h):
        self.data(self.bits2byte(a,b,c,d,e,f,g,h))
    
    def command_bits(self,a,b,c,d,e,f,g,h):
        self.command(self.bits2byte(a,b,c,d,e,f,g,h))

    def print_char(self,c):
        char_bytes = self.unscii.get_char(c)
        for b in char_bytes:
            self.data(b)
            
    def print_string(self,s):
        for c in s:
            self.print_char(c)

    def print_line(self,s):
        s = s[0:10]
        self.print_string(s)
        extra_chars = 10 - len(s)
        for blank in range(extra_chars):
            self.print_char(" ")
        self.data(0)
        self.data(0)
        self.data(0)
        self.data(0)

