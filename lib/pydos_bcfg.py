# PyDOS Board Configuration for Unidentified board

"""
    sndPin
    neoPixel
    neoPixel_Pow
    dotStar_Clock
    dotStar_Data

    I2C_NUM
    SCL
    SDA

    SD_SPI_NUM
    SD_SCK
    SD_MOSI
    SD_MISO
    SD_CS

    SPI_NUM
    SCK
    MOSI
    MISO
    CS
"""
from sys import implementation

if implementation.name.upper() == "CIRCUITPYTHON":
    import board

if implementation.name.upper() == "MICROPYTHON":
    Pydos_pins = {
        'sndPin' : (7,"IO7"),
        'led' : ('LED',"LED"),
        'neoPixel' : (16,"IO16"),
        'I2C_NUM' : (1,None),
        'SCL' : (3,"SCL IO3"),
        'SDA' : (2,"SDA IO2"),
        'SD_SPI_NUM' : (1,None),
        'SCK' : (14,"SCK IO14"),
        'MOSI' : (15,"MO IO15"),
        'MISO' : (12,"MI IO12"),
        'CS' : (9,"SS IO9")
    }

elif implementation.name.upper() == "CIRCUITPYTHON":
    Pydos_pins = {}

    if 'BUZZER' in dir(board):
        Pydos_pins['sndPin'] = (board.BUZZER,"board.BUZZER")
    elif 'D12' in dir(board):
        Pydos_pins['sndPin'] = (board.D12,"D12 GPIO12")
    if 'NEOPIXEL' in dir(board):
        Pydos_pins['neoPixel'] = (board.NEOPIXEL,None)
    if 'NEOPIXEL_POWER' in dir(board):
        Pydos_pins['neoPixel_Pow'] = (board.NEOPIXEL_POWER,None)
    if 'DOTSTAR_CLOCK' in dir(board):
        Pydos_pins['dotStar_Clock'] = (board.DOTSTAR_CLOCK,None)
    if 'DOTSTAR_DATA' in dir(board):
        Pydos_pins['dotStar_Data'] = (board.DOTSTAR_DATA,None)
    if 'SCL' in dir(board):
        Pydos_pins['SCL'] = (board.SCL,"SCL")
        Pydos_pins['SDA'] = (board.SDA,"SDA")
    elif 'D3' in dir(board) and 'D2' in dir(board):
        Pydos_pins['SCL'] = (board.D3,"SCL D3")
        Pydos_pins['SDA'] = (board.D2,"SDA D2")


    if "SD_CS" in dir(board):
        Pydos_pins["SD_CS"] = (board.SD_CS,"SD_CS")
    if "CS" in dir(board):
        Pydos_pins["CS"] = (board.CS,"CS")

    _SCK = False
    if 'SD_SCK' in dir(board):
        _SCK = board.SD_SCK
    elif 'SD_CLK' in dir(board):
        _SCK = board.SD_CLK
    if _SCK:
        if 'SD_MOSI' in dir(board):
            Pydos_pins["SD_SCK"] = (_SCK,"SD_SCK")
            Pydos_pins["SD_MOSI"] = (board.SD_MOSI,"SD_MOSI")
            Pydos_pins["SD_MISO"] = (board.SD_MISO,"SD_MISO")
        elif 'SD_COPI' in dir(board):
            Pydos_pins["SD_SCK"] = (_SCK,"SD_SCK")
            Pydos_pins["SD_MOSI"] = (board.SD_COPI,"SD_COPI")
            Pydos_pins["SD_MISO"] = (board.SD_CIPO,"SD_CIPO")

    _SCK = False
    if 'SCK' in dir(board):
        _SCK = board.SCK
    elif 'CLK' in dir(board):
        _SCK = board.CLK
    if _SCK:
        if 'MOSI' in dir(board):
            Pydos_pins["SCK"] = (_SCK,"SCK")
            Pydos_pins["MOSI"] = (board.MOSI,"MOSI")
            Pydos_pins["MISO"] = (board.MISO,"MISO")
        elif 'COPI' in dir(board):
            Pydos_pins["SCK"] = (_SCK,"SCK")
            Pydos_pins["MOSI"] = (board.SD_COPI,"COPI")
            Pydos_pins["MISO"] = (board.SD_CIPO,"CIPO")
