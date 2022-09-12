# PyDOS Board Configuration for 'adafruit_feather_rp2040'

import board

Pydos_pins = {
    'sndPin' : (board.D12,"D12 GPIO12"),
    'neoPixel' : (board.NEOPIXEL,None),
    'SCL' : (board.SCL,"SCL GPIO3"),
    'SDA' : (board.SDA,"SDA GPIO2"),
    'SCK' : (board.SCK,"SCK GPIO18"),
    'MOSI' : (board.MOSI,"MOSI GPIO19"),
    'MISO' : (board.MISO,"MISO GPIO20"),
    'SD_CS' : (board.D5,"D5 GPIO7")
}
