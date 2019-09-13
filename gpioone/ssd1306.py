from .i2c import *
import unscii

class SSD1306(I2C):
    def __init__(self,device_address=0x3c,font='unscii_8_thin_transposed',row_size=32):
        super(SSD1306,self).__init__(device_address)

        self.unscii = unscii.unscii(font)
        # Sample initialization from Section 3 of the Application Note Appendix in datasheet.

        self.row_size = row_size
        self.pages = row_size // 8
        
        self.send_command("SET_MUX_RATIO", 0x3f)
        self.send_command("SET_DISPLAY_OFFSET", 0x00)
        self.send_command("SET_DISPLAY_START_LINE")
        self.send_command("SET_SEGMENT_REMAP_0")
        self.send_command("SET_COM_OUTPUT_SCAN_DIRECTION_INCREMENT")
        if self.row_size == 32:
            self.send_command("SET_COM_PINS", 0x02)
        elif self.row_size == 64:
            self.send_command("SET_COM_PINS", 0x02 + 16)
        else:
            raise RuntimeError("Bad Size")
        
        self.send_command("SET_CONTRAST", 0x7F)
        self.send_command("ENTIRE_DISPLAY_ON")
        self.send_command("NORMAL_DISPLAY")
        self.send_command("ENABLE_CHARGE_PUMP_REGULATOR", 0x14)
        self.send_command("DISPLAY_ON")
        self.send_command("SET_MEMORY_ADDRESSING_MODE", 0x02) # Page addressing mode
        
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
            "LEFT_HORIZONTAL_SCROLL": 0x27,
            "VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL": 0x29,
            "VERTICAL_AND_LEFT_HORIZONTAL_SCROLL": 0x2A,
            
            "SET_MUX_RATIO": 0xA8,
            "SET_DISPLAY_OFFSET": 0xD3,
            "SET_DISPLAY_START_LINE": 0x40,
            "SET_SEGMENT_REMAP_0": 0xA0,
            "SET_SEGMENT_REMAP_127": 0xA1,
            "SET_COM_OUTPUT_SCAN_DIRECTION_INCREMENT": 0xC0,
            "SET_COM_OUTPUT_SCAN_DIRECTION_DECREMENT": 0xC8,
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
            "LOW_NIBBLE_1": 0x1,
            "LOW_NIBBLE_2": 0x2,
            "LOW_NIBBLE_3": 0x3,
            "LOW_NIBBLE_4": 0x4,
            "LOW_NIBBLE_5": 0x5,
            "LOW_NIBBLE_6": 0x6,
            "LOW_NIBBLE_7": 0x7,
            "LOW_NIBBLE_8": 0x8,
            "LOW_NIBBLE_9": 0x9,
            "LOW_NIBBLE_A": 0xA,
            "LOW_NIBBLE_B": 0xB,
            "LOW_NIBBLE_C": 0xC,
            "LOW_NIBBLE_D": 0xD,
            "LOW_NIBBLE_E": 0xE,
            "LOW_NIBBLE_F": 0xF,
            "HIGH_NIBBLE_0": 0x10,
            "HIGH_NIBBLE_1": 0x11,
            "HIGH_NIBBLE_2": 0x12,
            "HIGH_NIBBLE_3": 0x13,
            "HIGH_NIBBLE_4": 0x14,
            "HIGH_NIBBLE_5": 0x15,
            "HIGH_NIBBLE_6": 0x16,
            "HIGH_NIBBLE_7": 0x17,
            "HIGH_NIBBLE_8": 0x18,
            "HIGH_NIBBLE_9": 0x19,
            "HIGH_NIBBLE_A": 0x1A,
            "HIGH_NIBBLE_B": 0x1B,
            "HIGH_NIBBLE_C": 0x1C,
            "HIGH_NIBBLE_D": 0x1D,
            "HIGH_NIBBLE_E": 0x1E,
            "HIGH_NIBBLE_F": 0x1F,

            "ACTIVATE_SCROLL": 0x2F,
            "DEACTIVATE_SCROLL": 0x2E
            }[command]
    
    def send_command(self, command_name, *command_args):
        self.write_byte_data("COMMAND", self.commands(command_name))
        for arg in command_args:
            self.write_byte_data("COMMAND", arg)

    def send_data(self, data):
        self.write_byte_data("DATA", data)

    def print_char(self, char, half=None, exception_on_unknown=False):
        char_bytes = self.unscii.get_char(char)

        if len(char_bytes) > 8:
            if half == "TOP":
                char_bytes = char_bytes[:8]
            elif half == "BOTTOM":
                char_bytes = char_bytes[8:]
            else:
                raise RuntimeError("Need a half of TOP or BOTTOM for double-height characters")
            
        for byte in char_bytes:
            self.send_data(byte)


    def print_string(self, string, row=0, column=0, exception_on_unknown=False):
        self.set_row_and_column(row,column*8)
        for char in string:
            self.print_char(char,half="TOP",exception_on_unknown=exception_on_unknown)
        if self.unscii.size() == 2:
            self.set_row_and_column(row+1,column*8)
            for char in string:
                self.print_char(char,half="BOTTOM",exception_on_unknown=exception_on_unknown)

    def print_line(self, string, row=0, column=0, line_size=16):
        while (len(string) + column) < line_size:
            string += " "
        self.print_string(string,row=row,column=column)

    def print_bytes(self, byte_list):
        for byte in byte_list:
            self.send_data(byte)
            
    def clear_screen(self,blank_while_clearing=True):
        if blank_while_clearing:
            self.send_command("ENTIRE_DISPLAY_ON")
        for i in range(0,self.pages):
            self.send_command("PAGE_%d" % i)
            self.send_command("LOW_NIBBLE_0")
            self.send_command("HIGH_NIBBLE_0")

            for i in range(128):
                self.send_data(0x0)
                
        self.send_command("OUTPUT_RAM")

    def set_contrast(self, contrast):
        self.send_command("SET_CONTRAST", contrast)

    def set_row(self, row):
        self.send_command("PAGE_%d" % row)

    def set_column(self, column):
        hex = "%02X" % column
        self.send_command("LOW_NIBBLE_%s" % hex[1])
        self.send_command("HIGH_NIBBLE_%s" % hex[0])

    def set_row_and_column(self, row, column):
        self.set_row(row)
        self.set_column(column)
        
    def activate_scroll(self):
        self.send_command("ACTIVATE_SCROLL")

    def deactivate_scroll(self):
        self.send_command("DEACTIVATE_SCROLL")

    def set_font(self, font_name):
        self.unscii = unscii.unscii(font_name)
