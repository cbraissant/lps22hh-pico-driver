from machine import SPI, Pin
from src.lps22hh import Lps22hh

cs_pin = Pin(1, Pin.OUT)
spi = SPI(0, baudrate=1000000, firstbit=SPI.MSB, sck=Pin(2), mosi=Pin(3), miso=Pin(0))

sensor = Lps22hh(spi, cs_pin)
sensor.set_data_rate(1)

while True:
    if sensor.has_new_measurement():
        print(sensor.get_pressure())