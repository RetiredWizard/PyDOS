import board

Pydos_pins = {
    'SCL' : (board.SCL,"SCL GP17"),
    'SDA' : (board.SDA,"SDA GP16"),
# SDIO is faster
#    'SCK' : [(board.SD_SCK,"SD_SCK GP36")],
#    'MOSI' : [(board.SD_MOSI,"SD_MOSI GP36")],
#    'MISO' : [(board.SD_MISO,"SD_MISO GP37")],
#    'CS' : [(board.SD_CS,"SD_CS GP34")],
    'SDIO_CLK'   : (board.GP36,"GP36"),
    'SDIO_CMD'   : (board.GP35,"GP35"),
    'SDIO_DPINS' : ([board.GP37, board.GP33, board.GP38, board.GP34],"[GP37, GP33, GP38, GP34]")
}
