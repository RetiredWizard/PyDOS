# PyDOS Board Configuration for 'adafruit_itsybitsy_rp2040'

import board

Pydos_pins = {
    'sndPin' : (board.D12,"D12 GPIO10"),
    'neoPixel' : (board.NEOPIXEL,"NEOPIXEL"),
    'SCL' : (board.SCL,"SCL GPIO3"),
    'SDA' : (board.SDA,"SDA GPIO2"),
    'SCK' : [(board.SCK,"SCK GPIO18")],
    'MOSI' : [(board.MOSI,"MOSI GPIO19 MO")],
    'MISO' : [(board.MISO,"MISO GPIO20 MI")],
    'CS' : [(board.D9,"D9 GPIO7")]
}
