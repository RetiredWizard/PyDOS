# PyDOS Board Configuration for 'espressif_esp32s3_devkitc_1_n8r2'

import board

Pydos_pins = {
    'sndPin' : (board.IO10,"IO10"),
    'neoPixel' : (board.NEOPIXEL,None),
    'SCL' : (board.IO7,"IO7"),
    'SDA' : (board.IO6,"IO6"),
    'SCK' : (board.IO36,"IO36"),
    'MOSI' : (board.IO35,"IO35"),
    'MISO' : (board.IO37,"IO37"),
    'CS' : (board.IO9,"IO9")
}
