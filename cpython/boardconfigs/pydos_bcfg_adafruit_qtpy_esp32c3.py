# PyDOS Board Configuration for 'adafruit_qtpy_esp32c3'

import board

Pydos_pins = {
    'sndPin' : (board.A0,"A0"),
    'neoPixel' : (board.NEOPIXEL,None),
    'SCL' : (board.SCL,"SCL"),
    'SDA' : (board.SDA,"SDA"),
    'SCK' : (board.SCK,"SCK"),
    'MOSI' : (board.MOSI,"MO"),
    'MISO' : (board.MISO,"MI"),
    'CS' : (board.A3,"A3")
}
