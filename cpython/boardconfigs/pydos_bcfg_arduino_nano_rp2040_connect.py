# PyDOS Board Configuration for 'arduino_nano_rp2040_connect'

import board

Pydos_pins = {
    'sndPin' : (board.A3,"GPIO29 A3"),
    'led' : (board.D13,"GPIO6 D13"),
    'SCL' : (board.SCL,"GPIO13 A5"),
    'SDA' : (board.SDA,"GPIO12 A4"),
    'SCK' : (board.SCK,"GPIO6 D13"),
    'MOSI' : (board.MOSI,"GPIO7 D11"),
    'MISO' : (board.MISO,"GPIO4 D12"),
    'SD_CS' : (board.D10,"GPIO5 D10")
}
