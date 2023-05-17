from machine import SPI, Pin
from src.lps22hh import Lps22hh

cs_pin = Pin(1, Pin.OUT)
spi = SPI(0, baudrate=1000000, firstbit=SPI.MSB, sck=Pin(2), mosi=Pin(3), miso=Pin(0))

sensor = Lps22hh(spi, cs_pin)
sensor.data_rate = 200

while True:
    if sensor.new_pressure_data:
        print(sensor.pressure)