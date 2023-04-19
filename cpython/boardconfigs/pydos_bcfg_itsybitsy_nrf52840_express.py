# PyDOS Board Configuration for 'itsybitsy_nrf52840_express'

import board

Pydos_pins = {
    'sndPin' : (board.D12,"D12 GPIO10"),
    'dotStar_Clock' : (board.DOTSTAR_CLOCK,"DOTSTAR_CLOCK"),
    'dotStar_Data' : (board.DOTSTAR_DATA,"DOTSTAR_DATA"),
    'SCL' : (board.SCL,"SCL D22"),
    'SDA' : (board.SDA,"SDA D21"),
    'SCK' : [(board.SCK,"SCK D25")],
    'MOSI' : [(board.MOSI,"MOSI D24 MO")],
    'MISO' : [(board.MISO,"MISO D23 MI")],
    'CS' : [(board.D9,"D9")]
}
