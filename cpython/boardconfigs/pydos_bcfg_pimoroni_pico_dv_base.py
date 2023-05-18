# PyDOS Board Configuration for 'Pimoroni PICO dv'

import board

Pydos_pins = {
    'SCL'    : (board.GP1,"GP1"),
    'SDA'    : (board.GP0,"GP0"),
    'SCK'    : [(board.SD_SCK,"SD_SCK")],
    'MOSI'   : [(board.SD_MOSI,"SD_MOSI")],
    'MISO'   : [(board.SD_MISO,"SD_MISO")],
    'CS'     : [(board.SD_CS,"SD_CS")]
}
