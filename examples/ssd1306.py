from gpioone import *
from unscii_transposed_bytes import *

class SSD1306(I2C):
    def __init__(self,device_address=0x3c):
        super(SSD1306,self).__init__(device_address)
        self.send_command("SET_MUX_RATIO", 0x3f)
        self.send_command("SET_DISPLAY_OFFSET", 0x00)
        self.send_command("SET_DISPLAY_START_LINE")
        self.send_command("SET_SEGMENT_REMAP")
        self.send_command("SET_COM_OUTPUT_SCAN_DIRECTION")
        self.send_command("SET_COM_PINS", 0x02)
        self.send_command("SET_CONTRAST", 0x7F)
        self.send_command("ENTIRE_DISPLAY_ON")
        self.send_command("NORMAL_DISPLAY")
        self.send_command("ENABLE_CHARGE_PUMP_REGULATOR", 0x14)
        self.send_command("DISPLAY_ON")

    def registers(self):
        return {
            "COMMAND": 0x00,
            "DATA": 0x40
        }
    
    def __del__(self):
        self.send_command("DISPLAY_OFF")

    def commands(self, command):
        return {
            "RIGHT_HORIZONTAL_SCROLL": 0x26,
            
            "SET_MUX_RATIO": 0xA8,
            "SET_DISPLAY_OFFSET": 0xD3,
            "SET_DISPLAY_START_LINE": 0x40,
            "SET_SEGMENT_REMAP": 0xA0, # or A1?
            "SET_COM_OUTPUT_SCAN_DIRECTION": 0xC0, # or C8?
            "SET_COM_PINS": 0xDA,
            "SET_OSC_FREQUENCY": 0xD5,
            "ENABLE_CHARGE_PUMP_REGULATOR": 0x8D,

            "SET_MEMORY_ADDRESSING_MODE": 0x20,
            
            "DISPLAY_ON": 0xAF,
            "DISPLAY_OFF": 0xAE,
            
            "SET_CONTRAST": 0x81,
            "ENTIRE_DISPLAY_ON": 0xA5,
            "OUTPUT_RAM": 0xA4,
            
            "NORMAL_DISPLAY": 0xA6,
            "INVERSE_DISPLAY": 0xA7,

            "PAGE_0": 0xB0,
            "PAGE_1": 0xB1,
            "PAGE_2": 0xB2,
            "PAGE_3": 0xB3,
            "PAGE_4": 0xB4,
            "PAGE_5": 0xB5,
            "PAGE_6": 0xB6,
            "PAGE_7": 0xB7,
            
            "SET_COLUMN_ADDRESS": 0x21,

            "LOW_NIBBLE_0": 0x0,
            "HIGH_NIBBLE_0": 0x10,

            "ACTIVATE_SCROLL": 0x2F,
            "DEACTIVATE_SCROLL": 0x2E
            }[command]
    
    def send_command(self, command_name, *command_args):
        self.write_byte_data("COMMAND", self.commands(command_name))
        for arg in command_args:
            self.write_byte_data("COMMAND", arg)

    def send_data(self, data):
        self.write_byte_data("DATA", data)

import random

def a():
    a_hex = [0x18, 0x3C, 0x66, 0x66, 0x7E, 0x66, 0x66, 0x00]
    transposed_bits = [0,0,0,0,0,0,0,0]
    for i in range(8):
        hex_line = a_hex[i]
        for j in range(8):
            bit = hex_line & (1 << j)
            if bit:
                transposed_bits[j] += 1 << i
    print(repr(transposed_bits))
    x = 0
    while True:
        print(repr(x))
        yield transposed_bits[x]
        x += 1
        if x >= 8:
            x = 0

def s():
    digits =[1, 3, 6, 124, 124, 6, 3, 1]
    x = 0
    while True:
        yield digits[x]
        x += 1
        if x >= 8:
            x = 0

def deadbeef():
    word = "DeadBeef"
    x = 0
    while True:
        letter = word[x]
        print(letter)
        bytes = unscii_transposed_bytes[ord(letter)]
        for byte in bytes:
            yield byte
        x += 1
        if x >= 8:
            x = 0
if __name__ == "__main__":
    ssd = SSD1306()

    ssd.send_command("OUTPUT_RAM")
    ssd.send_command("SET_CONTRAST", 128)

    a_generator = deadbeef()
    
    ssd.send_command("SET_MEMORY_ADDRESSING_MODE", 0x02) # Page addressing mode
    for i in range(0,4):
        print("PAGE %d" % i)
        ssd.send_command("PAGE_%d" % i)
        ssd.send_command("LOW_NIBBLE_0")
        ssd.send_command("HIGH_NIBBLE_0")
        
        for i in range(128):
            data = 0
            
            ssd.send_data(data)

    sleep(1)
    ssd.send_command("SET_COLUMN_ADDRESS", 0x0, 0xFF)

    for i in range(0,4):
        print("PAGE %d" % i)
        ssd.send_command("PAGE_%d" % i)
        ssd.send_command("LOW_NIBBLE_0")
        ssd.send_command("HIGH_NIBBLE_0")

        
        for i in range(128):
            data = a_generator.next()
            
            ssd.send_data(data)
            sleep(0.01)
    
#    sleep(5)
    print "SCROLL RIGHT"
    ssd.send_command("RIGHT_HORIZONTAL_SCROLL", 0x0, 0x0, 0x0, 0x7, 0x0, 0xff)
    ssd.send_command("ACTIVATE_SCROLL")
    sleep(5)
    ssd.send_command("DEACTIVATE_SCROLL")
    print "GOODBYE"
