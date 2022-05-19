from sys import implementation

if implementation.name.upper() == "MICROPYTHON":
    from sys import print_exception
    import sdcard
    from os import uname
elif implementation.name.upper() == "CIRCUITPYTHON":
    import adafruit_sdcard
    import storage
    from pydos_hw import PyDOS_HW

drive = "/sd"

if __name__ != "PyDOS":
    passedIn = ""

if passedIn != "":
    drive = passedIn


if implementation.name.upper() == "MICROPYTHON":
    try:
        if uname().machine == 'Raspberry Pi Pico with RP2040':
            sd = sdcard.SDCard(spi=1, sck=10, mosi=11, miso=12, cs=15, drive=drive)
        else:
            sd = sdcard.SDCard(spi=1, sck=14, mosi=15, miso=12, cs=9, drive=drive)
    except Exception as e:
        print_exception(e)

elif implementation.name.upper() == "CIRCUITPYTHON":
    try:
        sd = adafruit_sdcard.SDCard(PyDOS_HW.SD_SPI(), PyDOS_HW.SD_CS)
        vfs = storage.VfsFat(sd)
        storage.mount(vfs, drive)
    except Exception as e:
        print('SD-Card: Fail,', e)
