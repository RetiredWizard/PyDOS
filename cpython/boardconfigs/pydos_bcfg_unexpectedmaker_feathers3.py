# PyDOS Board Configuration for 'unexpectedmaker_feathers3'

import board

Pydos_pins = {
    'sndPin' : (board.IO10,"IO10"),
    'neoPixel' : (board.NEOPIXEL,None),
    'SCL' : (board.SCL,"SCL IO9"),
    'SDA' : (board.SDA,"SDA IO8"),
    'SCK' : (board.SCK,"SCK IO36"),
    'MOSI' : (board.MOSI,"MO IO35"),
    'MISO' : (board.MISO,"MI IO37"),
    'CS' : (board.D5,"D5 IO33")
}
