# PyDOS Board Configuration for 'sparkfun_nrf52840_mini'

import board

Pydos_pins = {
    'sndPin' : (board.A3,"A3 GPIO5"),
    'SCL' : (board.SCL,"SCL GPIO11"),
    'SDA' : (board.SDA,"SDA GPIO8"),
    'SCK' : (board.SCK,"SCK D13 A6 GPIO30"),
    'MOSI' : (board.MOSI,"MOSI D11 A1 GPIO3"),
    'MISO' : (board.MISO,"MISO D12 A7 GPIO31"),
    'CS' : (board.D9,"D9 GPIO10")
}
