import board
import busio


_SPI = None
_UART = None
_I2C = None


A0 = board.A0
A1 = board.A1
A2 = board.A2
A3 = board.A3

SCK = board.GP10
COPI = board.GP11
MOSI = board.GP11
CIPO = board.GP12
MISO = board.GP12

NEOPIXEL = board.GP28
SNDPIN = board.GP18

D5 = board.GP15

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
SMPS_MODE = board.SMPS_MODE
VBUS_SENSE = board.VBUS_SENSE
VOLTAGE_MONITOR = board.VOLTAGE_MONITOR
board_id = board.board_id

def SPI():
    global _SPI

    if not _SPI:
        _SPI = busio.SPI(SCK, COPI, CIPO)

    return _SPI

def I2C():
    global _I2C

    if not _I2C:
        _I2C = busio.I2C(GP3, GP2)

    return _I2C

