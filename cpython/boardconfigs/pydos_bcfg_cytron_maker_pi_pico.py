# PyDOS Board Configuration for 'raspberry_pi_pico with Cytron Maker Pi Pico'

import cyt_mpp_board as board

Pydos_pins = {
    'sndPin' : (board.SNDPIN,"GP18 Onboard Buzzer"),
    'neoPixel' : (board.NEOPIXEL,None),
    'SCL' : (board.GP3,"GP3 GROVE#2"),
    'SDA' : (board.GP2,"GP2 GROVE#2"),
    'SD_SCK' : (board.SCK,"GP10 Onboard SD"),
    'SD_MOSI' : (board.MOSI,"GP11 Onboard SD"),
    'SD_MISO' : (board.MISO,"GP12 Onboard SD"),
    'SD_CS' : (board.GP15,"GP15 Onboard SD")
}
