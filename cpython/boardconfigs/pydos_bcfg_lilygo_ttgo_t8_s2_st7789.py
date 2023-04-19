# PyDOS Board Configuration for 'lilygo_ttgo_t8_s2_st7789'

import board

Pydos_pins = {
    'sndPin' : (board.IO2,"IO2"),
    'SCL' : (board.IO4,"IO4"),
    'SDA' : (board.IO3,"IO3"),
    'SCK' : [(board.SD_CLK,"SD_CLK IO12"), (board.SD_CLK,"SD_CLK IO12")],
    'MOSI' : [(board.SD_MOSI,"SD_MOSI IO11"), (board.SD_MOSI,"SD_MOSI IO11")],
    'MISO' : [(board.SD_MISO,"SD_MISO IO13"), (board.SD_MISO,"SD_MISO IO13")],
    'CS' : [(board.SD_CS,"SD_CS IO15 Internal"), (board.IO17,"IO17")]
}
