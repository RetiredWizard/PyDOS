"""
    GPIO abstraction layer

"""
from sys import implementation
if implementation.name.upper() == "MICROPYTHON":
    from os import uname
    from machine import Pin
    from machine import I2C as m_I2C

elif implementation.name.upper() == "CIRCUITPYTHON":
    import digitalio
    import busio
    import board
    if board.board_id == "unexpectedmaker_feathers2":
        try:
            import kfw_s2_board as board
            foundBoard = True
        except:
            foundBoard = False

    if board.board_id == "raspberry_pi_pico":
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


    def __init__(self):

        if implementation.name.upper() == 'MICROPYTHON':

            if uname().machine == 'TinyPICO with ESP32-PICO-D4':
                PyDOS_HW.sndPin = Pin(19)
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
                    import cyt_mpp_board
                    PyDOS_HW.sndPin = Pin(18)
                    PyDOS_HW.neoPixel = Pin(28)
                except:
                    PyDOS_HW.sndPin = Pin(11)
                PyDOS_HW.SCL=3
                PyDOS_HW.SDA=2
            elif 'ESP32S3 module' in uname().machine:
                PyDOS_HW.sndPin = Pin(12)
                PyDOS_HW.neoPixel = Pin(48)
                PyDOS_HW.SCL=7
                PyDOS_HW.SDA=6
            else:
                #Use D12 on Feathers
                PyDOS_HW.sndPin = Pin(12)
                PyDOS_HW.neoPixel = Pin(16)
                PyDOS_HW.SCL=3
                PyDOS_HW.SDA=2

        elif implementation.name.upper() == 'CIRCUITPYTHON':
            if "SNDPIN" in dir(board):
                PyDOS_HW.sndPin = board.SNDPIN
            elif "BUZZER" in dir(board):
                PyDOS_HW.sndPin = board.BUZZER
            else:
                if board.board_id in ["arduino_nano_rp2040_connect","adafruit_qtpy_esp32s2"]:
                    PyDOS_HW.sndPin = board.A3
                elif board.board_id == "raspberry_pi_pico":
                    #D12 is GP11 on the Raspberry PICO
                    PyDOS_HW.sndPin = board.GP11
                elif board.board_id == "sparkfun_thing_plus_rp2040":
                    PyDOS_HW.sndPin = board.D19
                elif board.board_id == "adafruit_kb2040":
                    PyDOS_HW.sndPin = board.D3
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

            if "NEOPIXEL" in dir(board):
                PyDOS_HW.neoPixel = board.NEOPIXEL


    def quietSnd(self):

        if implementation.name.upper() == "CIRCUITPYTHON":
            if PyDOS_HW.sndPin:
                PyDOS_HW.sndGPIO = digitalio.DigitalInOut(PyDOS_HW.sndPin)
                #PyDOS_HW.sndGPIO.direction = digitalio.Direction.OUTPUT
        return

    def I2C():

        if implementation.name.upper() == "CIRCUITPYTHON":

            if board.board_id == "cytron_maker_pi_rp2040":
                if not PyDOS_HW._I2C:
                    # Grove #2, GP3 & GP2
                    PyDOS_HW._I2C = busio.I2C(board.GP3, board.GP2)
            else:
                if 'I2C_POWER_INVERTED' in dir(board) and not PyDOS_HW._I2C_power:
                    PyDOS_HW._I2C_power = digitalio.DigitalInOut(board.I2C_POWER_INVERTED)
                    PyDOS_HW._I2C_power.direction = digitalio.Direction.OUTPUT
                    PyDOS_HW._I2C_power.value = False

                if 'STEMMA_I2C' in dir(board) and not PyDOS_HW._I2C:
                    PyDOS_HW._I2C = board.STEMMA_I2C()
                elif 'I2C' in dir(board) and not PyDOS_HW._I2C:
                    PyDOS_HW._I2C = board.I2C()
                elif not PyDOS_HW._I2C:
                    if "SCL" not in dir(board):
                        if board.board_id == "raspberry_pi_pico":
                            PyDOS_HW._I2C = busio.I2C(board.GP3, board.GP2)
                        elif board.board_id == 'espressif_esp32s3_devkitc_1_n8r2':
                            PyDOS_HW._I2C = busio.I2C(board.IO7, board.IO6)
                    else:
                        PyDOS_HW._I2C = busio.I2C(board.SCL, board.SDA)
        elif implementation.name.upper() == "MICROPYTHON":
            if not PyDOS_HW._I2C:
                if uname().machine == 'Arduino Nano RP2040 Connect with RP2040':
                    PyDOS_HW._I2C = m_I2C(0,scl=Pin(PyDOS_HW.SCL),sda=Pin(PyDOS_HW.SDA))
                else:
                    PyDOS_HW._I2C = m_I2C(1,scl=Pin(PyDOS_HW.SCL),sda=Pin(PyDOS_HW.SDA))

        return PyDOS_HW._I2C


    def SD_CSdeinit():
        if implementation.name.upper() == "CIRCUITPYTHON":
            PyDOS_HW.SD_CS.deinit()
            PyDOS_HW.SD_CS = None


    def SPI():
        if implementation.name.upper() == "CIRCUITPYTHON":
            if PyDOS_HW.SD_CS == None:
                if "SD_CS" in dir(board):
                    PyDOS_HW.SD_CS = digitalio.DigitalInOut(board.SD_CS)
                else:
                    PyDOS_HW.SD_CS = digitalio.DigitalInOut(board.D5)

            if 'SPI' in dir(board) and not PyDOS_HW._SPI:
                PyDOS_HW._SPI = board.SPI()
            elif not PyDOS_HW._SPI:
                if 'SCK' in dir(board):
                    if 'MOSI' in dir(board):
                        PyDOS_HW._SPI = busio.SPI(board.SCK, board.MOSI, board.MISO)
                    elif 'COPI' in dir(board):
                        PyDOS_HW._SPI = busio.SPI(board.SCK, board.COPI, board.CIPO)

        return PyDOS_HW._SPI

    def SD_SPI():
        if implementation.name.upper() == "CIRCUITPYTHON":
            if PyDOS_HW.SD_CS == None:
                if "SD_CS" in dir(board):
                    PyDOS_HW.SD_CS = digitalio.DigitalInOut(board.SD_CS)
                else:
                    PyDOS_HW.SD_CS = digitalio.DigitalInOut(board.D5)

            if 'SD_SPI' in dir(board) and not PyDOS_HW._SD_SPI:
                PyDOS_HW._SD_SPI = board.SD_SPI()
            elif not PyDOS_HW._SD_SPI:
                if 'SD_SCK' in dir(board):
                    if 'SD_MOSI' in dir(board):
                        PyDOS_HW._SD_SPI = busio.SPI(board.SD_SCK, board.SD_MOSI, board.SD_MISO)
                    elif 'SD_COPI' in dir(board):
                        PyDOS_HW._SD_SPI = busio.SPI(board.SD_SCK, board.SD_COPI, board.SD_CIPO)
                else:
                    PyDOS_HW._SD_SPI = PyDOS_HW.SPI()

        return PyDOS_HW._SD_SPI


Pydos_hw = PyDOS_HW()
sndPin = Pydos_hw.sndPin
sndGPIO = Pydos_hw.sndGPIO
neoPixel = Pydos_hw.neoPixel
