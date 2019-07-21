from i2c import I2C

class PCA9685(I2C):
    def __init__(self,device_address=0x70):
        super(PCA9685,self).__init__(device_address)

    def registers(self):
        return {
            "MODE1": 0x00,
            "MODE2": 0x01,
            "SUBADR1": 0x02,
            "SUBADR2": 0x03,
            "SUBADR3": 0x04,
            "ALLCALLADR": 0x05,
            "LED0_ON_L": 0x06,
            "LED0_ON_H": 0x07,
            "LED0_OFF_L": 0x08,
            "LED0_OFF_H": 0x09,
            "LED1_ON_L": 0x0A,
            "LED1_ON_H": 0x0B,
            "LED1_OFF_L": 0x0C,
            "LED1_OFF_H": 0x0D,
            "LED2_ON_L": 0x0E,
            "LED2_ON_H": 0x0F,
            "LED2_OFF_L": 0x10,
            "LED2_OFF_H": 0x11,
            "LED3_ON_L": 0x12,
            "LED3_ON_H": 0x13,
            "LED3_OFF_L": 0x14,
            "LED3_OFF_H": 0x15,
            "LED4_ON_L": 0x16,
            "LED4_ON_H": 0177,
            "LED4_OFF_L": 0x18,
            "LED4_OFF_H": 0x19,
            "LED5_ON_L": 0x1A,
            "LED5_ON_H": 0x1B,
            "LED5_OFF_L": 0x1C,
            "LED5_OFF_H": 0x1D,
            "LED6_ON_L": 0x1E,
            "LED6_ON_H": 0x1F,
            "LED6_OFF_L": 0x20,
            "LED6_OFF_H": 0x21,
            "LED7_ON_L": 0x22,
            "LED7_ON_H": 0x23,
            "LED7_OFF_L": 0x24,
            "LED7_OFF_H": 0x25,
            "LED8_ON_L": 0x26,
            "LED8_ON_H": 0x27,
            "LED8_OFF_L": 0x28,
            "LED8_OFF_H": 0x29,
            "LED9_ON_L": 0x2A,
            "LED9_ON_H": 0x2B,
            "LED9_OFF_L": 0x2C,
            "LED9_OFF_H": 0x2D,
            "LED10_ON_L": 0x2E,
            "LED10_ON_H": 0x2F,
            "LED10_OFF_L": 0x30,
            "LED10_OFF_H": 0x31,
            "LED11_ON_L": 0x32,
            "LED11_ON_H": 0x33,
            "LED11_OFF_L": 0x34,
            "LED11_OFF_H": 0x35,
            "LED12_ON_L": 0x36,
            "LED12_ON_H": 0x37,
            "LED12_OFF_L": 0x38,
            "LED12_OFF_H": 0x39,
            "LED13_ON_L": 0x3A,
            "LED13_ON_H": 0x3B,
            "LED13_OFF_L": 0x3C,
            "LED13_OFF_H": 0x3D,
            "LED14_ON_L": 0x3E,
            "LED14_ON_H": 0x3F,
            "LED14_OFF_L": 0x40,
            "LED14_OFF_H": 0x41,
            "LED15_ON_L": 0x42,
            "LED15_ON_H": 0x43,
            "LED15_OFF_L": 0x44,
            "LED15_OFF_H": 0x45,

            "ALL_LED_ON_L": 0xFA,
            "ALL_LED_ON_H": 0xFB,
            "ALL_LED_OFF_L": 0xFC,
            "ALL_LED_OFF_H": 0xFD,

            "PRE_SCALE": 0xFE,
            "TestMode": 0xFF
            
            }

    def set_frequency(self, frequency):
        new_freq = 25000000 / (4096 * frequency) - 1
        self.write_byte_data("MODE1",0x11) # do better
        self.write_byte_data("PRE_SCALE", new_freq)
        self.write_byte_data("MODE1",0x01)
        
    def servo_mode(self,start_ms=1,end_ms=2):
        """
        Assume we want to use this to drive servos.
        """
        self.set_frequency(50)
        self.start_ms = start_ms
        self.end_ms = end_ms

    def set_servo(self, servo_no, degrees):
        percent_degrees = float(degrees) / 180.0
        total_ms = ((self.end_ms - self.start_ms) * percent_degrees) + self.start_ms
        duty_cycle = float(total_ms) / 20.0
        scaled_setting = int(duty_cycle * 4096)

        # Start immediately
        self.write_byte_data("LED%d_ON_H" % servo_no, 0x0)
        self.write_byte_data("LED%d_ON_L" % servo_no, 0x0)
        # Stop after X ms
        self.write_byte_data("LED%d_OFF_H" % servo_no, scaled_setting >> 8)
        self.write_byte_data("LED%d_OFF_L" % servo_no, scaled_setting & 0xFF)
        
