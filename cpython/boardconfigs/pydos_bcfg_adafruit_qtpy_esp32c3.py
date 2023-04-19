# PyDOS Board Configuration for 'adafruit_qtpy_esp32c3'

import board

Pydos_pins = {
    'sndPin' : (board.A3,"A3"),
    'neoPixel' : (board.NEOPIXEL,"NEOPIXEL"),
    'SCL' : (board.SCL,"SCL A5"),
    'SDA' : (board.SDA,"SDA A4"),
    'SCK' : [(board.SCK,"SCK A8")],
    'MOSI' : [(board.MOSI,"MOSI A10 MO")],
    'MISO' : [(board.MISO,"MISO A9 MI")],
    'CS' : [(board.A2,"A2")]
}
