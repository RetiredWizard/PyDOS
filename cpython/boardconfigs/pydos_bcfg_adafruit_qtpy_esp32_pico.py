# PyDOS Board Configuration for 'adafruit_qtpy_esp32_pico'

import board

Pydos_pins = {
    'sndPin' : (board.A0,"A0"),
    'neoPixel' : (board.NEOPIXEL,"NEOPIXEL"),
    'neoPixel_Pow' : (board.NEOPIXEL_POWER,"NEOPIXEL_POWER"),
    'SCL' : (board.SCL,"SCL"),
    'SDA' : (board.SDA,"SDA"),
    'SCK' : [(board.SCK,"SCK")],
    'MOSI' : [(board.MOSI,"MOSI")],
    'MISO' : [(board.MISO,"MISO")],
    'CS' : [(board.A3,"A3")]
}
