# PyDOS Board Configuration for 'adafruit_feather_rp2040_usb_host'

import board

Pydos_pins = {
    'led'    : (board.LED,"LED D13 GPIO13")
    'sndPin' : (board.D12,"D12 GPIO12"),
    'neoPixel' : (board.NEOPIXEL,"NEOPIXEL GPIO21"),
    'SCL' : (board.SCL,"SCL GPIO3"),
    'SDA' : (board.SDA,"SDA GPIO2"),
    'SCK' : [(board.SCK,"SCK GPIO14")],
    'MOSI' : [(board.MOSI,"MOSI GPIO15")],
    'MISO' : [(board.MISO,"MISO GPIO8")],
    'CS' : [(board.D5,"D5 GPIO5")]
}
