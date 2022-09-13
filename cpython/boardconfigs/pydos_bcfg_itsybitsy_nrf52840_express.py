# PyDOS Board Configuration for 'itsybitsy_nrf52840_express'

import board

Pydos_pins = {
    'sndPin' : (board.D12,"GPIO10 D12"),
    'dotStar_Clock' : (board.DOTSTAR_CLOCK,None),
    'dotStar_Data' : (board.DOTSTAR_DATA,None),
    'SCL' : (board.SCL,"D22 SCL"),
    'SDA' : (board.SDA,"D21 SDA"),
    'SCK' : (board.SCK,"D25 SCK"),
    'MOSI' : (board.MOSI,"D24 MO"),
    'MISO' : (board.MISO,"D23 MI"),
    'CS' : (board.D9,"D9")
}
