# PyDOS Board Configuration for 'raspberrypi_zero2w'

import board

Pydos_pins = {
    'SCL' : (board.SCL,"GPIO3 SCL"),
    'SDA' : (board.SDA,"GPIO2 SDA"),
    'SCK' : (board.SCK,"GPIO11 SCLK"),
    'MOSI' : (board.MOSI,"GPIO10 MOSI"),
    'MISO' : (board.MISO,"GPIO9 MISO"),
    'CS' : (board.D5,"GPIO5 D5")
}
