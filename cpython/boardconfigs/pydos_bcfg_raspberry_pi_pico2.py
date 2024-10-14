# PyDOS Board Configuration for 'raspberry_pi_pico2'

import board

Pydos_pins = {
    'sndPin' : (board.GP6,"GP6"),
    'SCL'    : (board.GP5,"GP5"),
    'SDA'    : (board.GP4,"GP4"),
    'SCK'    : [(board.GP2,"GP2")],
    'MOSI'   : [(board.GP3,"GP3 TX")],
    'MISO'   : [(board.GP4,"GP4 RX")],
    'CS'     : [(board.GP5,"GP5")]
}
