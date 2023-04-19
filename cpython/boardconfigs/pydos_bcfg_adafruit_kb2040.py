# PyDOS Board Configuration for 'adafruit_kb2040'

import board

Pydos_pins = {
    'sndPin' : (board.A0,"A0 GPIO26"),
    'neoPixel' : (board.NEOPIXEL,"NEOPIXEL"),
    'SCL' : (board.SCL,"SCL GPIO13"),
    'SDA' : (board.SDA,"SDA GPIO12"),
    'SCK' : [(board.SCK,"SCK GPIO18")],
    'MOSI' : [(board.MOSI,"MOSI GPIO19 MO")],
    'MISO' : [(board.MISO,"MISO GPIO20 MI")],
    'CS' : [(board.D9,"D9 GPIO9")]
}
