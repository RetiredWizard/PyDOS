# PyDOS Board Configuration for 'adafruit_feather_huzzah32'

import board

Pydos_pins = {
    'sndPin' : (board.D12,"D12 GPIO12"),
    'neoPixel' : (board.NEOPIXEL,None),
    'SCL' : (board.SCL,"SCL GPIO22"),
    'SDA' : (board.SDA,"SDA GPIO23"),
    'SCK' : (board.SCK,"SCK GPIO5"),
    'MOSI' : (board.MOSI,"MOSI GPIO18"),
    'MISO' : (board.MISO,"MISO GPIO19"),
    'CS' : (board.D21,"D21 GPI21")
}
