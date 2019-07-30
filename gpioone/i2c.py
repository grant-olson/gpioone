import smbus
import numbers

class I2C(object):
    def __init__(self, device_address):
        self.device_address = device_address
        self.smb = smbus.SMBus(1)

    def registers(self):
        {}

    def register(self, register_name):
        if isinstance(register_name, numbers.Number):
            return register_name
        else:
            return self.registers()[register_name]

    def r(self, register_name):
        return self.register(register_name)

    def write_byte_data(self, register, data):
        self.smb.write_byte_data(self.device_address, self.r(register), data)

    def read_byte_data(self, register):
        return self.smb.read_byte_data(self.device_address, self.r(register))
        
    def write_block_data(self, register, *data):
        self.smb.write_block_data(self.device_address, self.r(register), list(data))

#    def read_block_data(self, register):
#        return self.smb.read_block_data(self.device_address, self.r(register))
        
