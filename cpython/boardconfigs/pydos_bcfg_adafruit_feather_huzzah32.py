# PyDOS Board Configuration for 'adafruit_feather_huzzah32'

import board

Pydos_pins = {
    'sndPin' : (board.D12,"D12 D12"),
    'SCL' : (board.SCL,"SCL V1:D22 V2:D20"),
    'SDA' : (board.SDA,"SDA V1:D23 V2:D22"),
    'SCK' : [(board.SCK,"SCK D5")],
    'MOSI' : [(board.MOSI,"MOSI V1:D18 V2:D19")],
    'MISO' : [(board.MISO,"MISO V1:D19 V2:D21")],
    'CS' : [(board.D14,"D14")]
}
