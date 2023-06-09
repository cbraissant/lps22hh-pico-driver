from machine import SPI, Pin
from lps22hh import LPS22HH

# Create a new SPI device, and assign the pins corresponding to your device
cs_pin = Pin(1, Pin.OUT)
spi = SPI(0, baudrate=1000000, firstbit=SPI.MSB, sck=Pin(2), mosi=Pin(3), miso=Pin(0))

# Create a new instance of the Lps22hh sensor
sensor = LPS22HH(spi, cs_pin)

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