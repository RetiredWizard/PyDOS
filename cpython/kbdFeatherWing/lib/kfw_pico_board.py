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

GP0 = board.GP0
GP1 = board.GP1
GP2 = board.GP2
GP3 = board.GP3
GP4 = board.GP4
GP5 = board.GP5
GP6 = board.GP6
GP7 = board.GP7
GP8 = board.GP8
GP9 = board.GP9
GP10 = board.GP10
GP11 = board.GP11
GP12 = board.GP12
GP13 = board.GP13
GP14 = board.GP14
GP15 = board.GP15
GP16 = board.GP16
GP17 = board.GP17
GP18 = board.GP18
GP19 = board.GP19
GP20 = board.GP20
GP21 = board.GP21
GP22 = board.GP22
GP23 = board.GP23
GP24 = board.GP24
GP25 = board.GP25
GP26 = board.GP26
GP27 = board.GP27
GP28 = board.GP28
GP26_A0 = board.GP26_A0
GP27_A1 = board.GP27_A1
GP28_A2 = board.GP28_A2
LED = board.LED
NEOPIXEL = D11
SMPS_MODE = board.SMPS_MODE
VBUS_SENSE = board.VBUS_SENSE
VOLTAGE_MONITOR = board.VOLTAGE_MONITOR
board_id = board.board_id

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
