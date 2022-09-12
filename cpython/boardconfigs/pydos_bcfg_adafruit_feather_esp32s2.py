# PyDOS Board Configuration for 'adafruit_feather_esp32s2'

import board

Pydos_pins = {
    'sndPin' : (board.D12,"GPIO12 D12"),
    'neoPixel' : (board.NEOPIXEL,None),
    'SCL' : (board.SCL,"GPIO4 SCL"),
    'SDA' : (board.SDA,"GPIO3 SDA"),
    'SCK' : (board.SCK,"GPIO36 SCK"),
    'MOSI' : (board.MOSI,"GPIO35 MO"),
    'MISO' : (board.MISO,"GPIO37 MI"),
    'SD_CS' : (board.D5,"GPIO5 D5")
}
