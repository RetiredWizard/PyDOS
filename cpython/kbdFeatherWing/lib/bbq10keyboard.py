# The MIT License (MIT)
#
# Copyright (c) 2020 arturo182
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`bbq10keyboard`
================================================================================

CircuitPython library for interfaceing the BB Q10 Keyboard over I2C.

* Author(s): arturo182

Implementation Notes
--------------------

**Hardware:**

* `BBQ10 Keyboard PMOD <https://www.tindie.com/products/17986/>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
import time

__version__ = "0.1.0-auto.0"
__repo__ = "https://github.com/arturo182/arturo182_CircuitPython_bbq10keyboard.git"


_ADDRESS_KBD = const(0x1F)

_REG_VER = const(0x01)  # fw version
_REG_CFG = const(0x02)  # config
_REG_INT = const(0x03)  # interrupt status
_REG_KEY = const(0x04)  # key status
_REG_BKL = const(0x05)  # backlight
_REG_DEB = const(0x06)  # debounce cfg
_REG_FRQ = const(0x07)  # poll freq cfg
_REG_RST = const(0x08)  # reset
_REG_FIF = const(0x09)  # fifo

_WRITE_MASK      = const(1 << 7)

CFG_OVERFLOW_ON  = const(1 << 0)
CFG_OVERFLOW_INT = const(1 << 1)
CFG_CAPSLOCK_INT = const(1 << 2)
CFG_NUMLOCK_INT  = const(1 << 3)
CFG_KEY_INT      = const(1 << 4)
CFG_PANIC_INT    = const(1 << 5)

INT_OVERFLOW     = const(1 << 0)
INT_CAPSLOCK     = const(1 << 1)
INT_NUMLOCK      = const(1 << 2)
INT_KEY          = const(1 << 3)
INT_PANIC        = const(1 << 4)

KEY_CAPSLOCK     = const(1 << 5)
KEY_NUMLOCK      = const(1 << 6)
KEY_COUNT_MASK   = const(0x1F)

STATE_IDLE       = const(0)
STATE_PRESS      = const(1)
STATE_LONG_PRESS = const(2)
STATE_RELEASE    = const(3)


class BBQ10Keyboard:
    def __init__(self, i2c):
        self._i2c = I2CDevice(i2c, _ADDRESS_KBD)
        self._buffer = bytearray(2)

        self.reset()

    def reset(self):
        with self._i2c as i2c:
            self._buffer[0] = _REG_RST
            i2c.write(self._buffer, end=1)

        # need to wait!
        time.sleep(0.05)

    @property
    def status(self):
        with self._i2c as i2c:
            self._buffer[0] = _REG_KEY
            i2c.write(self._buffer, end=1)
            i2c.readinto(self._buffer, end=1)

        return self._buffer[0]

    @property
    def key_count(self):
        return self.status & KEY_COUNT_MASK

    @property
    def key(self):
        if self.key_count == 0:
            return None

        with self._i2c as i2c:
            self._buffer[0] = _REG_FIF
            i2c.write(self._buffer, end=1)
            i2c.readinto(self._buffer, end=2)

        return (int(self._buffer[0]), chr(self._buffer[1]))

    @property
    def keys(self):
        keys = []

        for _ in range(self.key_count):
            keys.append(self.key)

        return keys

    @property
    def backlight(self):
        with self._i2c as i2c:
            self._buffer[0] = _REG_BKL
            i2c.write(self._buffer, end=1)
            i2c.readinto(self._buffer, end=1)

        return self._buffer[0] / 255

    @backlight.setter
    def backlight(self, val):
        with self._i2c as i2c:
            self._buffer[0] = _REG_BKL | _WRITE_MASK
            self._buffer[1] = int(255 * val)
            i2c.write(self._buffer, end=2)
