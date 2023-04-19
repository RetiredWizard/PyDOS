# PyDOS Board Configuration for 'raspberry_pi_pico with Cytron Maker Pi Pico'

import cyt_mpp_board as board

Pydos_pins = {
    'sndPin' : (board.SNDPIN,"SNDPIN GP18 Onboard Buzzer"),
    'neoPixel' : (board.NEOPIXEL,"NEOPIXEL Onboard Neopixel"),
    'SCL' : (board.GP5,"GP5 GROVE#3"),
    'SDA' : (board.GP4,"GP4 GROVE#3"),
    'SCK' : [(board.SCK,"SCK GP10 Onboard SD")],
    'MOSI' : [(board.MOSI,"MOSI GP11 Onboard SD")],
    'MISO' : [(board.MISO,"MISO GP12 Onboard SD")],
    'CS' : [(board.GP15,"GP15 Onboard SD")]
}
