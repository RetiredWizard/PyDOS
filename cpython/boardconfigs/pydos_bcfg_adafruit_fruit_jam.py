# PyDOS Board Configuration for 'adafruit_fruit_jam'

import board

Pydos_pins = {
    'neoPixel' : (board.NEOPIXEL,"NEOPIXEL GPIO32"),
    # Fruit Jam DAC not yet supported in PyDOS sound examples
    # Will require TLV320DAC3100 configuration in code
    'i2s_BitClock'   : (board.I2S_BCLK,"board.I2S_BCLK GPIO26"),
    'i2s_WordSelect' : (board.I2S_WS,"board.I2S_WS GPIO27"),
    'i2s_Data'       : (board.I2S_DIN,"board.I2S_DIN GPIO24"),

    'SCL' : (board.SCL,"SCL GPIO21"),
    'SDA' : (board.SDA,"SDA GPIO20"),
    'SCK' : [(board.SD_SCK,"SD_SCK GPIO34"), (board.SCK,"SCK GPIO30")],
    'MOSI' : [(board.SD_MOSI,"SD_MOSI GPIO35"), (board.MOSI,"MOSI GPIO31")],
    'MISO' : [(board.SD_MISO,"SD_MISO GPIO36"), (board.MISO,"MISO GPIO28")],
    'CS' : [(board.SD_CS,"SD_CS GPIO39"), (None,"None")],

}
