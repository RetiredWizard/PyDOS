"""
    Screen/Keyboard abstraction layer

"""
from supervisor import runtime
from sys import stdin
import displayio
import board
import busio
import fourwire
import adafruit_ili9341

class PyDOS_UI:

    def __init__(self):
        displayio.release_displays()
        self.scrollable = True

        spi = busio.SPI(board.IO14,board.IO13,board.IO12)
        bus = fourwire.FourWire(spi,command=board.IO2,chip_select=board.IO15)
        self.display = adafruit_ili9341.ILI9341(bus,width=320,height=240,backlight_pin=board.IO21)

    def serial_bytes_available(self):
        # Does the same function as supervisor.runtime.serial_bytes_available
        retval = runtime.serial_bytes_available

        return retval

    def read_keyboard(self,num):
        # Does the same function as sys.stdin.read(num), blocking read
        return stdin.read(num)

    def get_screensize(self):
        return(19,53)

Pydos_ui = PyDOS_UI()

