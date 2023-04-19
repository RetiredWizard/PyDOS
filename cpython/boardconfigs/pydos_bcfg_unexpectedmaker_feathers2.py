# PyDOS Board Configuration for 'unexpectedmaker_feathers2'

import board

Pydos_pins = {
    'sndPin' : (board.D12,"D12 IO10"),
    'dotStar_Clock' : (board.APA102_SCK,"APA102_SCK"),
    'dotStar_Data' : (board.APA102_MOSI,"APA102_MOSI"),
    'SCL' : (board.SCL,"SCL IO9"),
    'SDA' : (board.SDA,"SDA IO8"),
    'SCK' : [(board.SCK,"SCK IO36")],
    'MOSI' : [(board.MOSI,"MOSI IO35 SDO")],
    'MISO' : [(board.MISO,"MISO IO37 SDI")],
    'CS' : [(board.D20,"D20 IO33")]
}
