# PyDOS Board Configuration for 'ESP32S3 module (spiram) with ESP32S3' (DevkitC-1-N8R2)

Pydos_pins = {
    'sndPin' : (10,"GPIO10"),
    'neoPixel' : (48,"GPIO48"),
    'I2C_NUM' : (1,"machine.I2C(1), scl=GPIO9,sda=GPIO8"),
    'SCL' : (9,"GPIO9"),
    'SDA' : (8,"GPIO8"),
    'SPI_NUM' : [(1,"machine.SPI(1, sck=12,mosi=11,miso=13)")],
    'SCK' : [(12,"GPIO12")],
    'MOSI' : [(11,"GPIO11")],
    'MISO' : [(13,"GPIO13")],
    'CS' : [(7,"GPIO7")]
}
