# PyDOS Board Configuration for Unidentified board

"""

    DICTIONARY VALUES INPUT VIA pydos_bcfg.py AS TUPLES

    led
    sndPin
    neoPixel
    neoPixel_Pow
    dotStar_Clock
    dotStar_Data
    dotStar_Extra
    dotStar_Pow

    I2C_NUM                     MicroPython hardware I2C number
    SCL
    SDA

    * SPI data entered as list of tuples
    * First tuple in list used for machine/board SD dedicated SPI (board.SD_SPI)
    * Last tuple in list used for machine/board general use SPI (board.SPI)
    SPI_NUM                     MicroPython hardware SPI number
    SCK
    MOSI
    MISO
    CS

    CALCULATED DATA 

    sndGPIO                     digitalio.DigitalInOut(sndPin)
    KFW                         Using Keyboard FeatherWing True/False
    I2CbbqDevice                I2C device being used for the KFW keyboard
    SD                          list of sdcard objects
    SDdrive                     list of mount points for mounted SD cards

"""
from sys import implementation

if implementation.name.upper() == "CIRCUITPYTHON":
    import board

if implementation.name.upper() == "MICROPYTHON":
    from machine import Pin
    try:
        led = "LED"
        test = machine.Pin(led,Pin.OUT)
    except:
        led = "D13"

    Pydos_pins = {
        'led' : (led,led),
        'neoPixel' : (16,"IO16"),
        'I2C_NUM' : (1,None),
        'SCL' : (3,"SCL IO3"),
        'SDA' : (2,"SDA IO2"),
        'SPI_NUM' : [(1,None)],
        'SCK' : [(14,"SCK IO14")],
        'MOSI' : [(15,"MO IO15")],
        'MISO' : [(12,"MI IO12")],
        'CS' : [(9,"SS IO9")]
    }

elif implementation.name.upper() == "CIRCUITPYTHON":
    Pydos_pins = {}

    if 'BUZZER' in dir(board):
        Pydos_pins['sndPin'] = (board.BUZZER,"board.BUZZER")
    elif 'D12' in dir(board):
        Pydos_pins['sndPin'] = (board.D12,"D12 GPIO12")
    if 'NEOPIXEL' in dir(board):
        Pydos_pins['neoPixel'] = (board.NEOPIXEL,"NEOPIXEL")
    if 'NEOPIXEL_POWER' in dir(board):
        Pydos_pins['neoPixel_Pow'] = (board.NEOPIXEL_POWER,"NEOPIXEL_POWER")
    if 'DOTSTAR_CLOCK' in dir(board):
        Pydos_pins['dotStar_Clock'] = (board.DOTSTAR_CLOCK,"DOTSTAR_CLOCK")
    if 'DOTSTAR_DATA' in dir(board):
        Pydos_pins['dotStar_Data'] = (board.DOTSTAR_DATA,"DOTSTAR_DATA")
    if 'DOTSTAR_POWER' in dir(board):
        Pydos_pins['dotStar_Pow'] = (board.DOTSTAR_POWER,"DOTSTAR_POWER")
    if 'SCL' in dir(board):
        Pydos_pins['SCL'] = (board.SCL,"SCL")
        Pydos_pins['SDA'] = (board.SDA,"SDA")
    elif 'D3' in dir(board) and 'D2' in dir(board):
        Pydos_pins['SCL'] = (board.D3,"SCL D3")
        Pydos_pins['SDA'] = (board.D2,"SDA D2")

    Pydos_pins["SCK"] = []
    Pydos_pins["MOSI"] = []
    Pydos_pins["MISO"] = []
    Pydos_pins["CS"] = []

    _SCK = False
    if 'SD_SCK' in dir(board):
        _SCK = board.SD_SCK
    elif 'SD_CLK' in dir(board):
        _SCK = board.SD_CLK
    if _SCK:
        
        if 'SD_MOSI' in dir(board):
            Pydos_pins["SCK"].append((_SCK,"SD_SCK"))
            Pydos_pins["MOSI"].append((board.SD_MOSI,"SD_MOSI"))
            Pydos_pins["MISO"].append((board.SD_MISO,"SD_MISO"))
        elif 'SD_COPI' in dir(board):
            Pydos_pins["SCK"].append((_SCK,"SD_SCK"))
            Pydos_pins["MOSI"].append((board.SD_COPI,"SD_COPI"))
            Pydos_pins["MISO"].append((board.SD_CIPO,"SD_CIPO"))
        if 'SD_CS' in dir(board):
            Pydos_pins["CS"].append((board.SD_CS,"SD_CS"))
        else:
            Pydos_pins["CS"].append((None,"None"))

    _SCK = False
    if 'SCK' in dir(board):
        _SCK = board.SCK
    elif 'CLK' in dir(board):
        _SCK = board.CLK
    if _SCK:
        Pydos_pins["SCK"] = []
        Pydos_pins["MOSI"] = []
        Pydos_pins["MISO"] = []
        if 'MOSI' in dir(board):
            Pydos_pins["SCK"].append((_SCK,"SCK"))
            Pydos_pins["MOSI"].append((board.MOSI,"MOSI"))
            Pydos_pins["MISO"].append((board.MISO,"MISO"))
        elif 'COPI' in dir(board):
            Pydos_pins["SCK"].append((_SCK,"SCK"))
            Pydos_pins["MOSI"].append((board.SD_COPI,"COPI"))
            Pydos_pins["MISO"].append((board.SD_CIPO,"CIPO"))
        if "CS" in dir(board):
            Pydos_pins["CS"].append((board.CS,"CS"))
        else:
            Pydos_pins["CS"].append((None,"None"))

