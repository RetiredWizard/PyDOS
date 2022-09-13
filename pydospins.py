from sys import implementation
from pydos_bcfg import Pydos_pins

if implementation.name.upper() == "CIRCUITPYTHON":
    import board
    if board.board_id == 'raspberry_pi_pico':
        try:
            import kfw_pico_board as board
        except:
            pass

        try:
            import cyt_mpp_board as board
        except:
            pass
    elif board.board_id == 'unexpectedmaker_feathers2':
        try:
            import kfw_s2_board as board
        except:
            pass
elif implementation.name.upper() == "MICROPYTHON":
    from os import uname


def printPinAssignments():

    if implementation.name.upper() == "CIRCUITPYTHON":
        print("Board ID:              ",board.board_id)
    elif implementation.name.upper() == "MICROPYTHON":
        print("Board ID:              ",uname().machine)

    if Pydos_pins.get('sndPin',(None,None))[1]:
        print("PyDOS Sound Pin:       ",Pydos_pins['sndPin'][1])

    if Pydos_pins.get('SCL',(None,None))[1]:
        print("SCL Pin:               ",Pydos_pins['SCL'][1])

    if Pydos_pins.get('SDA',(None,None))[1]:
        print("SDA Pin:               ",Pydos_pins['SDA'][1])

    if implementation.name.upper() == "CIRCUITPYTHON":
        if board.board_id == "cytron_maker_pi_rp2040":
            print('*** The "+" pins on the SERVO header put out 5V')
            print('Be sure to use a grove 3v3 pin when connecting 3v3 devices')
            print('The GPIO pins on the SERVO header use 3.3V logic')
            print("I2C                    ","Grove #2")
        elif 'STEMMA_I2C' in dir(board):
            print("I2C                    ","board.STEMMA_I2C")
        elif 'I2C' in dir(board):
            print("I2C                    ","board.I2C")

        if 'SD_SPI' in dir(board):
            print("SD_SPI                 ","board.SD_SPI()")
        if 'SPI' in dir(board):
            print("SPI                    ","board.SPI()")

    if Pydos_pins.get('SD_CS',(None,None))[1]:
        print("SD_CS Pin:             ",Pydos_pins['SD_CS'][1])

    if Pydos_pins.get('SD_SCK',(None,None))[1]:
        print("SD_SCK Pin:            ",Pydos_pins['SD_SCK'][1])

    if Pydos_pins.get('SD_MOSI',(None,None))[1]:
        print("SD_MOSI Pin:           ",Pydos_pins['SD_MOSI'][1])

    if Pydos_pins.get('SD_MISO',(None,None))[1]:
        print("SD_MISO Pin:           ",Pydos_pins['SD_MISO'][1])

    if Pydos_pins.get('CS',(None,None))[1]:
        print("CS Pin:                ",Pydos_pins['CS'][1])

    if Pydos_pins.get('SCK',(None,None))[1]:
        print("SCK Pin:               ",Pydos_pins['SCK'][1])

    if Pydos_pins.get('MOSI',(None,None))[1]:
        print("MOSI Pin:              ",Pydos_pins['MOSI'][1])

    if Pydos_pins.get('MISO',(None,None))[1]:
        print("MISO Pin:              ",Pydos_pins['MISO'][1])

    if implementation.name.upper() == "CIRCUITPYTHON":
        if board.board_id == 'arduino_nano_rp2040_connect':
            # For Gemma M0, Trinket M0, Metro M0/M4 Express, ItsyBitsy M0/M4 Express
            print("Read/Write Ground Pin: ","board.D2")
        elif board.board_id in ['raspberry_pi_pico','cytron_maker_pi_rp2040']:
            print("Read/Write Ground Pin: ","board.GP6")
        elif board.board_id == 'adafruit_qtpy_esp32c3':
            print("Read/Write Ground Pin: ","board.A1")
        elif board.board_id == 'unexpectedmaker_feathers2':
            print("Read/Write Ground Pin: ","board.IO1")
        elif board.board_id == 'adafruit_itsybitsy_rp2040':
            print("Read/Write Ground Pin: ","board.D7")
        else:
            if "D5" in dir(board):
                print("Read/Write Ground Pin: ","board.D5")
            elif "GP5" in dir(board):
                print("Read/Write Ground Pin: ","board.GP5")
            elif "IO5" in dir(board):
                print("Read/Write Ground Pin: ","board.IO5")
            elif "D6" in dir(board):
                print("Read/Write Ground Pin: ","board.D6")
            elif "GP6" in dir(board):
                print("Read/Write Ground Pin: ","board.GP6")
            elif "IO6" in dir(board):
                print("Read/Write Ground Pin: ","board.IO6")
            elif "D2" in dir(board):
                print("Read/Write Ground Pin: ","board.D2")
            elif "GP2" in dir(board):
                print("Read/Write Ground Pin: ","board.GP2")
            elif "IO2" in dir(board):
                print("Read/Write Ground Pin: ","board.IO2")
            else:
                print("Read/Write Ground Pin: ","None")
                print("To set the PyDOS FS readonly and give the host write access")
                print("the following command at the PyDOS prompt: fs ro")

        print()
        print('*The Read/Write Ground Pin will no longer function')
        print('after the PyDOS "fs" command has been used')


    return

printPinAssignments()

