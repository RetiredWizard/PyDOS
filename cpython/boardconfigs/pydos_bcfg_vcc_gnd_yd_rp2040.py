# PyDOS Board Configuration for 'raspberry_pi_pico'

import board

Pydos_pins = {
    'sndPin' : (board.GP12,"GP12"),
    'led'    : (board.LED,"LED, GP25"),
    'neoPixel' : (board.NEOPIXEL,"NEOPIXEL"),
    'SCL'    : (board.GP9,"GP9"),
    'SDA'    : (board.GP8,"GP8"),
    'SCK'    : [(board.GP18,"GP18")],
    'MOSI'   : [(board.GP19,"GP19")],
    'MISO'   : [(board.GP16,"GP16")],
    'CS'     : [(board.GP6,"GP6")]
}
