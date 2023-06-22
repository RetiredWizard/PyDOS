# PyDOS Board Configuration for Adafruit 'matrixportal_m4'

import board

Pydos_pins = {
    'sndPin' : (board.A2,"A2"),
    'neoPixel' : (board.NEOPIXEL,"NEOPIXEL"),
    'SCL' : (board.SCL,"SCL"),
    'SDA' : (board.SDA,"SDA"),
    'SCK' : [(board.SCK,"SCK")],
    'MOSI' : [(board.MOSI,"MOSI")],
    'MISO' : [(board.MISO,"MISO")],
    'CS' : [(board.A3,"A3")]
}
