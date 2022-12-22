# PyDOS Board Configuration for 'raspberry_pi_pico with Cytron Maker Pi Pico'

import cyt_mpp_board as board

Pydos_pins = {
    'sndPin' : (board.SNDPIN,"GP18 Onboard Buzzer"),
    'neoPixel' : (board.NEOPIXEL,None),
    'SCL' : (board.GP3,"GP3 GROVE#2"),
    'SDA' : (board.GP2,"GP2 GROVE#2"),
    'SCK' : [(board.SCK,"GP10 Onboard SD")],
    'MOSI' : [(board.MOSI,"GP11 Onboard SD")],
    'MISO' : [(board.MISO,"GP12 Onboard SD")],
    'CS' : [(board.GP15,"GP15 Onboard SD")]
}
