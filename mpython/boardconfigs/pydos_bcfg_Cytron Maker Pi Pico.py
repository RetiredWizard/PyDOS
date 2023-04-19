# PyDOS Board Configuration for 'Raspberry Pi Pico with RP2040 with Cytron Maker Pi Pico'

Pydos_pins = {
    'sndPin' : (18,"GP18 Onboard Buzzer"),
    'led' : (25,"GP25"),
    'neoPixel' : (28,"GP28"),
    'I2C_NUM' : (0,"machine.I2C(0), scl=GP5,sda=GP4"),
    'SCL' : (5,"GP5 GROVE#3"),
    'SDA' : (4,"GP4 GROVE#3"),
    'SPI_NUM' : [(1,"machine.SPI(1,...")],
    'SCK' : [(10,"GP10 Onboard SD")],
    'MOSI' : [(11,"GP11 Onboard SD")],
    'MISO' : [(12,"GP12 Onboard SD")],
    'CS' : [(15,"GP15 Onboard SD")]
}
