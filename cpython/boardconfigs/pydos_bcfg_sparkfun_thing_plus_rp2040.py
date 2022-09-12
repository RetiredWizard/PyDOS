# PyDOS Board Configuration for 'sparkfun_thing_plus_rp2040'

import board

Pydos_pins = {
    'sndPin' : (board.D17,"D17"),
    'neoPixel' : (board.NEOPIXEL,None),
    'SCL' : (board.SCL,"SCL D7 D23"),
    'SDA' : (board.SDA,"SDA D6"),
    'SD_SCK' : (board.SD_SCK,"SD_SCK GPIO14 Internal"),
    'SD_MOSI' : (board.SD_MOSI,"SD_MOSI GPIO15 Internal"),
    'SD_MISO' : (board.SD_MISO,"SD_MISO GPIO12 Internal"),
    'SD_CS' : (board.SD_CS,"SD_CS GPIO9 Internal"),
    'SCK' : (board.SCK,"SCK D2"),
    'MOSI' : (board.MOSI,"COPI D3"),
    'MISO' : (board.MISO,"CIPO D4"),
    'CS' : (board.D22,"D22")
}
