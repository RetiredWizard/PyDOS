# PyDOS Board Configuration for 'unexpectedmaker_feathers3'

import board

Pydos_pins = {
    'sndPin' : (board.IO10,"IO10"),
    'neoPixel' : (board.NEOPIXEL,"NEOPIXEL"),
    'SCL' : (board.SCL,"SCL IO9"),
    'SDA' : (board.SDA,"SDA IO8"),
    'SCK' : [(board.SCK,"SCK IO36")],
    'MOSI' : [(board.MOSI,"MOSI IO35 MO")],
    'MISO' : [(board.MISO,"MISO IO37 MI")],
    'CS' : [(board.D5,"D5 IO33")]
}
