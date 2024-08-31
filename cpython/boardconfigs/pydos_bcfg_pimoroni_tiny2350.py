# PyDOS Board Configuration for 'pimoroni_tiny235040'

import board

Pydos_pins = {
    'sndPin'    : (board.A3,"A3"),
    'SCL'       : (board.SCL,"SCL GP13"),
    'SDA'       : (board.SDA,"SDA GP12"),
    'SCK'       : [(board.GP2,"SCK GP2")],
    'MOSI'      : [(board.GP3,"MOSI TX GP3")],
    'MISO'      : [(board.GP0,"MISO RX GP0")],
    'CS'        : [(board.GP1,"CS GP1")],
    'LED_RED'   : (board.LED_R,"LED_R"),
    'LED_GREEN' : (board.LED_G,"LED_G"),
    'LED_BLUE'  : (board.LED_B,"LED_B")
}
