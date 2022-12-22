# PyDOS Board Configuration for 'unexpectedmaker_tinypico'

import board

Pydos_pins = {
    'sndPin' : (board.IO27,"IO27"),
    'SCL' : (board.SCL,"SCL IO22"),
    'SDA' : (board.SDA,"SDA IO21"),
    'SCK' : [(board.SCK,"SCK IO18")],
    'MOSI' : [(board.MOSI,"MOSI IO23")],
    'MISO' : [(board.MISO,"MISO IO19")],
    'CS' : [(board.IO5,"SS IO5")],
    'dotStar_Clock' : (board.APA102_SCK,"APA102_SCK CLK internal GPIO12"),
    'dotStar_Data' : (board.APA102_MOSI,"APA102_MOSI DATA internal GPIO2"),
    'dotStar_Pow' : (board.APA102_PWR,"APA102_PWR internal PWR GPIO13"),
}
