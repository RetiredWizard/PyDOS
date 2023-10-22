# PyDOS Board Configuration for 'espressif_esp32s3_devkitc_1_n8r2'

import board

Pydos_pins = {
    'sndPin' : (board.IO10,"IO10"),
    'neoPixel' : (board.NEOPIXEL,"NEOPIXEL"),
    'SCL' : (board.IO9,"IO9"),
    'SDA' : (board.IO8,"IO8"),
    'SCK' : [(board.IO12,"IO12")],
    'MOSI' : [(board.IO11,"IO11")],
    'MISO' : [(board.IO13,"IO13")],
    'CS' : [(board.IO7,"IO7")]
}
