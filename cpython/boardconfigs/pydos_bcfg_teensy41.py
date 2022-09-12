# PyDOS Board Configuration for 'teensy41'

import board

Pydos_pins = {
    'sndPin' : (board.D36,"D36"),
    'SCL' : (board.SCL,"SCL D19 A5"),
    'SDA' : (board.SDA,"SDA D18 A4"),
    'SD_SCK' : (board.CLK,"CLK D44 Internal"),
    'SD_MOSI' : (board.CMD,"CMD D45 Internal"),
    'SD_MISO' : (board.DAT0,"DAT0 D43 Internal"),
    'SD_CS' : (board.DAT3,"DAT3 D46 Internal"),
    'SCK' : (board.SCK,"SCK D13"),
    'MOSI' : (board.MOSI,"MOSI D11"),
    'MISO' : (board.MISO,"MISO D12"),
    'CS' : (board.D10,"D10")
}
