import board
Pydos_pins = {
    'sndPin'    : (board.IO26,"IO26"),
    'SCL'       : (board.IO27,"IO27"),
    'SDA'       : (board.IO22,"IO22"),
    'SCK'       : [(board.IO18,"SCL IO18")],
    'MISO'      : [(board.IO19,"MISO IO19")],
    'MOSI'      : [(board.IO23,"MOSI IO23")],
    'CS'        : [(board.IO5,"CS IO5")],
    'LED_RED'   : (board.IO4,"IO4"),
    'LED_GREEN' : (board.IO16,"IO16"),
    'LED_BLUE'  : (board.IO17,"IO17")
}
