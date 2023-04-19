# PyDOS Board Configuration for 'cytron_maker_pi_rp2040'

import board

Pydos_pins = {
    'sndPin' : (board.BUZZER,"BUZZER"),
    'neoPixel' : (board.NEOPIXEL,"NEOPIXEL"),
    'SCL' : (board.GP5,"GP5 GROVE#3"),
    'SDA' : (board.GP4,"GP4 GROVE#3"),
    'SCK' : [(board.GP12,"GP12 SERVO HEADER")],
    'MOSI' : [(board.GP13,"GP13 SERVO HEADER")],
    'MISO' : [(board.GP14,"GP14 SERVO HEADER")],
    'CS' : [(board.GP15,"GP15 SERVO HEADER")]
}
