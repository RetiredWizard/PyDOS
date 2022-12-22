# PyDOS Board Configuration for 'adafruit_kb2040'

import board

Pydos_pins = {
    'sndPin' : (board.A0,"GPIO26 A0"),
    'neoPixel' : (board.NEOPIXEL,None),
    'SCL' : (board.SCL,"GPIO13 SCL"),
    'SDA' : (board.SDA,"GPIO12 SDA"),
    'SCK' : [(board.SCK,"GPIO18 SCK")],
    'MOSI' : [(board.MOSI,"GPIO19 MO")],
    'MISO' : [(board.MISO,"GPIO20 MI")],
    'CS' : [(board.D9,"GPIO9 D9")]
}
