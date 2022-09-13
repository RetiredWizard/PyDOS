# PyDOS Board Configuration for 'cytron_maker_pi_rp2040'

import board

Pydos_pins = {
    'sndPin' : (board.BUZZER,"board.BUZZER"),
    'neoPixel' : (board.NEOPIXEL,None),
    'SCL' : (board.GP3,"GP3 GROVE#2"),
    'SDA' : (board.GP2,"GP2 GROVE#2"),
    'SD_SCK' : (board.GP14,"GP14 SERVO HEADER"),
    'SD_MOSI' : (board.GP15,"GP15 SERVO HEADER"),
    'SD_MISO' : (board.GP12,"GP12 SERVO HEADER"),
    'SD_CS' : (board.GP5,"GP5 GROVE#3")
}
