# PyDOS Board Configuration for 'sparkfun_thingplus_matter_mgm240p_brd2704a'

import board

Pydos_pins = {
    'sndPin' : (board.PC7,"PC7 C7"),
    'SCL' : (board.SCL,"SCL PB3 B3"),
    'SDA' : (board.SDA,"SDA PB4 B4"),
    'SCK' : [(board.SCK,"SCK PC2 C2"), (board.SCK,"SCK PC2 C2")],
    'MOSI' : [(board.MOSI,"MOSI C3 PICO"),(board.MOSI,"MOSI C3 PICO")],
    'MISO' : [(board.MISO,"MISO C6 POCI"), (board.MISO,"MISO C6 POCI")],
    'CS' : [(board.SD_CS,"SD_CS Internal"), (board.PD0,"PD0 D0")]
}
