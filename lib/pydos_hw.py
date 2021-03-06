"""
    GPIO abstraction layer

"""
from sys import implementation
if implementation.name.upper() == "MICROPYTHON":
    from os import uname
    from machine import Pin
    from machine import SoftI2C as s_I2C
    from machine import I2C as m_I2C

elif implementation.name.upper() == "CIRCUITPYTHON":
    from adafruit_bus_device.i2c_device import I2CDevice
    import digitalio
    import busio
    import board

    if board.board_id == "unexpectedmaker_feathers2":
        try:
            import kfw_s2_board as board
        except:
            pass
    elif board.board_id == "raspberry_pi_pico":
        try:
            import kfw_pico_board as board
            foundBoard = True
        except:
            foundBoard = False

        if not foundBoard:
            try:
                import cyt_mpp_board as board
            except:
                pass

class PyDOS_HW:

    _I2C = None
    _I2C_power = None
    _SPI = None
    _SD_SPI = None
    SD_CS = None
    sndPin = None
    sndGPIO = None
    neoPixel = None
    SCL = None
    SDA = None
    I2CbbqDevice = None
    KFW = False


    def __init__(self):

        if implementation.name.upper() == 'MICROPYTHON':

            if uname().machine == 'TinyPICO with ESP32-PICO-D4':
                PyDOS_HW.sndPin = Pin(27)
                PyDOS_HW.SCL=22
                PyDOS_HW.SDA=21
            elif uname().machine == 'SparkFun Thing Plus RP2040 with RP2040':
                PyDOS_HW.sndPin = Pin(19)
                PyDOS_HW.neoPixel = Pin(8)
                PyDOS_HW.SCL=7
                PyDOS_HW.SDA=6
            elif uname().machine == 'Arduino Nano RP2040 Connect with RP2040':
                PyDOS_HW.sndPin = Pin(29) # A3
                PyDOS_HW.SCL=13
                PyDOS_HW.SDA=12
            elif uname().machine == 'Raspberry Pi Pico with RP2040':
                try:
                    chkForFile = open('/lib/cyt_mpp_board.py')
                    chkForFile.close()
                    PyDOS_HW.neoPixel = Pin(28)
                except:
                    pass
                PyDOS_HW.sndPin = Pin(18)
                PyDOS_HW.SCL=3
                PyDOS_HW.SDA=2
            elif uname().machine == 'ESP32S3 module (spiram) with ESP32S3' or 'ESP32S3' in uname().machine:
                PyDOS_HW.sndPin = Pin(10)
                PyDOS_HW.neoPixel = Pin(48)
                PyDOS_HW.SCL=7
                PyDOS_HW.SDA=6
            elif uname().machine == 'ESP32C3 module with ESP32C3':
                PyDOS_HW.sndPin = Pin(0)
                PyDOS_HW.neoPixel = Pin(2)
                PyDOS_HW.SCL=6
                PyDOS_HW.SDA=5
            else:
                #Use D12 on Feathers
                try:
                    PyDOS_HW.sndPin = Pin(12)
                except:
                    pass
                try:
                    PyDOS_HW.neoPixel = Pin(16)
                except:
                    pass
                PyDOS_HW.SCL=3
                PyDOS_HW.SDA=2

        elif implementation.name.upper() == 'CIRCUITPYTHON':
            if "SD_CS" in dir(board):
                PyDOS_HW.SD_CS = digitalio.DigitalInOut(board.SD_CS)
            else:
                if 'D5' in dir(board):
                    PyDOS_HW.SD_CS = digitalio.DigitalInOut(board.D5)
                elif 'GP5' in dir(board):
                    PyDOS_HW.SD_CS = digitalio.DigitalInOut(board.GP5)
                elif 'IO5' in dir(board):
                    PyDOS_HW.SD_CS = digitalio.DigitalInOut(board.IO5)

            if 'SCL' in dir(board):
                PyDOS_HW.SCL=board.SCL
                PyDOS_HW.SDA=board.SDA
            elif board.board_id in ["cytron_maker_pi_rp2040","raspberry_pi_pico"]:
                # Grove #2, GP3 & GP2
                PyDOS_HW.SCL=board.GP3
                PyDOS_HW.SDA=board.GP2
            elif 'STEMMA_I2C' in dir(board) or 'I2C' in dir(board):
                pass
            else:
                if 'IO7' in dir(board): # esp32s3_devkitc_1_n8r2, LILYGO_S2
                    PyDOS_HW.SCL=board.IO7
                    PyDOS_HW.SDA=board.IO6

            if "SNDPIN" in dir(board):
                PyDOS_HW.sndPin = board.SNDPIN
            elif "BUZZER" in dir(board):
                PyDOS_HW.sndPin = board.BUZZER
            else:
                if board.board_id in ["arduino_nano_rp2040_connect","adafruit_qtpy_esp32s2",
                    "adafruit_qtpy_esp32c3","sparkfun_nrf52840_mini"]:
                    PyDOS_HW.sndPin = board.A3
                elif board.board_id == "raspberry_pi_pico":
                    PyDOS_HW.sndPin = board.GP7
                elif board.board_id == "sparkfun_thing_plus_rp2040":
                    PyDOS_HW.sndPin = board.D19
                elif board.board_id == "adafruit_kb2040":
                    PyDOS_HW.sndPin = board.D3
                elif board.board_id == "lilygo_ttgo_t8_s2_st7789":
                    PyDOS_HW.sndPin = board.IO3
                elif board.board_id == "espressif_esp32s3_devkitc_1_n8r2":
                    PyDOS_HW.sndPin = board.IO10
                else:
                    #Use D12 on Feathers
                    if 'D12' in dir(board):
                        PyDOS_HW.sndPin = board.D12
                    elif 'GP12' in dir(board):
                        PyDOS_HW.sndPin = board.GP12
                    elif 'IO12' in dir(board):
                        PyDOS_HW.sndPin = board.IO12
                    else:
                        PyDOS_HW.sndPin = None

            if PyDOS_HW.sndPin:
                PyDOS_HW.sndGPIO = digitalio.DigitalInOut(PyDOS_HW.sndPin)
                PyDOS_HW.sndGPIO.direction = digitalio.Direction.OUTPUT
                PyDOS_HW.sndGPIO.value = False

            try:
                chkForFile = open('/lib/kfw_pico_board.py','r')
                chkForFile.close()
                PyDOS_HW.KFW = True
            except:
                pass
            if not PyDOS_HW.KFW:
                try:
                    chkForFile = open('/lib/kfw_s2_board.py','r')
                    chkForFile.close()
                    PyDOS_HW.KFW = True
                except:
                    pass

            if PyDOS_HW.KFW:
                PyDOS_HW.neoPixel = board.D11
            elif "NEOPIXEL" in dir(board):
                PyDOS_HW.neoPixel = board.NEOPIXEL

    def quietSnd(self):

        if implementation.name.upper() == "CIRCUITPYTHON":
            if PyDOS_HW.sndPin:
                PyDOS_HW.sndGPIO = digitalio.DigitalInOut(PyDOS_HW.sndPin)
                #PyDOS_HW.sndGPIO.direction = digitalio.Direction.OUTPUT
        return

    def I2C():

        if not PyDOS_HW._I2C:
            if implementation.name.upper() == "CIRCUITPYTHON":

                if 'I2C_POWER_INVERTED' in dir(board) and not PyDOS_HW._I2C_power:
                    PyDOS_HW._I2C_power = digitalio.DigitalInOut(board.I2C_POWER_INVERTED)
                    PyDOS_HW._I2C_power.direction = digitalio.Direction.OUTPUT
                    PyDOS_HW._I2C_power.value = False

                if 'STEMMA_I2C' in dir(board):
                    PyDOS_HW._I2C = board.STEMMA_I2C()
                elif 'I2C' in dir(board):
                    PyDOS_HW._I2C = board.I2C()
                else:
                    PyDOS_HW._I2C = busio.I2C(PyDOS_HW.SCL, PyDOS_HW.SDA)

                if PyDOS_HW.KFW and not PyDOS_HW.I2CbbqDevice:
                    PyDOS_HW.I2CbbqDevice = I2CDevice(PyDOS_HW._I2C, 0x1F)
            elif implementation.name.upper() == "MICROPYTHON":
                if uname().machine in ['Arduino Nano RP2040 Connect with RP2040']:
                    PyDOS_HW._I2C = m_I2C(0,scl=Pin(PyDOS_HW.SCL),sda=Pin(PyDOS_HW.SDA))
                elif uname().machine in ['Raspberry Pi Pico with RP2040']:
                    PyDOS_HW._I2C = m_I2C(1,scl=Pin(PyDOS_HW.SCL),sda=Pin(PyDOS_HW.SDA))
                else:
                    PyDOS_HW._I2C = s_I2C(scl=Pin(PyDOS_HW.SCL),sda=Pin(PyDOS_HW.SDA))

        return PyDOS_HW._I2C

    def I2C_deinit():
        if implementation.name.upper() == "CIRCUITPYTHON":
            if PyDOS_HW._I2C_power:
                PyDOS_HW._I2C_power.deinit()
                PyDOS_HW._I2C_power = None

            if PyDOS_HW._I2C:
                PyDOS_HW._I2C.deinit()
            PyDOS_HW._I2C = None
            PyDOS_HW.I2CbbqDevice = None

    def SD_deinit():
        if implementation.name.upper() == "CIRCUITPYTHON":
            if PyDOS_HW._SD_SPI:
                PyDOS_HW.SD_SPI().deinit()
                if PyDOS_HW._SPI == PyDOS_HW._SD_SPI:
                    PyDOS_HW._SPI = None
                PyDOS_HW._SD_SPI = None

    def SPI():
        if implementation.name.upper() == "CIRCUITPYTHON":
            if not PyDOS_HW._SPI:
                if 'SPI' in dir(board):
                    PyDOS_HW._SPI = board.SPI()
                else:
                    _SCK = None
                    if 'SCK' in dir(board):
                        _SCK = board.SCK
                    elif 'CLK' in dir(board):
                        _SCK = board.CLK
                    if _SCK:
                        if 'MOSI' in dir(board):
                            PyDOS_HW._SPI = busio.SPI(_SCK, board.MOSI, board.MISO)
                        elif 'COPI' in dir(board):
                            PyDOS_HW._SPI = busio.SPI(_SCK, board.COPI, board.CIPO)
                    else:
                        if 'D14' in dir(board):
                            PyDOS_HW._SPI = busio.SPI(board.D14, board.D15, board.D12)
                        elif 'GP14' in dir(board):
                            PyDOS_HW._SPI = busio.SPI(board.GP14, board.GP15, board.GP12)
                        elif 'IO14' in dir(board):
                            PyDOS_HW._SPI = busio.SPI(board.IO14, board.IO15, board.IO12)

        return PyDOS_HW._SPI

    def SD_SPI():
        if implementation.name.upper() == "CIRCUITPYTHON":
            if not PyDOS_HW._SD_SPI:
                if 'SD_SPI' in dir(board):
                    PyDOS_HW._SD_SPI = board.SD_SPI()
                else:
                    _SCK = None
                    if 'SD_SCK' in dir(board):
                        _SCK = board.SD_SCK
                    elif 'SD_CLK' in dir(board):
                        _SCK = board.SD_CLK
                    if _SCK:
                        if 'SD_MOSI' in dir(board):
                            PyDOS_HW._SD_SPI = busio.SPI(_SCK, board.SD_MOSI, board.SD_MISO)
                        elif 'SD_COPI' in dir(board):
                            PyDOS_HW._SD_SPI = busio.SPI(_SCK, board.SD_COPI, board.SD_CIPO)
                    else:
                        PyDOS_HW._SD_SPI = PyDOS_HW.SPI()

        return PyDOS_HW._SD_SPI


Pydos_hw = PyDOS_HW()
sndPin = Pydos_hw.sndPin
sndGPIO = Pydos_hw.sndGPIO
neoPixel = Pydos_hw.neoPixel
