# PyDOS Board Configuration for 'Adafruit QT Py RP2040 with RP2040'

Pydos_pins = {
    'sndPin' : (26,"A3"),
    'neoPixel' : (12,"12"),
    'neoPixel_Pow' : (11,"11"),
    'I2C_NUM' : (1,"STEMMA_I2C"),  # 0 = machine.I2C(0,SCL=25,SDA=24)
    'SPI_NUM' : [(0,"")],
    'SCL' : (25,"SCL"),
    'SDA' : (24,"SDA"),
    'SCK' : [(6,"SCK")],
    'MOSI' : [(3,"MO")],
    'MISO' : [(4,"MI")],
    'CS' : [(27,"A2")]
}
