import sdcard
drive = "/sd"
if passedIn != "":
    drive = passedIn
sd = sdcard.SDCard(spi=1, sck=14, mosi=15, miso=12, cs=9, drive=drive)