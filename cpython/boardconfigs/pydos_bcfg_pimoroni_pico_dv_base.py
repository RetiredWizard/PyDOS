# PyDOS Board Configuration for 'Pimoroni PICO dv'

import board

Pydos_pins = {
    'i2s_BitClock'   : (board.I2S_BIT_CLOCK,"board.I2S_BIT_CLOCK, GP27"),
    'i2s_WordSelect' : (board.I2S_WORD_SELECT,"board.I2S_WORD_SELECT, GP28"),
    'i2s_Data'       : (board.I2S_DATA,"board.IS2_DATA, GP26"),
    'SCL'    : (board.GP1,"GP1"),
    'SDA'    : (board.GP0,"GP0"),
    'SCK'    : [(board.SD_SCK,"SD_SCK")],
    'MOSI'   : [(board.SD_MOSI,"SD_MOSI")],
    'MISO'   : [(board.SD_MISO,"SD_MISO")],
    'CS'     : [(board.SD_CS,"SD_CS")]
}
