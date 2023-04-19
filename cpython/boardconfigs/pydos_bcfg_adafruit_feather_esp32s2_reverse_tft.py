# PyDOS Board Configuration for 'adafruit_feather_esp32s2_reverse_tft'

import board

Pydos_pins = {
    'sndPin' : (board.D12,"D12 GPIO12"),
    'neoPixel' : (board.NEOPIXEL,"NEOPIXEL"),
    'SCL' : (board.SCL,"SCL GPIO4"),
    'SDA' : (board.SDA,"SDA GPIO3"),
    'SCK' : [(board.SCK,"SCK GPIO36")],
    'MOSI' : [(board.MOSI,"MOSI GPIO35 MO")],
    'MISO' : [(board.MISO,"MISO GPIO37 MI")],
    'CS' : [(board.D5,"D5 GPIO5")]
}
