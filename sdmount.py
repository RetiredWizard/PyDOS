from sys import implementation,print_exception

if implementation.name.upper() == "MICROPYTHON":
    import sdcard
    from os import uname
elif implementation.name.upper() == "CIRCUITPYTHON":
    import adafruit_sdcard
    import storage
    import digitalio
    from pydos_ui import PyDOS_UI

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
        sd = adafruit_sdcard.SDCard(PyDOS_UI.SPI(), PyDOS_UI.SD_CS)
        vfs = storage.VfsFat(sd)
        storage.mount(vfs, drive)
    except Exception as e:
        print('SD-Card: Fail,', e)
