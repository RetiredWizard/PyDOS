# PyDOS Board Configuration for 'adafruit_itsybitsy_rp2040'

import board

Pydos_pins = {
    'sndPin' : (board.D12,"GPIO10 D12"),
    'neoPixel' : (board.NEOPIXEL,None),
    'SCL' : (board.SCL,"GPIO3 SCL"),
    'SDA' : (board.SDA,"GPIO2 SDA"),
    'SCK' : (board.SCK,"GPIO18 SCK"),
    'MOSI' : (board.MOSI,"GPIO19 MO"),
    'MISO' : (board.MISO,"GPIO20 MI"),
    'CS' : (board.D9,"GPIO7 D9")
}
