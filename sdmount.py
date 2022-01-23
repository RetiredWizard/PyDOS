from sys import implementation

if implementation.name.upper() == "MICROPYTHON":
    import sdcard
elif implementation.name.upper() == "CIRCUITPYTHON":
    import adafruit_sdcard
    import board
    import storage
    import digitalio
    if board.board_id == "unexpectedmaker_feathers2":
        import kfw_s2_board as board
    if board.board_id == "raspberry_pi_pico":
        import kfw_pico_board as board

drive = "/sd"

if __name__ != "PyDOS":
    passedIn = ""

if passedIn != "":
    drive = passedIn


if implementation.name.upper() == "MICROPYTHON":
    try:
        sd = sdcard.SDCard(spi=1, sck=14, mosi=15, miso=12, cs=9, drive=drive)
    except Exception as e:
        print_exception(e)

elif implementation.name.upper() == "CIRCUITPYTHON":
    try:
        sd = adafruit_sdcard.SDCard(board.SPI(), digitalio.DigitalInOut(board.D5))
        vfs = storage.VfsFat(sd)
        storage.mount(vfs, drive)
    except Exception as e:
        print('SD-Card: Fail,', e)
