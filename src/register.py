# Author: Chris Braissant
#
# Register library for:
# Driver for the ST LPS22HH:
# High-performance MEMS nano pressure sensor:
# 260-1260 hPa absolute digital output barometer
from machine import SPI, Pin

class Bits:
    def __init__(self, register_address, start_position:int, length:int):
        self.register_address = register_address
        self.start_position = start_position
        self.length = length
        self.mask = ((1 << self.length) - 1) << self.start_position

    def __get__(self, obj, objtype=None):
        reg = Register(self.register_address, 1)
        data = reg.__get__(obj)
        data &= self.mask
        data >>= self.start_position
        return data 

    def __set__(self, obj, value):
        reg = Register(self.register_address, 1)
        data = reg.__get__(obj)
        # clear the bits to write
        data &= ~self.mask 
        # write the new value
        data |= (value << self.start_position)
        reg.__set__(obj, data)



class Register:
    def __init__(self, register_address:int, length:int):
        self.register_address = register_address
        self.length = length
    
    def start_transaction(self, obj, objtype=None):
        obj.cs_pin.value(0)
    
    def end_transaction(self, obj, objtype=None):
        obj.cs_pin.value(1)

    def convert_bytes_to_int(self, bytes):
        return int.from_bytes(bytes, 'little')
    
    def convert_int_to_bytes(self, data):
        return data.to_bytes(self.length, 'little')
            
    def __get__(self, obj, objtype=None):
        msg = bytearray()
        msg.append(0x80 | self.register_address)
        self.start_transaction(obj)
        obj.spi.write(msg)
        data = obj.spi.read(self.length)
        self.end_transaction(obj)
        return self.convert_bytes_to_int(data)

    def __set__(self, obj, data):
        data_bytes = self.convert_int_to_bytes(data)
        msg = bytearray()
        msg.append(self.register_address)
        msg.extend(data_bytes)
        self.start_transaction(obj)
        obj.spi.write(msg)
        self.end_transaction(obj)