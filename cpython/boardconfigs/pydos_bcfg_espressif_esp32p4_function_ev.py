# PyDOS Board Configuration for 'makerfabs_tft7'

import board

Pydos_pins = {
    'SDIO_CLK'   : (board.IO43,"IO43"),
    'SDIO_CMD'   : (board.IO44,"IO44"),
    'SDIO_DPINS' : ([board.IO39],"[IO39]")
}
