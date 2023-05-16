# Author: Chris Braissant
#
# Register library for:
# Driver for the ST LPS22HH:
# High-performance MEMS nano pressure sensor:
# 260-1260 hPa absolute digital output barometer
from machine import SPI, Pin

class RegisterBits:
    def __init__(self, register_address, start_position:int, length:int, spi:SPI, cs_pin:Pin):
        self.register_address = register_address
        self.start_position = start_position
        self.length = length
        self.spi = spi
        self.cs_pin = cs_pin

    def read(self):
        reg = Register(self.register_address, 1, self.spi, self.cs_pin)
        data = reg.read()
        mask = ((1 << self.length) - 1) << self.start_position
        data &= mask
        data >>= self.start_position
        return data 

    def write(self, value):
        reg = Register(self.register_address, 1, self.spi, self.cs_pin)
        data = reg.read()
        mask = ((1 << self.length) - 1) << self.start_position
        # clear the bits to write
        data &= ~mask 
        # write the new value
        data |= (value << self.start_position)
        reg.write(data)



class Register:
    def __init__(self, register_address, length:int, spi:SPI, cs_pin:Pin):
        self.register_address = register_address
        self.length = length
        self.spi = spi
        self.cs_pin = cs_pin
    
    def start_transaction(self):
        self.cs_pin.value(0)
    
    def end_transaction(self):
        self.cs_pin.value(1)

    def convert_bytes_to_int(self, bytes):
        return int.from_bytes(bytes, 'little')
    
    def convert_int_to_bytes(self, data):
        return data.to_bytes(self.length, 'little')
            
    def read(self):
        msg = bytearray()
        msg.append(0x80 | self.register_address)
        self.start_transaction()
        self.spi.write(msg)
        data = self.spi.read(self.length)
        self.end_transaction()
        return self.convert_bytes_to_int(data)

    def write(self, data):
        data_bytes = self.convert_int_to_bytes(data)
        msg = bytearray()
        msg.append(self.register_address)
        msg.extend(data_bytes)
        self.start_transaction()
        self.spi.write(msg)
        self.end_transaction()
