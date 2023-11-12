# PyDOS Board Configuration for 'lilygo_tdeck'

import board

Pydos_pins = {
    'SCL' : (board.SCL,"SCL IO8"),
    'SDA' : (board.SDA,"SDA IO18"),
    'SCK' : [(board.SCK,"SCK IO40")],
    'MOSI' : [(board.MOSI,"MOSI IO41")],
    'MISO' : [(board.MISO,"MISO IO38")],
    'CS' : [(board.SDCARD_CS,"SDCARD_CS IO39")]
}
