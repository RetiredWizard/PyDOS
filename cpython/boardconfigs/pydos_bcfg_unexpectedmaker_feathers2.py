# PyDOS Board Configuration for 'unexpectedmaker_feathers2'

import board

Pydos_pins = {
    'sndPin' : (board.D12,"IO10 D12"),
    'dotStar_Clock' : (board.APA102_SCK,None),
    'dotStar_Data' : (board.APA102_MOSI,None),
    'SCL' : (board.SCL,"IO9 SCL"),
    'SDA' : (board.SDA,"IO8 SDA"),
    'SCK' : (board.SCK,"IO36 SCK"),
    'MOSI' : (board.MOSI,"IO35 SDO"),
    'MISO' : (board.MISO,"IO37 SDI"),
    'CS' : (board.D20,"IO33 D20")
}
