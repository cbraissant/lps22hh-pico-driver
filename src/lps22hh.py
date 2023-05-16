# Author: Chris Braissant
#
# Driver for the ST LPS22HH:
# High-performance MEMS nano pressure sensor:
# 260-1260 hPa absolute digital output barometer

from machine import SPI, Pin
from src.register import Register, RegisterBits

class LPS22HH_address():
    LPS22HH_INTERRUPT_CFG = 0x0B
    LPS22HH_THS_P_L = 0x0C
    LPS22HH_THS_P_H = 0x0D
    LPS22HH_IF_CTRL = 0x0E
    LPS22HH_WHO_AM_I = 0x0F
    LPS22HH_CTRL_REG1 = 0x10
    LPS22HH_CTRL_REG2 = 0x11
    LPS22HH_CTRL_REG3 = 0x12
    LPS22HH_FIFO_CTRL = 0x13
    LPS22HH_FIFO_WTM = 0x14
    LPS22HH_REF_P_L = 0x15
    LPS22HH_REF_P_H = 0x16
    LPS22HH_RPDS_L = 0x18
    LPS22HH_RPDS_H = 0x19
    LPS22HH_INT_SOURCE = 0x24
    LPS22HH_FIFO_STATUS1 = 0x25
    LPS22HH_FIFO_STATUS2 = 0x26
    LPS22HH_STATUS = 0x27
    LPS22HH_PRESSURE_OUT_XL = 0x28
    LPS22HH_PRESSURE_OUT_L = 0x29
    LPS22HH_PRESSURE_OUT_H = 0x2A
    LPS22HH_TEMP_OUT_L = 0x2B
    LPS22HH_TEMP_OUT_H = 0x2C
    LPS22HH_FIFO_DATA_OUT_PRESS_XL = 0x78
    LPS22HH_FIFO_DATA_OUT_PRESS_L = 0x79
    LPS22HH_FIFO_DATA_OUT_PRESS_H = 0x7A
    LPS22HH_FIFO_DATA_OUT_TEMP_L = 0x7B
    LPS22HH_FIFO_DATA_OUT_TEMP_H = 0x7C

    LPS22HH_PRESSURE_SENSITIVITY = 4096       # 4096 LSB = 1 hPa
    LPS22HH_PRESSURE_RESOLUTION = 0.00024414  # 1 LSB = 1/4096 = 0.0002441406 hPa
    LPS22HH_TEMPERATURE_SENSITIVITY = 100     # 100 LSB = °C
    LPS22HH_TEMPERATURE_RESOLUTION =  0.01    # 1 LSB = 1/100 = 0.01 °C

    LPS22HH_ODR_ONE_SHOT = 0
    LPS22HH_ODR_1_HZ = 1
    LPS22HH_ODR_10_HZ = 2
    LPS22HH_ODR_25_HZ = 3
    LPS22HH_ODR_50_HZ = 4
    LPS22HH_ODR_75_HZ = 5
    LPS22HH_ODR_100_HZ = 6
    LPS22HH_ODR_200_HZ = 7


class Lps22hh:
    def __init__(self, spi:SPI, cs_pin:Pin):
        self.spi = spi
        self.cs_pin = cs_pin


    def set_spi(self, spi:SPI):
        self.spi = spi

    def get_spi(self):
        return self.spi


    def set_cs_pin(self, cs_pin:Pin):
        self.cs_pin = cs_pin
        self.cs_pin.value(0)

    def get_cs_pin(self):
        return self.cs_pin


    def reset(self):
        # Software reset procedure.
        # The following registers are reset to their default value:
        # INTERRUPT_CFG, THS_P_L, THS_P_H, IF_CTRL, CTRL_REG1, CTRL_REG2, CTRL_REG3
        # FIFO_CTRL, FIFO_WTM, INT_SOURCE, FIFO_STATUS1, FIFO_STATUS2, STATUS
        reg = RegisterBits(LPS22HH_address.LPS22HH_CTRL_REG2, 2, 1, self.spi, self.cs_pin)
        reg.write(1)
        while reg.read() == 1:
            pass


    def boot(self):
        reg_boot = RegisterBits(LPS22HH_address.LPS22HH_CTRL_REG2, 7, 1, self.spi, self.cs_pin)
        reg_boot_on = RegisterBits(LPS22HH_address.LPS22HH_INT_SOURCE, 7, 1, self.spi, self.cs_pin)
        reg_boot.write(1)
        while reg_boot_on.read() == 1:
            pass


    def status(self):
        reg = Register(LPS22HH_address.LPS22HH_STATUS, 1, self.spi, self.cs_pin)
        return reg.read()

    def device_id(self):
        reg = Register(LPS22HH_address.LPS22HH_WHO_AM_I, 1, self.spi, self.cs_pin)
        return reg.read()

    def get_raw_pressure(self):
        reg = Register(LPS22HH_address.LPS22HH_PRESSURE_OUT_XL, 3, self.spi, self.cs_pin)
        return reg.read()

    def get_pressure(self):
        return self.get_raw_pressure() * LPS22HH_address.LPS22HH_PRESSURE_RESOLUTION
    
    def set_reference_pressure(self, data):
        reg = Register(LPS22HH_address.LPS22HH_RPDS_L, 2, self.spi, self.cs_pin)
        reg.write(data)

    def get_reference_pressure(self):
        reg = Register(LPS22HH_address.LPS22HH_RPDS_L, 2, self.spi, self.cs_pin)
        return reg.read()

    def get_raw_temperature(self):
        reg = Register(LPS22HH_address.LPS22HH_TEMP_OUT_L, 2, self.spi, self.cs_pin)
        return reg.read()
    
    def get_temperature(self):
        return self.get_raw_temperature() * LPS22HH_address.LPS22HH_TEMPERATURE_RESOLUTION
    
    def set_data_rate(self, data_rate):
        reg_bits = RegisterBits(LPS22HH_address.LPS22HH_CTRL_REG1, 4, 3, self.spi, self.cs_pin)
        if data_rate == 0:
            odr = LPS22HH_address.LPS22HH_ODR_ONE_SHOT
        elif data_rate <= 1:
            odr = LPS22HH_address.LPS22HH_ODR_1_HZ
        elif data_rate <= 10:
            odr = LPS22HH_address.LPS22HH_ODR_10_HZ
        elif data_rate <= 25:
            odr = LPS22HH_address.LPS22HH_ODR_25_HZ
        elif data_rate <= 50:
            odr = LPS22HH_address.LPS22HH_ODR_50_HZ
        elif data_rate <= 75:
            odr = LPS22HH_address.LPS22HH_ODR_75_HZ
        elif data_rate <= 100:
            odr = LPS22HH_address.LPS22HH_ODR_100_HZ
        else:
            odr = LPS22HH_address.LPS22HH_ODR_200_HZ
        reg_bits.write(odr)

    def has_new_measurement(self):
        reg_bit = RegisterBits(LPS22HH_address.LPS22HH_STATUS, 0, 1, self.spi, self.cs_pin)
        return reg_bit.read()
    
    def trigger_measurement(self):
        reg_bit = RegisterBits(LPS22HH_address.LPS22HH_CTRL_REG2, 0, 1, self.spi, self.cs_pin)
        reg_bit.write(1)

    def set_fifo_wtm(self, data):
        reg = Register(LPS22HH_address.LPS22HH_FIFO_WTM, 1, self.spi, self.cs_pin)
        reg.write(data)

    def get_fifo_wtm(self):
        reg = Register(LPS22HH_address.LPS22HH_FIFO_WTM, 1, self.spi, self.cs_pin)
        return reg.read()
    
    def set_low_noise_enable(self, data):
        reg_bit = RegisterBits(LPS22HH_address.LPS22HH_CTRL_REG2, 1, 1, self.spi, self.cs_pin)
        reg_bit.write(data)

    def get_low_noise_enable(self):
        reg_bit = RegisterBits(LPS22HH_address.LPS22HH_CTRL_REG2, 1, 1, self.spi, self.cs_pin)
        return reg_bit.read

    def set_low_pass_filter_enable(self, data):
        reg_bit = RegisterBits(LPS22HH_address.LPS22HH_CTRL_REG1, 3, 1, self.spi, self.cs_pin)
        reg_bit.write(data)

    def get_low_pass_filter_enable(self):
        reg_bit = RegisterBits(LPS22HH_address.LPS22HH_CTRL_REG1, 3, 1, self.spi, self.cs_pin)
        return reg_bit.read
        