import board
Pydos_pins = {
    'sndPin'    : (board.SPEAKER,"SPEAKER"),
    'SCL'       : (board.SCL,"SCL"),
    'SDA'       : (board.SDA,"SDA"),
    'SCK'       : [(board.SD_SCK,"SD_SCK")],
    'MISO'      : [(board.SD_MISO,"SD_MISO")],
    'MOSI'      : [(board.SD_MOSI,"SD_MOSI")],
    'CS'        : [(board.SD_CS,"SD_CS")],
    'LED_RED'   : (board.LED_RED,"LED_RED"),
    'LED_GREEN' : (board.LED_GREEN,"LED_GREEN"),
    'LED_BLUE'  : (board.LED_BLUE,"LED_BLUE")
}
