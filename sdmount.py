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
        elif uname().machine == 'Arduino Nano RP2040 Connect with RP2040':
            sd = sdcard.SDCard(spi=0, sck=6, mosi=7, miso=4, cs=5, drive=drive)
        elif uname().machine == 'Adafruit Feather RP2040 with RP2040':
            sd = sdcard.SDCard(spi=0,sck=18,mosi=19,miso=20,cs=9,drive=drive)
        elif uname().machine == 'ESP32S3 module (spiram) with ESP32S3':
            sd = sdcard.SDCard(spi=2, sck=14, mosi=15, miso=12, cs=9, drive=drive)
        elif uname().machine == 'TinyPICO with ESP32-PICO-D4':
            sd = sdcard.SDCard(spi=1,sck=18,mosi=19,miso=23,cs=5,drive=drive)
        else:
            sd = sdcard.SDCard(spi=1, sck=14, mosi=15, miso=12, cs=9, drive=drive)
    except Exception as e:
        print_exception(e)

elif implementation.name.upper() == "CIRCUITPYTHON":
    if not PyDOS_HW.SD_CS:
        print("CS Pin not allocated for SDCard SPI interface")
    else:
        try:
            sd = adafruit_sdcard.SDCard(PyDOS_HW.SD_SPI(), PyDOS_HW.SD_CS)
            vfs = storage.VfsFat(sd)
            storage.mount(vfs, drive)
        except Exception as e:
            print('SD-Card: Fail,', e)
