# PyDOS Board Configuration for 'Banana Pi PicoW-S3'

import board

Pydos_pins = {
    'sndPin' : (board.GP12,"GP12"),
    'SCL'    : (board.GP5,"GP5"),
    'SDA'    : (board.GP4,"GP4"),
    'SCK'    : [(board.GP18,"GP18")],
    'MOSI'   : [(board.GP19,"GP19")],
    'MISO'   : [(board.GP16,"GP16")],
    'CS'     : [(board.GP6,"GP6")]
}
