import time
from machine import I2C, Pin
from lps22hh import LPS22HH

# The RP2040 starts faster than the LPSxxHH pressure sensor and a delay must be introduced
time.sleep_ms(100)

# Create a new I2C device, and assign the pins corresponding to your device
i2c = I2C(1, sda=Pin(6), scl=Pin(7))

# Create a new instance of the Lps22hh sensor
sensor = LPS22HH(interface=i2c, address=0x5D)

# By default, the device is in power-down mode and the ODR need to be changed
# for the device to take continuous measurements
sensor.data_rate = 200

# The Block Data Update (BDU) is used to inhibit the update of the output
# registers until all output registers parts are read, to avoids reading values
# from different sample times
sensor.block_data_update = 1

while True:
    if sensor.new_pressure_data:
        print(sensor.pressure)