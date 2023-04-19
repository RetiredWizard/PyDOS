# PyDOS Board Configuration for 'teensy41'

import board

Pydos_pins = {
    'sndPin' : (board.D36,"D36"),
    'SCL' : (board.SCL,"SCL D19 A5"),
    'SDA' : (board.SDA,"SDA D18 A4"),
    'SCK' : [(board.CLK,"CLK D44 Internal"), (board.SCK,"SCK D13")],
    'MOSI' : [(board.CMD,"CMD D45 Internal"), (board.MOSI,"MOSI D11")],
    'MISO' : [(board.DAT0,"DAT0 D43 Internal"), (board.MISO,"MISO D12")],
    'CS' : [(board.DAT3,"DAT3 D46 Internal"), (board.D10,"D10")]
}
