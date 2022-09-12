# PyDOS Board Configuration for 'lilygo_ttgo_t8_s2_st7789'

import board

Pydos_pins = {
    'sndPin' : (board.IO2,"IO2"),
    'SCL' : (board.IO4,"IO4"),
    'SDA' : (board.IO3,"IO3"),
    'SD_SCK' : (board.SD_CLK,"SD_CLK IO12"),
    'SD_MOSI' : (board.SD_MOSI,"SD_MOSI IO11"),
    'SD_MISO' : (board.SD_MISO,"SD_MISO IO13"),
    'SD_CS' : (board.SD_CS,"SD_CS IO15 Internal"),
    'SCK' : (board.IO8,"IO8"),
    'MOSI' : (board.IO7,"IO7"),
    'MISO' : (board.IO6,"IO6"),
    'CS' : (board.IO5,"IO5")
}
