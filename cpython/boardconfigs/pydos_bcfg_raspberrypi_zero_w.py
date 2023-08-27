# PyDOS Board Configuration for 'raspberrypi_zero2w'

import board
import microcontroller

Pydos_pins = {
    'led' : (microcontroller.pin.GPIO47,"GPIO47"),
    # 'sndPin' : (board.D6,"D6 GPIO6"), # pwmio not currently supported
    'SCL' : (board.SCL,"SCL D3 GPIO3"),
    'SDA' : (board.SDA,"SDA D2 GPIO2"),
    'SCK' : [(board.SCK,"SCK D11 GPIO11 SCLK")],
    'MOSI' : [(board.MOSI,"MOSI D10 GPIO10")],
    'MISO' : [(board.MISO,"MISO D9 GPIO9")],
    'CS' : [(board.D5,"D5 GPIO5")]
}
