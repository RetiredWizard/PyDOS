# PyDOS Board Configuration for 'adafruit_qtpy_esp32_pico'

import board

Pydos_pins = {
    'sndPin' : (board.A3,"A3"),
    'neoPixel' : (board.NEOPIXEL,"NEOPIXEL"),
    'neoPixel_Pow' : (board.NEOPIXEL_POWER,"NEOPIXEL_POWER"),
    'SCL' : (board.SCL,"SCL A5"),
    'SDA' : (board.SDA,"SDA A4"),
    'SCK' : [(board.SCK,"SCK A8")],
    'MOSI' : [(board.MOSI,"MOSI A10")],
    'MISO' : [(board.MISO,"MISO A9")],
    'CS' : [(board.A2,"A2")]
}
