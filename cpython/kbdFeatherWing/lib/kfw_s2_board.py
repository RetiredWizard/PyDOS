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

A6 = board.A6
A7 = board.A7
A8 = board.A8
A9 = board.A9
A10 = board.A10
AMB = board.AMB
APA102_MOSI = board.APA102_MOSI
APA102_SCK = board.APA102_SCK
D0 = board.D0
D1 = board.D1
D4 = board.D4
D15 = board.D15
D16 = board.D16
D17 = board.D17
D18 = board.D18
D19 = board.D19
D20 = board.D20
D21 = board.D21
D23 = board.D23
D24 = board.D24
D25 = board.D25
DAC1 = board.DAC1
DAC2 = board.DAC2
IO0 = board.IO0
IO1 = board.IO1
IO3 = board.IO3
IO4 = board.IO4
IO5 = board.IO5
IO6 = board.IO6
IO7 = board.IO7
IO8 = board.IO8
IO9 = board.IO9
IO10 = board.IO10
IO11 = board.IO11
IO12 = board.IO12
IO14 = board.IO14
IO17 = board.IO17
IO18 = board.IO18
IO21 = board.IO21
IO33 = board.IO33
IO35 = board.IO35
IO36 = board.IO36
IO37 = board.IO37
IO38 = board.IO38
IO43 = board.IO43
IO44 = board.IO44
LDO2 = board.LDO2
LED = board.LED
board_id = board.board_id
NEOPIXEL = D11


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

