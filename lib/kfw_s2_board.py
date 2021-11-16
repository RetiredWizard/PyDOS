import board
import busio


_SPI = None
_UART = None
_I2C = None


A0 = board.A0
A1 = board.A1
A2 = board.A2
A3 = board.A3
A4 = board.A4
A5 = board.A5
SCK = board.SCK
COPI = board.MOSI
MOSI = board.MOSI
CIPO = board.MISO
MISO = board.MISO
RX = board.RX
TX = board.TX
D14 = board.D4
MISC = board.D4
SCL = board.SCL
SDA = board.SDA
D5 = board.D20
D6 = board.D21
D9 = board.D5
D10 = board.D6
D11 = board.D9
D12 = board.D12
D13 = board.D13


def SPI():
    global _SPI

    if not _SPI:
        _SPI = board.SPI()

    return _SPI


def UART():
    global _UART

    if not _UART:
        _UART = board.UART()

    return _UART


def I2C():
    global _I2C

    if not _I2C:
        _I2C = board.I2C()

    return _I2C

