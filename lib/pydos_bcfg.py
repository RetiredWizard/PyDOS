# PyDOS Board Configuration for Unidentified board

"""

    DICTIONARY VALUES INPUT VIA pydos_bcfg.py AS TUPLES

    led
    sndPin
    i2s_BitClock
    i2s_WordSelect
    i2s_Data
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
        test = Pin(led,Pin.OUT)
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
    bdir = dir(board)

    if 'BUZZER' in bdir:
        Pydos_pins['sndPin'] = (board.BUZZER,"board.BUZZER")
    elif 'D12' in bdir:
        Pydos_pins['sndPin'] = (board.D12,"D12 GPIO12")
    if 'I2S_BIT_CLOCK' in bdir:
        Pydos_pins['i2s_BitClock'] = (board.I2S_BIT_CLOCK,"board.I2S_BIT_CLOCK")
        Pydos_pins['i2s_WordSelect'] = (board.I2S_WORD_SELECT,"board.I2S_WORD_SELECT")
        if 'I2S_DATA' in bdir:
            Pydos_pins['i2s_Data'] = (board.I2S_DATA,"board.I2S_DATA")
        else:
            Pydos_pins['i2s_Data'] = (board.IS2_DATA,"board.IS2_DATA")
    elif 'SPEAKER_SCK' in bdir:
        Pydos_pins['i2s_BitClock'] = (board.SPEAKER_SCK,"board.SPEAKER_SCK")
        Pydos_pins['i2s_WordSelect'] = (board.SPEAKER_WS,"board.SPEAKER_WS")
        Pydos_pins['i2s_Data'] = (board.SPEAKER_DOUT,"board.SPEAKER_DOUT")
    if 'LED_RED' in bdir:
        Pydos_pins['LED_RED'] = (board.LED_RED,"LED_RED")
    elif 'LED_R' in bdir:
        Pydos_pins['LED_RED'] = (board.LED_R,"LED_R")
    if 'LED_GREEN' in bdir:
        Pydos_pins['LED_GREEN'] = (board.LED_GREEN,"LED_GREEN")
    elif 'LED_G' in bdir:
        Pydos_pins['LED_GREEN'] = (board.LED_G,"LED_G")
    if 'LED_BLUE' in bdir:        
        Pydos_pins['LED_BLUE'] = (board.LED_BLUE,"LED_BLUE")
    elif 'LED_B' in bdir:
        Pydos_pins['LED_BLUE'] = (board.LED_B,"LED_B")
    if 'NEOPIXEL' in bdir:
        Pydos_pins['neoPixel'] = (board.NEOPIXEL,"NEOPIXEL")
    if 'NEOPIXEL_POWER' in bdir:
        Pydos_pins['neoPixel_Pow'] = (board.NEOPIXEL_POWER,"NEOPIXEL_POWER")
    if 'DOTSTAR_CLOCK' in bdir:
        Pydos_pins['dotStar_Clock'] = (board.DOTSTAR_CLOCK,"DOTSTAR_CLOCK")
    if 'DOTSTAR_DATA' in bdir:
        Pydos_pins['dotStar_Data'] = (board.DOTSTAR_DATA,"DOTSTAR_DATA")
    if 'DOTSTAR_POWER' in bdir:
        Pydos_pins['dotStar_Pow'] = (board.DOTSTAR_POWER,"DOTSTAR_POWER")
    if 'SCL' in bdir:
        Pydos_pins['SCL'] = (board.SCL,"SCL")
        Pydos_pins['SDA'] = (board.SDA,"SDA")
    elif 'D3' in bdir and 'D2' in bdir:
        Pydos_pins['SCL'] = (board.D3,"SCL D3")
        Pydos_pins['SDA'] = (board.D2,"SDA D2")

    Pydos_pins["SCK"] = []
    Pydos_pins["MOSI"] = []
    Pydos_pins["MISO"] = []
    Pydos_pins["CS"] = []

    _SCK = False
    if 'SD_SCK' in bdir:
        _SCK = board.SD_SCK
    elif 'SD_CLK' in bdir:
        _SCK = board.SD_CLK
    if _SCK:
        
        if 'SD_MOSI' in bdir:
            Pydos_pins["SCK"].append((_SCK,"SD_SCK"))
            Pydos_pins["MOSI"].append((board.SD_MOSI,"SD_MOSI"))
            Pydos_pins["MISO"].append((board.SD_MISO,"SD_MISO"))
        elif 'SD_COPI' in bdir:
            Pydos_pins["SCK"].append((_SCK,"SD_SCK"))
            Pydos_pins["MOSI"].append((board.SD_COPI,"SD_COPI"))
            Pydos_pins["MISO"].append((board.SD_CIPO,"SD_CIPO"))
        if 'SD_CS' in bdir:
            Pydos_pins["CS"].append((board.SD_CS,"SD_CS"))
        else:
            Pydos_pins["CS"].append((None,"None"))

    _SCK = False
    if 'SCK' in bdir:
        _SCK = board.SCK
    elif 'CLK' in bdir:
        _SCK = board.CLK
    if _SCK:
        if 'MOSI' in bdir:
            Pydos_pins["SCK"].append((_SCK,"SCK"))
            Pydos_pins["MOSI"].append((board.MOSI,"MOSI"))
            Pydos_pins["MISO"].append((board.MISO,"MISO"))
        elif 'COPI' in bdir:
            Pydos_pins["SCK"].append((_SCK,"SCK"))
            Pydos_pins["MOSI"].append((board.SD_COPI,"COPI"))
            Pydos_pins["MISO"].append((board.SD_CIPO,"CIPO"))
        if "CS" in bdir:
            Pydos_pins["CS"].append((board.CS,"CS"))
        elif "SS" in bdir:
            Pydos_pins["CS"].append((board.SS,"SS"))
        else:
            Pydos_pins["CS"].append((None,"None"))

    if 'SDIO_CLK' in bdir and 'SDIO_CMD' in bdir:
        Pydos_pins['SDIO_CLK'] = (board.SDIO_CLK,"board.SDIO_CLK")
        Pydos_pins['SDIO_CMD'] = (board.SDIO_CMD,"board.SDIO_CMD")
        datapins = [getattr(board,attr) for attr in bdir if 'SDIO_D' in attr]
        if len(datapins) > 0:
            Pydos_pins['SDIO_DPINS'] = (datapins,"[board.SDIO_D*]")

