# PyDOS Board Configuration for 'lilygo_tdeck'

import board

Pydos_pins = {
    'i2s_BitClock'   : (board.SPEAKER_SCK,"board.SPEAKER_SCK IO7"),
    'i2s_WordSelect' : (board.SPEAKER_WS,"board.SPEAKER_WS IO5"),
    'i2s_Data'       : (board.SPEAKER_DOUT,"board.SPEAKER_DOUT IO6"),
    'SCL' : (board.SCL,"SCL IO8"),
    'SDA' : (board.SDA,"SDA IO18"),
    'SCK' : [(board.SCK,"SCK IO40")],
    'MOSI' : [(board.MOSI,"MOSI IO41")],
    'MISO' : [(board.MISO,"MISO IO38")],
    'CS' : [(board.SDCARD_CS,"SDCARD_CS IO39")]
}
