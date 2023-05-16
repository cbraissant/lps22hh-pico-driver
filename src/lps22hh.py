# Author: Chris Braissant
#
# Driver for the ST LPS22HH:
# High-performance MEMS nano pressure sensor:
# 260-1260 hPa absolute digital output barometer

from machine import SPI, Pin
from src.register import Register, Bits

_INTERRUPT_CFG = 0x0B
_THS_P_L = 0x0C
_THS_P_H = 0x0D
_IF_CTRL = 0x0E
_WHO_AM_I = 0x0F
_CTRL_REG1 = 0x10
_CTRL_REG2 = 0x11
_CTRL_REG3 = 0x12
_FIFO_CTRL = 0x13
_FIFO_WTM = 0x14
_REF_P_L = 0x15
_REF_P_H = 0x16
_RPDS_L = 0x18
_RPDS_H = 0x19
_INT_SOURCE = 0x24
_FIFO_STATUS1 = 0x25
_FIFO_STATUS2 = 0x26
_STATUS = 0x27
_PRESS_OUT_XL = 0x28
_PRESS_OUT_L = 0x29
_PRESS_OUT_H = 0x2A
_TEMP_OUT_L = 0x2B
_TEMP_OUT_H = 0x2C
_FIFO_DATA_OUT_PRESS_XL = 0x78
_FIFO_DATA_OUT_PRESS_L = 0x79
_FIFO_DATA_OUT_PRESS_H = 0x7A
_FIFO_DATA_OUT_TEMP_L = 0x7B
_FIFO_DATA_OUT_TEMP_H = 0x7C

_PRESSURE_SENSITIVITY = 4096       # 4096 LSB = 1 hPa
_PRESSURE_RESOLUTION = 0.00024414  # 1 LSB = 1/4096 = 0.0002441406 hPa
_TEMPERATURE_SENSITIVITY = 100     # 100 LSB = °C
_TEMPERATURE_RESOLUTION =  0.01    # 1 LSB = 1/100 = 0.01 °C

_ODR_ONE_SHOT = 0
_ODR_1_HZ = 1
_ODR_10_HZ = 2
_ODR_25_HZ = 3
_ODR_50_HZ = 4
_ODR_75_HZ = 5
_ODR_100_HZ = 6
_ODR_200_HZ = 7


class Lps22hh:

    # REGISTERS
    _interrupt_cfg = Register(_INTERRUPT_CFG, 1)
    _ths_p = Register(_THS_P_L, 2)
    _if_ctrl = Register(_IF_CTRL, 1)
    _who_am_i = Register(_WHO_AM_I, 1)
    _ctrl_reg1 = Register(_CTRL_REG1, 1)
    _ctrl_reg2 = Register(_CTRL_REG2, 1)
    _ctrl_reg3 = Register(_CTRL_REG3, 1)
    _fifo_ctrl = Register(_FIFO_CTRL, 1)
    _fifo_wtm = Register(_FIFO_WTM, 1)
    _ref_p = Register(_REF_P_L, 2)
    _rpds = Register(_RPDS_L, 2)
    _int_source = Register(_INT_SOURCE, 1)
    _fifo_status1 = Register(_FIFO_STATUS1, 1)
    _fifo_status2 = Register(_FIFO_STATUS2, 1)
    _status = Register(_STATUS, 1)
    _press_out = Register(_PRESS_OUT_XL, 3)
    _temp_out = Register(_TEMP_OUT_L, 2)
    _fifo_data_out_press = Register(_FIFO_DATA_OUT_PRESS_XL, 3)
    _fifo_data_out_temp = Register(_FIFO_DATA_OUT_TEMP_L, 2)
    
    # INTERRUPT_CFG
    _autorefp = Bits(_INTERRUPT_CFG, 7, 1)
    _reset_arp = Bits(_INTERRUPT_CFG, 6, 1)
    _autozero = Bits(_INTERRUPT_CFG, 5, 1)
    _reset_az = Bits(_INTERRUPT_CFG, 4, 1)
    _diff_en = Bits(_INTERRUPT_CFG, 3, 1)
    _lir = Bits(_INTERRUPT_CFG, 2, 1)
    _ple = Bits(_INTERRUPT_CFG, 1, 1)
    _phe = Bits(_INTERRUPT_CFG, 0, 1)

    # IF_CTRL
    _int_en_i3c = Bits(_IF_CTRL, 7, 1)
    _sda_pu_en = Bits(_IF_CTRL, 4, 1)
    _sdo_pu_en = Bits(_IF_CTRL, 3, 1)
    _pd_dis_int1 = Bits(_IF_CTRL, 2, 1)
    _i3c_disable = Bits(_IF_CTRL, 1, 1)
    _i2c_disable = Bits(_IF_CTRL, 0, 1)

    # CTRL_REG1
    _odr = Bits(_CTRL_REG1, 4, 3)
    _en_lpfp = Bits(_CTRL_REG1, 3, 1)
    _lpfp_cfg = Bits(_CTRL_REG1, 2, 1)
    _bdu = Bits(_CTRL_REG1, 1, 1)
    _sim = Bits(_CTRL_REG1, 0, 1)

    # CTRL_REG2
    _boot = Bits(_CTRL_REG2, 7, 1)
    _int_h_l = Bits(_CTRL_REG2, 6, 1)
    _pp_od = Bits(_CTRL_REG2, 5, 1)
    _if_add_inc = Bits(_CTRL_REG2, 4, 1)
    _swreset = Bits(_CTRL_REG2, 2, 1)
    _low_noise_en = Bits(_CTRL_REG2, 1, 1)
    _one_shot = Bits(_CTRL_REG2, 0, 1)

    # CTRL_REG3
    _int_f_full = Bits(_CTRL_REG3, 5, 1)
    _int_f_wtm = Bits(_CTRL_REG3, 4, 1)
    _int_f_ovr = Bits(_CTRL_REG3, 3, 1)
    _drdy = Bits(_CTRL_REG3, 2, 1)
    _int_s1 = Bits(_CTRL_REG3, 1, 1)
    _int_s0 = Bits(_CTRL_REG3, 0, 1)

    # FIFO_CTRL
    _stop_on_wtm = Bits(_FIFO_CTRL, 3, 1)
    _trig_modes = Bits(_FIFO_CTRL, 2, 1)
    _f_mode1 = Bits(_FIFO_CTRL, 1, 1)
    _f_mode0 = Bits(_FIFO_CTRL, 0, 1)

    # INT_SOURCE
    _boot_on = Bits(_INT_SOURCE, 7, 1)
    _ia = Bits(_INT_SOURCE, 2, 1)
    _pl = Bits(_INT_SOURCE, 1, 1)
    _ph = Bits(_INT_SOURCE, 0, 1)

    # FIFO_STATUS2
    _fifo_wtm_ia = Bits(_FIFO_STATUS2, 7, 1)
    _fifo_ovr_ia = Bits(_FIFO_STATUS2, 6, 1)
    _fifo_full_ia = Bits(_FIFO_STATUS2, 5, 1)

    # STATUS
    _t_or = Bits(_STATUS, 5, 1)
    _p_or = Bits(_STATUS, 4, 1)
    _t_da = Bits(_STATUS, 1, 1)
    _p_da = Bits(_STATUS, 0, 1)
    

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
        self._swreset = 1
        while self._swreset:
            pass


    def boot(self):
        self._boot = 1
        while self._boot_on:
            pass

    def get_device_id(self):
        return self._who_am_i

    def get_raw_pressure(self):
        return self._press_out

    def get_pressure(self):
        return self.get_raw_pressure() * _PRESSURE_RESOLUTION
    
    def set_reference_pressure(self, data):
        self._ref_p = data

    def get_reference_pressure(self):
        return self._ref_p

    def get_raw_temperature(self):
        return self._temp_out
    
    def get_temperature(self):
        return self.get_raw_temperature() * _TEMPERATURE_RESOLUTION
    
    def set_data_rate(self, data_rate):
        if data_rate == 0:
            odr = _ODR_ONE_SHOT
        elif data_rate <= 1:
            odr = _ODR_1_HZ
        elif data_rate <= 10:
            odr = _ODR_10_HZ
        elif data_rate <= 25:
            odr = _ODR_25_HZ
        elif data_rate <= 50:
            odr = _ODR_50_HZ
        elif data_rate <= 75:
            odr = _ODR_75_HZ
        elif data_rate <= 100:
            odr = _ODR_100_HZ
        else:
            odr = _ODR_200_HZ
        self._odr = odr

    def has_new_measurement(self):
        return self._p_da
    
    def trigger_measurement(self):
        self._one_shot = 1

    def set_fifo_wtm(self, data):
        self._fifo_wtm = data

    def get_fifo_wtm(self):
        return self._fifo_wtm
    
    def set_low_noise_enable(self, data):
        self._low_noise_en = data

    def get_low_noise_enable(self):
        return self._low_noise_en

    def set_low_pass_filter_enable(self, data):
        self._en_lpfp = data

    def get_low_pass_filter_enable(self):
        return self._en_lpfp
  
    def set_low_pass_filter_configuration(self, data):
        self._lpfp_cfg = data

    def get_low_pass_filter_configuration(self):
        return self._lpfp_cfg
    
    def set_block_data_update(self):
        self._bdu = 1

    def get_block_data_update(self):
        return self._bdu


