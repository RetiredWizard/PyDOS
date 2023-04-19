# PyDOS Board Configuration for 'ESP32C3 module with ESP32C3' 
# Generic Micropython build configured for adafruit_qtpy_esp32c3/Seeed XIAO esp32-c3

Pydos_pins = {
    'sndPin' : (0,"0 A3"),
    'neoPixel' : (2,"2"),
    'I2C_NUM' : (1,"Stemma_I2C"),
    'SCL' : (6,"6 SCL"),
    'SDA' : (5,"5 SDA"),
    'SCK' : [(10,"10 SCK")],
    'MOSI' : [(7,"7 MO")],
    'MISO' : [(8,"8 MI")],
    'CS' : [(1,"1 A2")]
}
