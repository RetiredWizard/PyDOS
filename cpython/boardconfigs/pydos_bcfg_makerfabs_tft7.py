# PyDOS Board Configuration for 'makerfabs_tft7'

import board

Pydos_pins = {
    'SCL'        : (board.SCL,"GPIO18 board.SCL"),
    'SDA'        : (board.SDA,"GPIO17 board.SDA"),
    'SDIO_CLK'   : (board.SDIO_CLK,"GPIO12 board.SDIO_CLK"),
    'SDIO_CMD'   : (board.SDIO_CMD,"GPIO11 board.SDIO_CMD"),
    'SDIO_DPINS' : ([board.SDIO_D0],"[GPIO13] [board.SDIO_D0]")
}
