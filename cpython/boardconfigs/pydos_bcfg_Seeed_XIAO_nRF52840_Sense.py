# PyDOS Board Configuration for 'XIAO nRF52840 Sense with NRF52840'

import board

Pydos_pins = {
    'sndPin' : (board.D3,"D3 A3 P0.29"),
    'LED_RED' : (board.LED_RED,"LED_RED P0.26"),
    'LED_GREEN' : (board.LED_GREEN,"LED_GREEN P0.30"),
    'LED_BLUE' : (board.LED_BLUE,"LED_BLUE P0.06"),
    'SCL' : (board.SCL,"SCL D5 A5 P0.05"),
    'SDA' : (board.SDA,"SDA D4 A4 P0.04"),
    'SCK' : [(board.SCK,"SCK D8 P1.13")],
    'MOSI' : [(board.MOSI,"MOSI D10 P1.15")],
    'MISO' : [(board.MISO,"MISO D9 P1.14")],
    'CS' : [(board.D2,"D2 A2 P0.28")]
}
