# The MIT License (MIT)
#
# Copyright (c) 2021 arturo182
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

CircuitPython library for interfacing the BB Q10 Keyboard over I2C.

* Author(s): arturo182

Implementation Notes
--------------------

**Hardware:**

* `BBQ10 Keyboard PMOD <https://www.tindie.com/products/17986/>`_
* `Keyboard FeatherWing <https://www.tindie.com/products/20905/>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
import digitalio
import time

__version__ = "0.2.0-auto.0"
__repo__ = "https://github.com/solderparty/arturo182_CircuitPython_bbq10keyboard.git"


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
_REG_BK2 = const(0x0A)  # backlight 2
_REG_DIR = const(0x0B)  # gpio direction
_REG_PUE = const(0x0C)  # gpio input pull enable
_REG_PUD = const(0x0D)  # gpio input pull direction
_REG_GIO = const(0x0E)  # gpio value
_REG_GIC = const(0x0F)  # gpio interrupt config
_REG_GIN = const(0x10)  # gpio interrupt status

_WRITE_MASK      = const(1 << 7)

CFG_OVERFLOW_ON  = const(1 << 0)
CFG_OVERFLOW_INT = const(1 << 1)
CFG_CAPSLOCK_INT = const(1 << 2)
CFG_NUMLOCK_INT  = const(1 << 3)
CFG_KEY_INT      = const(1 << 4)
CFG_PANIC_INT    = const(1 << 5)
CFG_REPORT_MODS  = const(1 << 6)
CFG_USE_MODS     = const(1 << 7)

INT_OVERFLOW     = const(1 << 0)
INT_CAPSLOCK     = const(1 << 1)
INT_NUMLOCK      = const(1 << 2)
INT_KEY          = const(1 << 3)
INT_PANIC        = const(1 << 4)
INT_GPIO         = const(1 << 5)  # since FW 0.4

KEY_CAPSLOCK     = const(1 << 5)
KEY_NUMLOCK      = const(1 << 6)
KEY_COUNT_MASK   = const(0x1F)

DIR_OUTPUT       = const(0)
DIR_INPUT        = const(1)

PUD_DOWN         = const(0)
PUD_UP           = const(1)

STATE_IDLE       = const(0)
STATE_PRESS      = const(1)
STATE_LONG_PRESS = const(2)
STATE_RELEASE    = const(3)


class DigitalInOut:
    def __init__(self, pin, kbd):
        if pin < 0 or pin > 7:
            raise ValueError('Only pins 0-7 supported right now')

        self._pin = pin
        self._kbd = kbd

    def switch_to_output(self, value=False):
        self.direction = digitalio.Direction.OUTPUT
        self.value = value

    def switch_to_input(self, pull=None):
        self.direction = digitalio.Direction.INPUT
        self.pull = pull

    @property
    def value(self):
        return self._kbd._get_register_bit(_REG_GIO, self._pin)

    @value.setter
    def value(self, value):
        self._kbd._update_register_bit(_REG_GIO, self._pin, value)

    @property
    def direction(self):
        if self._kbd._get_register_bit(_REG_DIR, self._pin) == DIR_INPUT:
            return digitalio.Direction.INPUT

        return digitalio.Direction.OUTPUT

    @direction.setter
    def direction(self, value):
        self._kbd._update_register_bit(_REG_DIR, self._pin, value == digitalio.Direction.INPUT)

    @property
    def pull(self):
        if self.direction == digitalio.Direction.OUTPUT:
            raise AttributeError('Pull not used when direction is output')

        if self._kbd._get_register_bit(_REG_PUE, self._pin):
            if self._kbd._get_register_bit(_REG_PUD, self._pin) == PUD_UP:
                return digitalio.Pull.UP

            return digitalio.Pull.DOWN

        return None

    @pull.setter
    def pull(self, value):
        if self.direction == digitalio.Direction.OUTPUT:
            raise AttributeError('Pull not used when direction is output')

        if value is None:
            self._kbd._update_register_bit(_REG_PUE, self._pin, False)
        else:
            self._kbd._update_register_bit(_REG_PUD, self._pin, value == digitalio.Pull.UP)
            self._kbd._update_register_bit(_REG_PUE, self._pin, True)


class BBQ10Keyboard:
    def __init__(self, i2c, BBQI2CDevice=None):
        self._i2cdelay = 0.01

        if not BBQI2CDevice:
            self._i2c = I2CDevice(i2c, _ADDRESS_KBD)
        else:
            self._i2c = BBQI2CDevice

        self._buffer = bytearray(2)
        self.reset()

    def reset(self):
        with self._i2c as i2c:
            self._buffer[0] = _REG_RST
            time.sleep(self._i2cdelay)
            i2c.write(self._buffer, end=1)

        # need to wait!
        time.sleep(0.05)

    @property
    def version(self):
        ver = self._read_register(_REG_VER)
        return (ver >> 4, ver & 0x0F)

    @property
    def status(self):
        return self._read_register(_REG_KEY)

    @property
    def key_count(self):
        return self.status & KEY_COUNT_MASK

    @property
    def key(self):
        if self.key_count == 0:
            return None

        with self._i2c as i2c:
            self._buffer[0] = _REG_FIF
            time.sleep(self._i2cdelay)
            i2c.write(self._buffer, end=1)
            time.sleep(self._i2cdelay)
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
        return self._read_register(_REG_BKL) / 255

    @backlight.setter
    def backlight(self, value):
        self._write_register(_REG_BKL, int(255 * value))

    @property
    def backlight2(self):
        if self.version < (0, 4):
            raise NotImplementedError('This function requires FW version 0.4 or newer')

        return self._read_register(_REG_BK2) / 255

    @backlight.setter
    def backlight2(self, value):
        if self.version < (0, 4):
            raise NotImplementedError('This function requires FW version 0.4 or newer')

        self._write_register(_REG_BK2, int(255 * value))

    @property
    def gpio(self):
        return self._read_register(_REG_GIO)

    @gpio.setter
    def gpio(self, value):
        self._write_register(_REG_GIO, value)

    def get_pin(self, pin):
        if pin < 0 or pin > 7:
            raise ValueError('Only pins 0-7 supported right now')

        return DigitalInOut(pin, self)

    def _read_register(self, reg):
        with self._i2c as i2c:
            self._buffer[0] = reg
            time.sleep(self._i2cdelay)
            i2c.write(self._buffer, end=1)
            time.sleep(self._i2cdelay)
            i2c.readinto(self._buffer, end=1)

        return self._buffer[0]

    def _write_register(self, reg, value):
        with self._i2c as i2c:
            self._buffer[0] = reg | _WRITE_MASK
            self._buffer[1] = value
            time.sleep(self._i2cdelay)
            i2c.write(self._buffer, end=2)

    def _update_register_bit(self, reg, bit, value):
        reg_val = self._read_register(reg)
        old_val = reg_val

        if value:
            reg_val |= (1 << bit)
        else:
            reg_val &= ~(1 << bit)

        if reg_val != old_val:
            self._write_register(reg, reg_val)

    def _get_register_bit(self, reg, bit):
        return self._read_register(reg) & (1 << bit) != 0

    keyboard_backlight = backlight
    display_backlight = backlight2

