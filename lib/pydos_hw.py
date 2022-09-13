"""
    GPIO abstraction layer

"""
from sys import implementation
from pydos_bcfg import Pydos_pins
if implementation.name.upper() == "MICROPYTHON":
    from os import uname
    from machine import Pin
    from machine import SoftI2C as s_I2C
    from machine import I2C as m_I2C
    from machine import SoftSPI as s_SPI
    from machine import SPI as m_SPI

elif implementation.name.upper() == "CIRCUITPYTHON":
    try:
        from adafruit_bus_device.i2c_device import I2CDevice
    except:
        pass
    import digitalio
    import busio
    import board

    if board.board_id == "unexpectedmaker_feathers2":
        try:
            import kfw_s2_board as board
        except ImportError:
            pass
    elif board.board_id == "raspberry_pi_pico":
        try:
            import kfw_pico_board as board
            foundBoard = True
        except ImportError:
            foundBoard = False

        if not foundBoard:
            try:
                import cyt_mpp_board as board
            except ImportError:
                pass

class PyDOS_HW:

    _I2C = None
    _I2C_power = None
    _SPI = None
    _SD_SPI = None
    sndPin = None
    sndGPIO = None
    neoPixel = None
    neoPixel_Pow = None
    dotStar_Clock = None
    dotStar_Data = None
    led = None
    I2C_NUM = None
    SCL = None
    SDA = None
    SD_SPI_NUM = None
    SD_SCK = None
    SD_MOSI = None
    SD_MISO = None
    SD_CS = None
    SPI_NUM = None
    SCK = None
    MOSI = None
    MISO = None
    CS = None
    I2CbbqDevice = None
    KFW = False

    def __init__(self):

        self.sndPin = Pydos_pins.get('sndPin',(None,None))[0]
        self.neoPixel = Pydos_pins.get('neoPixel',(None,None))[0]
        self.neoPixel_Pow = Pydos_pins.get('neoPixel_Pow',(None,None))[0]
        self.dotStar_Clock = Pydos_pins.get('dotStar_Clock',(None,None))[0]
        self.dotStar_Data = Pydos_pins.get('dotStar_Data',(None,None))[0]
        self.led = Pydos_pins.get('led',(None,None))[0]

        if implementation.name.upper() == 'MICROPYTHON':
            if self.sndPin:
                self.sndPin = Pin(self.sndPin)

            if self.neoPixel:
                self.neoPixel = Pin(self.neoPixel)

            if self.neoPixel_Pow:
                self.neoPixel_Pow = Pin(self.neoPixel_Pow,Pin.OUT)

        self.I2C_NUM=Pydos_pins.get('I2C_NUM',(None,None))[0]
        self.SCL=Pydos_pins.get('SCL',(None,None))[0]
        self.SDA=Pydos_pins.get('SDA',(None,None))[0]
        self.SD_SPI_NUM=Pydos_pins.get('SD_SPI_NUM',(None,None))[0]
        self.SD_SCK=Pydos_pins.get('SD_SCK',(None,None))[0]
        self.SD_MOSI=Pydos_pins.get('SD_MOSI',(None,None))[0]
        self.SD_MISO=Pydos_pins.get('SD_MISO',(None,None))[0]
        self.SD_CS=Pydos_pins.get('SD_CS',(None,None))[0]
        self.SPI_NUM=Pydos_pins.get('SPI_NUM',(None,None))[0]
        self.SCK=Pydos_pins.get('SCK',(None,None))[0]
        self.MOSI=Pydos_pins.get('MOSI',(None,None))[0]
        self.MISO=Pydos_pins.get('MISO',(None,None))[0]
        self.CS=Pydos_pins.get('CS',(None,None))[0]

        if implementation.name.upper() == 'CIRCUITPYTHON':
            if self.CS:
                self.CS = digitalio.DigitalInOut(self.CS)
            if self.SD_CS:
                self.SD_CS = digitalio.DigitalInOut(self.SD_CS)

            if self.sndPin:
                self.sndGPIO = digitalio.DigitalInOut(self.sndPin)
                self.sndGPIO.direction = digitalio.Direction.OUTPUT
                self.sndGPIO.value = False

            try:
                chkForFile = open('/lib/kfw_pico_board.py','r')
                chkForFile.close()
                self.KFW = True
            except:
                pass
            if not self.KFW:
                try:
                    chkForFile = open('/lib/kfw_s2_board.py','r')
                    chkForFile.close()
                    self.KFW = True
                except:
                    pass

            if self.KFW:
                self.neoPixel = board.D11
            elif self.neoPixel is None and 'NEOPIXEL' in dir(board):
                self.neoPixel = board.NEOPIXEL

    def quietSnd(self):

        if implementation.name.upper() == "CIRCUITPYTHON":
            if self.sndPin:
                self.sndGPIO = digitalio.DigitalInOut(self.sndPin)
                #self.sndGPIO.direction = digitalio.Direction.OUTPUT
        return

    def I2C(self):

        if not self._I2C:
            if implementation.name.upper() == "CIRCUITPYTHON":

                if 'I2C_POWER_INVERTED' in dir(board) and not self._I2C_power:
                    self._I2C_power = digitalio.DigitalInOut(board.I2C_POWER_INVERTED)
                    self._I2C_power.direction = digitalio.Direction.OUTPUT
                    self._I2C_power.value = False

                if 'STEMMA_I2C' in dir(board):
                    self._I2C = board.STEMMA_I2C()
                elif 'I2C' in dir(board):
                    self._I2C = board.I2C()
                else:
                    self._I2C = busio.I2C(self.SCL, self.SDA)

                if self.KFW and not self.I2CbbqDevice:
                    self.I2CbbqDevice = I2CDevice(self._I2C, 0x1F)
            elif implementation.name.upper() == "MICROPYTHON":
                if self.I2C_NUM:
                    self._I2C = m_I2C(self.I2C_NUM,scl=Pin(self.SCL),sda=Pin(self.SDA))
                else:
                    self._I2C = s_I2C(scl=Pin(self.SCL),sda=Pin(self.SDA))

        return self._I2C

    def I2C_deinit(self):
        if implementation.name.upper() == "CIRCUITPYTHON":
            if self._I2C_power:
                self._I2C_power.deinit()
                self._I2C_power = None

            if self._I2C:
                self._I2C.deinit()
            self._I2C = None
            self.I2CbbqDevice = None

    def SD_deinit(self):
        if self._SD_SPI:
            if self._SPI == self._SD_SPI:
                self._SPI = None
            self.SD_SPI().deinit()
            self._SD_SPI = None

    def SPI_deinit(self):
        if self._SPI:
            if self._SPI == self._SD_SPI:
                self._SD_SPI = None
            self.SPI().deinit()
            self._SPI = None

    def SPI(self):
        if not self._SPI:
            if implementation.name.upper() == "CIRCUITPYTHON":
                if 'SPI' in dir(board):
                    self._SPI = board.SPI()
                else:
                    if self.SCK:
                        trybitbangio = False
                        try:
                            self._SPI = busio.SPI(self.SCK, self.MOSI, self.MISO)
                        except ValueError:
                            trybitbangio = True

                        if trybitbangio:
                            try:
                                import bitbangio
                            except ImportError:
                                trybitbangio = False
                                print('SPI Create Fail')

                        if trybitbangio:
                            self._SPI = bitbangio.SPI(self.SCK, self.MOSI, self.MISO)

            elif implementation.name.upper() == "MICROPYTHON":
                if Pydos_hw.SPI_NUM != None:
                    self._SPI = m_SPI(Pydos_hw.SPI_NUM)
                else:
                    if self.SCK:
                        self._SPI = s_SPI(sck=Pin(Pydos_hw.SCK),mosi=Pin(Pydos_hw.MOSI), \
                            miso=Pin(Pydos_hw.MISO))
        return self._SPI

    def SD_SPI(self):
        if not self._SD_SPI:
            if implementation.name.upper() == "CIRCUITPYTHON":
                if 'SD_SPI' in dir(board):
                    self._SD_SPI = board.SD_SPI()
                else:
                    if self.SD_SCK:
                        trybitbangio = False
                        try:
                            self._SD_SPI = busio.SPI(self.SD_SCK, self.SD_MOSI, self.SD_MISO)
                        except ValueError:
                            trybitbangio = True

                        if trybitbangio:
                            try:
                                import bitbangio
                            except ImportError:
                                trybitbangio = False
                                print('SD_SPI Create Fail')

                        if trybitbangio:
                            self._SD_SPI = bitbangio.SPI(self.SD_SCK, self.SD_MOSI, self.SD_MISO)
                    else:
                        self._SD_SPI = self.SPI()
            elif implementation.name.upper() == "MICROPYTHON":
                if Pydos_hw.SD_SPI_NUM != None:
                    self._SD_SPI = m_SPI(Pydos_hw.SD_SPI_NUM)
                else:
                    if self.SD_SCK:
                        self._SD_SPI = s_SPI(sck=Pin(Pydos_hw.SD_SCK),mosi=Pin(Pydos_hw.SD_MOSI), \
                            miso=Pin(Pydos_hw.SD_MISO))
                    else:
                        self._SD_SPI = self.SPI()

        return self._SD_SPI

Pydos_hw = PyDOS_HW()
sndPin = Pydos_hw.sndPin
sndGPIO = Pydos_hw.sndGPIO
