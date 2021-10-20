# SPDX-FileCopyrightText: 2019 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_pct2075`
================================================================================

CircuitPython library for the NXP PCT2075 Digital Temperature Sensor


* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**

* `Adafruit PCT2075 Temperature Sensor Breakout
  <https://www.adafruit.com/products/4369>`_ (Product ID: 4369)

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library:
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

* Adafruit's Register library:
  https://github.com/adafruit/Adafruit_CircuitPython_Register

"""

from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_bit import RWBit
import adafruit_bus_device.i2c_device as i2cdevice

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_PCT2075.git"
# pylint: disable=too-few-public-methods
PCT2075_DEFAULT_ADDRESS = 0x37  # Address is configured with pins A0-A2

PCT2075_REGISTER_TEMP = 0  # Temperature register (read-only)
PCT2075_REGISTER_CONFIG = 1  # Configuration register
PCT2075_REGISTER_THYST = 2  # Hysterisis register
PCT2075_REGISTER_TOS = 3  # OS register
PCT2075_REGISTER_TIDLE = 4  # Measurement idle time register


class Mode:
    """Options for `Mode`"""

    INTERRUPT = 1
    COMPARITOR = 0


class FaultCount:
    """Options for `faults_to_alert`"""

    FAULT_1 = 0
    FAULT_2 = 1
    FAULT_4 = 2
    FAULT_6 = 3


# pylint: enable=too-few-public-methods


class PCT2075:
    """Driver for the PCT2075 Digital Temperature Sensor and Thermal Watchdog.

    :param ~busio.I2C i2c_bus: The I2C bus the PCT2075 is connected to.
    :param address: The I2C device address. Default is :const:`0x37`

    **Quickstart: Importing and using the PCT2075 temperature sensor**

        Here is an example of using the :class:`PCT2075` class.
        First you will need to import the libraries to use the sensor

        .. code-block:: python

            import board
            import adafruit_pct2075

        Once this is done you can define your `board.I2C` object and define your sensor object

        .. code-block:: python

            i2c = board.I2C()  # uses board.SCL and board.SDA
            pct = adafruit_pct2075.PCT2075(i2c)

        Now you have access to the temperature using the attribute :attr:`temperature`.

        .. code-block:: python

            temperature = pct.temperature

    """

    def __init__(self, i2c_bus, address=PCT2075_DEFAULT_ADDRESS):
        self.i2c_device = i2cdevice.I2CDevice(i2c_bus, address)

    _temperature = ROUnaryStruct(PCT2075_REGISTER_TEMP, ">h")
    mode = RWBit(PCT2075_REGISTER_CONFIG, 1, register_width=1)
    """Sets the alert mode. In comparator mode, the sensor acts like a thermostat and will activate
    the INT pin according to `high_temp_active_high` when an alert is triggered. The INT pin will be
    deactivated when the temperature falls below :attr:`temperature_hysteresis`.
    In interrupt mode the INT pin is activated once when a temperature fault
    is detected, and once more when the     temperature falls below
    :attr:`temperature_hysteresis`. In interrupt mode, the alert is cleared by
    reading a property"""

    shutdown = RWBit(PCT2075_REGISTER_CONFIG, 0, 1)
    """Set to True to turn off the temperature measurement circuitry in the sensor. While shut down
    the configurations properties can still be read or written but the temperature will not be
    measured"""
    _fault_queue_length = RWBits(2, PCT2075_REGISTER_CONFIG, 3, register_width=1)
    _high_temperature_threshold = UnaryStruct(PCT2075_REGISTER_TOS, ">h")
    _temp_hysteresis = UnaryStruct(PCT2075_REGISTER_THYST, ">h")
    _idle_time = RWBits(5, PCT2075_REGISTER_TIDLE, 0, register_width=1)
    high_temp_active_high = RWBit(PCT2075_REGISTER_CONFIG, 2, register_width=1)
    """Sets the alert polarity. When False the INT pin will be tied to ground when an alert is
    triggered. If set to True it will be disconnected from ground when an alert is triggered."""

    @property
    def temperature(self):
        """Returns the current temperature in degrees Celsius.
        Resolution is 0.125 degrees Celsius"""
        return (self._temperature >> 5) * 0.125

    @property
    def high_temperature_threshold(self):
        """The temperature in degrees celsius that will trigger an alert on the INT pin if it is
        exceeded. Resolution is 0.5 degrees Celsius"""
        return (self._high_temperature_threshold >> 7) * 0.5

    @high_temperature_threshold.setter
    def high_temperature_threshold(self, value):
        self._high_temperature_threshold = int(value * 2) << 7

    @property
    def temperature_hysteresis(self):
        """The temperature hysteresis value defines the bottom
        of the temperature range in degrees Celsius in which
        the temperature is still considered high.
        :attr:`temperature_hysteresis` must be lower than
        :attr:`high_temperature_threshold`.
        Resolution is 0.5 degrees Celsius
        """
        return (self._temp_hysteresis >> 7) * 0.5

    @temperature_hysteresis.setter
    def temperature_hysteresis(self, value):
        if value >= self.high_temperature_threshold:
            raise ValueError(
                "temperature_hysteresis must be less than high_temperature_threshold"
            )
        self._temp_hysteresis = int(value * 2) << 7

    @property
    def faults_to_alert(self):
        """The number of consecutive high temperature faults required to raise an alert. An fault
        is tripped each time the sensor measures the temperature to be greater than
        :attr:`high_temperature_threshold`. The rate at which the sensor measures the temperature
        is defined by :attr:`delay_between_measurements`.
        """

        return self._fault_queue_length

    @faults_to_alert.setter
    def faults_to_alert(self, value):
        if value > 4 or value < 1:
            raise ValueError("faults_to_alert must be an adafruit_pct2075.FaultCount")
        self._fault_queue_length = value

    @property
    def delay_between_measurements(self):
        """The amount of time between measurements made by the sensor in milliseconds. The value
        must be between 100 and 3100 and a multiple of 100"""
        return self._idle_time * 100

    @delay_between_measurements.setter
    def delay_between_measurements(self, value):
        if value > 3100 or value < 100 or value % 100 > 0:
            raise AttributeError(
                """"delay_between_measurements must be >= 100 or <= 3100\
            and a multiple of 100"""
            )
        self._idle_time = int(value / 100)
