from machine import SPI, Pin
from time import sleep
from tests.unittest import Test, bcolors
from src.lps22hh import Lps22hh
from src.lps22hh import LPS22HH_address as LPS22
from src.register import Register, RegisterBits

def test_basic():
    print(f'{bcolors.BOLD}{bcolors.BRIGHT_BLUE}-- Basic testing --{bcolors.DEFAULT}')
    Test('Test sanity').assert_equal(1,1)

def test_register(spi, cs_pin):
    print(f'{bcolors.BOLD}{bcolors.BRIGHT_BLUE}-- Register testing --{bcolors.DEFAULT}')

    reg = Register(LPS22.LPS22HH_WHO_AM_I, 1, spi, cs_pin)
    Test('Read single register').assert_equal(reg.read(), 0xB3)

    reg = Register(LPS22.LPS22HH_CTRL_REG1, 3, spi, cs_pin)
    Test('Read multiple register').assert_equal(reg.read(), 0x1000)

    reg = Register(LPS22.LPS22HH_RPDS_L, 1, spi, cs_pin)
    reg.write(0xAB)
    Test('Write single register').assert_equal(reg.read(), 0xAB)

    #clean up
    reg.write(0x00)
    Test('Clean up').assert_equal(reg.read(), 0x00)

    reg = Register(LPS22.LPS22HH_RPDS_L, 2, spi, cs_pin)
    reg.write(0xABCD)
    Test('Write multiple register').assert_equal(reg.read(), 0xABCD)

    #clean up
    reg.write(0x0000)
    Test('Clean up').assert_equal(reg.read(), 0x00)



def test_register_bits(spi, cs_pin):
    print(f'{bcolors.BOLD}{bcolors.BRIGHT_BLUE}-- Register Bits testing --{bcolors.DEFAULT}')

    reg = RegisterBits(LPS22.LPS22HH_WHO_AM_I, 2, 1, spi, cs_pin)
    Test('Read single bit (low)').assert_equal(reg.read(), 0)

    reg = RegisterBits(LPS22.LPS22HH_WHO_AM_I, 4, 1, spi, cs_pin)
    Test('Read single bit (high)').assert_equal(reg.read(), 1)

    reg = RegisterBits(LPS22.LPS22HH_WHO_AM_I, 0, 8, spi, cs_pin)
    Test('Read multiple bits').assert_equal(reg.read(), 179)
    
    reg = RegisterBits(LPS22.LPS22HH_RPDS_L, 0, 1, spi, cs_pin)
    reg.write(1)
    Test('Write single bit (high)').assert_equal(reg.read(), 1)
    reg.write(0)
    Test('Write single bit (low)').assert_equal(reg.read(), 0)

    reg = Register(LPS22.LPS22HH_RPDS_L, 1, spi, cs_pin)
    Test('Write multiple bits (position)').assert_equal(reg.read(), 0)

    reg = RegisterBits(LPS22.LPS22HH_RPDS_L, 2, 4, spi, cs_pin)
    reg.write(0b1101)
    Test('Write multiple bits (data)').assert_equal(reg.read(), 0b1101)
    reg = Register(LPS22.LPS22HH_RPDS_L, 1, spi, cs_pin)
    Test('Write multiple bits (position)').assert_equal(reg.read(), 0b0110100)


def test_functionnality(spi, cs_pin):
    print(f'{bcolors.BOLD}{bcolors.BRIGHT_BLUE}-- Functionnalities --{bcolors.DEFAULT}')
   
    sensor = Lps22hh(spi, cs_pin)

    # Device Id
    Test('Read single register').assert_equal(sensor.device_id(), 0xB3)
 

    # SPI
    Test('Get SPI').assert_equal(sensor.get_spi(), spi)
    new_spi = SPI(1, baudrate=1000000, firstbit=SPI.MSB, sck=Pin(10), mosi=Pin(11), miso=Pin(8))
    sensor.set_spi(new_spi)
    Test('Set SPI - not old one').assert_not_equal(sensor.get_spi(), spi)
    Test('Set SPI - new one').assert_equal(sensor.get_spi(), new_spi)


    # CS Pin
    Test('Get CS Pin').assert_equal(sensor.get_cs_pin(), cs_pin)
    new_cs_pin = Pin(9, Pin.OUT)
    sensor.set_cs_pin(new_cs_pin)
    Test('Set CS Pin - not old one').assert_not_equal(sensor.get_cs_pin(), cs_pin)
    Test('Set CS Pin - new one').assert_equal(sensor.get_cs_pin(), new_cs_pin)


    # Clean up
    sensor.set_spi(spi)
    sensor.set_cs_pin(cs_pin)


    # FIFO
    sensor.set_fifo_wtm(0xAB)
    reg = Register(LPS22.LPS22HH_FIFO_WTM, 1, spi, cs_pin)
    Test('Set FIFO watermark').assert_equal(reg.read(), 0xAB)
    Test('Read FIFO watermark').assert_equal(sensor.get_fifo_wtm(), 0XAB)


    # Reset
    # The reset procedure clears multiple regiters,
    # but only the fifo wtm is tested
    sensor.set_fifo_wtm(0XAB)
    sensor.reset()
    Test('Reset - fifo wtm').assert_equal(sensor.get_fifo_wtm(), 0X00)

    # New measurement
    Test('No new measurement').assert_equal(sensor.has_new_measurement(), 0x00)
    sensor.trigger_measurement()
    sleep(1)
    Test('Has new measurement').assert_equal(sensor.has_new_measurement(), 0x01)


if __name__ == "__main__":
    cs_pin = Pin(1, Pin.OUT)
    spi = SPI(0, baudrate=1000000, firstbit=SPI.MSB, sck=Pin(2), mosi=Pin(3), miso=Pin(0))

    print(f'{bcolors.BOLD}{bcolors.BRIGHT_MAGENTA}Testing starts...{bcolors.DEFAULT}')

    test_basic()
    test_register(spi, cs_pin)
    test_register_bits(spi, cs_pin)
    test_functionnality(spi, cs_pin)

