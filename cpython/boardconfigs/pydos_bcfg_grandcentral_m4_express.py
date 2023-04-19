# PyDOS Board Configuration for 'Adafruit Grand Central M4 Express with samd51p20'

import board

Pydos_pins = {
    'sndPin' : (board.D8,"D8"),
    'SCL' : (board.SCL,"SCL D21"),
    'SDA' : (board.SDA,"SDA D20"),
    'SCK' : [(board.SD_SCK,"SD_SCK PB27 Internal"), (board.SCK,"SCK D52")],
    'MOSI' : [(board.SD_MOSI,"SD_MOSI PB26 Internal"),(board.MOSI,"MOSI D51")],
    'MISO' : [(board.SD_MISO,"SD_MISO PB29 Internal"), (board.MISO,"CIPO D50")],
    'CS' : [(board.SD_CS,"SD_CS PB28 Internal"), (board.SS,"SS D53")]
}
