import board
import busio


_SPI = None
_UART = None
_I2C = None


A0 = board.GP26
A1 = board.GP27
A2 = board.GP20
A3 = board.GP21
A4 = board.GP22
A5 = board.GP28
SCK = board.GP18
COPI = board.GP19
MOSI = board.GP19
CIPO = board.GP16
MISO = board.GP16
RX = board.GP1
TX = board.GP0
D14 = board.GP13
MISC = board.GP13
SCL = board.GP5
SDA = board.GP4
D5 = board.GP6
D6 = board.GP7
D9 = board.GP8
D10 = board.GP9
D11 = board.GP10
D12 = board.GP11
D13 = board.GP12


def SPI():
    global _SPI

    if not _SPI:
        _SPI = busio.SPI(SCK, COPI, CIPO)

    return _SPI


def UART():
    global _UART

    if not _UART:
        _UART = busio.UART(TX, RX)

    return _UART


def I2C():
    global _I2C

    if not _I2C:
        _I2C = busio.I2C(SCL, SDA)

    return _I2C
