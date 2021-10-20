# SPDX-FileCopyrightText: 2017 Jerry Needell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_stmpe610`
====================================================

This is a CircuitPython Driver for the STMPE610 Resistive Touch sensor

* Author(s): Jerry Needell
"""

# imports

import time
from micropython import const


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_STMPE610.git"


_STMPE_ADDR = const(0x41)
_STMPE_VERSION = const(0x0811)

_STMPE_SYS_CTRL1 = const(0x03)
_STMPE_SYS_CTRL1_RESET = const(0x02)
_STMPE_SYS_CTRL2 = const(0x04)

_STMPE_TSC_CTRL = const(0x40)
_STMPE_TSC_CTRL_EN = const(0x01)
_STMPE_TSC_CTRL_XYZ = const(0x00)
_STMPE_TSC_CTRL_XY = const(0x02)

_STMPE_INT_CTRL = const(0x09)
_STMPE_INT_CTRL_POL_HIGH = const(0x04)
_STMPE_INT_CTRL_POL_LOW = const(0x00)
_STMPE_INT_CTRL_EDGE = const(0x02)
_STMPE_INT_CTRL_LEVEL = const(0x00)
_STMPE_INT_CTRL_ENABLE = const(0x01)
_STMPE_INT_CTRL_DISABLE = const(0x00)


_STMPE_INT_EN = const(0x0A)
_STMPE_INT_EN_TOUCHDET = const(0x01)
_STMPE_INT_EN_FIFOTH = const(0x02)
_STMPE_INT_EN_FIFOOF = const(0x04)
_STMPE_INT_EN_FIFOFULL = const(0x08)
_STMPE_INT_EN_FIFOEMPTY = const(0x10)
_STMPE_INT_EN_ADC = const(0x40)
_STMPE_INT_EN_GPIO = const(0x80)

_STMPE_INT_STA = const(0x0B)
_STMPE_INT_STA_TOUCHDET = const(0x01)

_STMPE_ADC_CTRL1 = const(0x20)
_STMPE_ADC_CTRL1_12BIT = const(0x08)
_STMPE_ADC_CTRL1_10BIT = const(0x00)

_STMPE_ADC_CTRL2 = const(0x21)
_STMPE_ADC_CTRL2_1_625MHZ = const(0x00)
_STMPE_ADC_CTRL2_3_25MHZ = const(0x01)
_STMPE_ADC_CTRL2_6_5MHZ = const(0x02)

_STMPE_TSC_CFG = const(0x41)
_STMPE_TSC_CFG_1SAMPLE = const(0x00)
_STMPE_TSC_CFG_2SAMPLE = const(0x40)
_STMPE_TSC_CFG_4SAMPLE = const(0x80)
_STMPE_TSC_CFG_8SAMPLE = const(0xC0)
_STMPE_TSC_CFG_DELAY_10US = const(0x00)
_STMPE_TSC_CFG_DELAY_50US = const(0x08)
_STMPE_TSC_CFG_DELAY_100US = const(0x10)
_STMPE_TSC_CFG_DELAY_500US = const(0x18)
_STMPE_TSC_CFG_DELAY_1MS = const(0x20)
_STMPE_TSC_CFG_DELAY_5MS = const(0x28)
_STMPE_TSC_CFG_DELAY_10MS = const(0x30)
_STMPE_TSC_CFG_DELAY_50MS = const(0x38)
_STMPE_TSC_CFG_SETTLE_10US = const(0x00)
_STMPE_TSC_CFG_SETTLE_100US = const(0x01)
_STMPE_TSC_CFG_SETTLE_500US = const(0x02)
_STMPE_TSC_CFG_SETTLE_1MS = const(0x03)
_STMPE_TSC_CFG_SETTLE_5MS = const(0x04)
_STMPE_TSC_CFG_SETTLE_10MS = const(0x05)
_STMPE_TSC_CFG_SETTLE_50MS = const(0x06)
_STMPE_TSC_CFG_SETTLE_100MS = const(0x07)

_STMPE_FIFO_TH = const(0x4A)

_STMPE_FIFO_SIZE = const(0x4C)

_STMPE_FIFO_STA = const(0x4B)
_STMPE_FIFO_STA_RESET = const(0x01)
_STMPE_FIFO_STA_OFLOW = const(0x80)
_STMPE_FIFO_STA_FULL = const(0x40)
_STMPE_FIFO_STA_EMPTY = const(0x20)
_STMPE_FIFO_STA_THTRIG = const(0x10)

_STMPE_TSC_I_DRIVE = const(0x58)
_STMPE_TSC_I_DRIVE_20MA = const(0x00)
_STMPE_TSC_I_DRIVE_50MA = const(0x01)

_STMPE_TSC_DATA_X = const(0x4D)
_STMPE_TSC_DATA_Y = const(0x4F)
_STMPE_TSC_FRACTION_Z = const(0x56)

_STMPE_GPIO_SET_PIN = const(0x10)
_STMPE_GPIO_CLR_PIN = const(0x11)
_STMPE_GPIO_DIR = const(0x13)
_STMPE_GPIO_ALT_FUNCT = const(0x17)


class Adafruit_STMPE610:
    """
    A driver for the STMPE610 Resistive Touch sensor.
    """

    def __init__(self):
        """Reset the controller"""
        self._write_register_byte(_STMPE_SYS_CTRL1, _STMPE_SYS_CTRL1_RESET)
        time.sleep(0.001)

        self._write_register_byte(_STMPE_SYS_CTRL2, 0x0)  # turn on clocks!
        self._write_register_byte(
            _STMPE_TSC_CTRL, _STMPE_TSC_CTRL_XYZ | _STMPE_TSC_CTRL_EN
        )  # XYZ and enable!
        self._write_register_byte(_STMPE_INT_EN, _STMPE_INT_EN_TOUCHDET)
        self._write_register_byte(
            _STMPE_ADC_CTRL1, _STMPE_ADC_CTRL1_10BIT | (0x6 << 4)
        )  # 96 clocks per conversion
        self._write_register_byte(_STMPE_ADC_CTRL2, _STMPE_ADC_CTRL2_6_5MHZ)
        self._write_register_byte(
            _STMPE_TSC_CFG,
            _STMPE_TSC_CFG_4SAMPLE
            | _STMPE_TSC_CFG_DELAY_1MS
            | _STMPE_TSC_CFG_SETTLE_5MS,
        )
        self._write_register_byte(_STMPE_TSC_FRACTION_Z, 0x6)
        self._write_register_byte(_STMPE_FIFO_TH, 1)
        self._write_register_byte(_STMPE_FIFO_STA, _STMPE_FIFO_STA_RESET)
        self._write_register_byte(_STMPE_FIFO_STA, 0)  # unreset
        self._write_register_byte(_STMPE_TSC_I_DRIVE, _STMPE_TSC_I_DRIVE_50MA)
        self._write_register_byte(_STMPE_INT_STA, 0xFF)  # reset all ints
        self._write_register_byte(
            _STMPE_INT_CTRL, _STMPE_INT_CTRL_POL_HIGH | _STMPE_INT_CTRL_ENABLE
        )

    def read_data(self):
        """Request next stored reading - return tuple containing  (x,y,pressure) """
        d_1 = self._read_byte(0xD7)
        d_2 = self._read_byte(0xD7)
        d_3 = self._read_byte(0xD7)
        d_4 = self._read_byte(0xD7)
        x_loc = d_1 << 4 | d_2 >> 4
        y_loc = (d_2 & 0xF) << 8 | d_3
        pressure = d_4
        # reset all ints  (not sure what this does)
        if self.buffer_empty:
            self._write_register_byte(_STMPE_INT_STA, 0xFF)
        return (x_loc, y_loc, pressure)

    def _read_byte(self, register):
        """Read a byte register value and return it"""
        return self._read_register(register, 1)[0]

    def _read_register(self, register, length):
        # Read an arbitrarily long register (specified by length number of
        # bytes) and return a bytearray of the retrieved data.
        # Subclasses MUST implement this!
        raise NotImplementedError

    def _write_register_byte(self, register, value):
        # Write a single byte register at the specified register address.
        # Subclasses MUST implement this!
        raise NotImplementedError

    @property
    def touches(self):
        """
        Returns a list of touchpoint dicts, with 'x' and 'y' containing the
        touch coordinates, and 'pressure'
        """
        touchpoints = []
        while (len(touchpoints) < 4) and not self.buffer_empty:
            (x_loc, y_loc, pressure) = self.read_data()
            point = {"x": x_loc, "y": y_loc, "pressure": pressure}
            touchpoints.append(point)
        return touchpoints

    @property
    def get_version(self):
        "Read the version number from the sensosr"
        v_1 = self._read_byte(0)
        v_2 = self._read_byte(1)
        version = v_1 << 8 | v_2
        # print("version ",hex(version))
        return version

    @property
    def touched(self):
        "Report if any touches have been detectd"
        touch = self._read_byte(_STMPE_TSC_CTRL) & 0x80
        return touch == 0x80

    @property
    def buffer_size(self):
        "The amount of touch data in the buffer"
        return self._read_byte(_STMPE_FIFO_SIZE)

    @property
    def buffer_empty(self):
        "Buffer empty status"
        empty = self._read_byte(_STMPE_FIFO_STA) & _STMPE_FIFO_STA_EMPTY
        return empty != 0

    @property
    def get_point(self):
        "Read one touch from the buffer"
        (x_loc, y_loc, pressure) = self.read_data()
        point = {"x": x_loc, "y": y_loc, "pressure": pressure}
        return point


class Adafruit_STMPE610_I2C(Adafruit_STMPE610):
    """
    I2C driver for the STMPE610 Resistive Touch sensor.
    """

    def __init__(self, i2c, address=_STMPE_ADDR):
        """
        Check the STMPE610 was founnd
        Default address is 0x41 but another address can be passed in as an argument
        """
        import adafruit_bus_device.i2c_device as i2cdev  # pylint: disable=import-outside-toplevel

        self._i2c = i2cdev.I2CDevice(i2c, address)
        # Check device version.
        version = self.get_version
        if _STMPE_VERSION != version:
            raise RuntimeError("Failed to find STMPE610! Chip Version 0x%x" % version)
        super().__init__()

    def _read_register(self, register, length):
        """Low level register reading over I2C, returns a list of values"""
        with self._i2c as i2c:
            i2c.write(bytearray([register & 0xFF]))
            result = bytearray(length)
            i2c.readinto(result)
            # print("$%02X => %s" % (register, [hex(i) for i in result]))
            return result

    def _write_register_byte(self, register, value):
        """Low level register writing over I2C, writes one 8-bit value"""
        with self._i2c as i2c:
            i2c.write(bytes([register & 0xFF, value & 0xFF]))
            # print("$%02X <= 0x%02X" % (register, value))


class Adafruit_STMPE610_SPI(Adafruit_STMPE610):
    """
    SPI driver for the STMPE610 Resistive Touch sensor.
    """

    def __init__(self, spi, cs, baudrate=1000000):
        """
        Check the STMPE610 was found,Default clock rate 1000000 - can be changed with 'baudrate'
        """
        import adafruit_bus_device.spi_device as spidev  # pylint: disable=import-outside-toplevel

        self._spi = spidev.SPIDevice(spi, cs, baudrate=baudrate)
        # Check device version.
        version = self.get_version
        if _STMPE_VERSION != version:
            # if it fails try SPI MODE 1  -- that is what Arduino does
            self._spi = spidev.SPIDevice(
                spi, cs, baudrate=baudrate, polarity=0, phase=1
            )
            version = self.get_version
            if _STMPE_VERSION != version:
                raise RuntimeError(
                    "Failed to find STMPE610! Chip Version 0x%x. "
                    "If you are using the breakout, verify you are in SPI mode."
                    % version
                )
        super().__init__()

    # pylint: disable=no-member
    # Disable should be reconsidered when refactor can be tested.
    def _read_register(self, register, length):
        """Low level register reading over SPI, returns a list of values"""
        register = (register | 0x80) & 0xFF  # Read single, bit 7 high.
        with self._spi as spi:
            spi.write(bytearray([register]))
            result = bytearray(length)
            spi.readinto(result)
            #            print("$%02X => %s" % (register, [hex(i) for i in result]))
            return result

    def _write_register_byte(self, register, value):
        """Low level register writing over SPI, writes one 8-bit value"""
        register &= 0x7F  # Write, bit 7 low.
        with self._spi as spi:
            spi.write(bytes([register, value & 0xFF]))
