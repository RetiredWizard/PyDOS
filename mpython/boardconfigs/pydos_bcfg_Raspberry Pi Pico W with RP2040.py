# PyDOS Board Configuration for 'Raspberry Pi Pico W with RP2040'

Pydos_pins = {
    'sndPin' : (12,"GP12"),
    'led' : ('LED',"LED"),
    'I2C_NUM' : (0,"machine.I2C(0), scl=GP5,sda=GP4"),
    'SCL' : (5,"SCL GP5"),
    'SDA' : (4,"SDA GP4"),
    'SPI_NUM' : [(0,"machine.SPI(0,...)")],
    'SCK' : [(18,"GP18")],
    'MOSI' : [(19,"GP19")],
    'MISO' : [(16,"GP16")],
    'CS' : [(6,"GP6")]
}
