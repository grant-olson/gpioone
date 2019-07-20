import smbus

class I2C(object):
    def __init__(self, device_address):
        self.device_address = device_address
        self.smb = smbus.SMBus(1)

    def registers(self):
        {}

    def register(self, register_name):
        return self.registers()[register_name]

    def r(self, register_name):
        return self.register(register_name)

    def write_byte_data(self, register, data):
        self.smb.write_byte_data(self.device_address, self.r(register), data)

    def read_byte_data(self, register):
        return self.smb.read_byte_data(self.device_address, self.r(register))
        
