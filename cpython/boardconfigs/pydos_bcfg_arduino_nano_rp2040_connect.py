# PyDOS Board Configuration for 'arduino_nano_rp2040_connect'

import board

Pydos_pins = {
    'sndPin' : (board.A3,"A3 GPIO29"),
    'led' : (board.D13,"D13 GPIO6"),
    'SCL' : (board.SCL,"SCL GPIO13 A5"),
    'SDA' : (board.SDA,"SDA GPIO12 A4"),
    'SCK' : [(board.SCK,"SCK GPIO6 D13")],
    'MOSI' : [(board.MOSI,"MOSI GPIO7 D11")],
    'MISO' : [(board.MISO,"MISO GPIO4 D12")],
    'CS' : [(board.D10,"D10 GPIO5")]
}
