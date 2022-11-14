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

def printPinAssignments():

    if implementation.name.upper() == "CIRCUITPYTHON":
        print("Board ID:                ",board.board_id)
        if board.board_id == "cytron_maker_pi_rp2040":
            print('*** The "+" pins on the SERVO header put out 5V')
            print('Be sure to use a grove 3v3 pin when connecting 3v3 devices')
            print('The GPIO pins on the SERVO header use 3.3V logic\n')
            print("I2C                      ","Grove #2")
        elif 'STEMMA_I2C' in dir(board):
            print("I2C                      ","board.STEMMA_I2C")
        elif 'I2C' in dir(board):
            print("I2C                      ","board.I2C")

        if 'SD_SPI' in dir(board):
            print("SD_SPI                   ","board.SD_SPI()")
        if 'SPI' in dir(board):
            print("SPI                      ","board.SPI()")

    elif implementation.name.upper() == "MICROPYTHON":
        print("Board ID:                ",implementation._machine)

    for entry in Pydos_pins:
        if entry == 'sndPin':
            print("PyDOS Sound Pin:         ",Pydos_pins['sndPin'][1])
        elif entry in ['led','SCL','SDA','SD_CS','SD_SCK','SD_MOSI','SD_MISO','CS','SCK','MOSI','MISO','neoPixel']:
            print(entry+" Pin:"+(20-len(entry))*" ",Pydos_pins[entry][1])
        else:
            if Pydos_pins[entry][1] != None:
                print("*Custom Pin ["+entry+"]:"+(max(0,10-len(entry)))*" ",Pydos_pins[entry][1])

    if implementation.name.upper() == "CIRCUITPYTHON":
        if board.board_id == 'arduino_nano_rp2040_connect':
            print("Read/Write Ground Pin:   ","board.D2")
        elif board.board_id in ['raspberry_pi_pico','cytron_maker_pi_rp2040']:
            print("Read/Write Ground Pin:   ","board.GP6")
        elif board.board_id == 'adafruit_qtpy_esp32c3':
            print("Read/Write Ground Pin:   ","board.A1")
        elif board.board_id == 'unexpectedmaker_feathers2':
            print("Read/Write Ground Pin:   ","board.IO1")
        elif board.board_id == 'adafruit_itsybitsy_rp2040':
            print("Read/Write Ground Pin:   ","board.D7")
        else:
            if "D5" in dir(board):
                print("Read/Write Ground Pin:   ","board.D5")
            elif "GP5" in dir(board):
                print("Read/Write Ground Pin:   ","board.GP5")
            elif "IO5" in dir(board):
                print("Read/Write Ground Pin:   ","board.IO5")
            elif "D6" in dir(board):
                print("Read/Write Ground Pin:   ","board.D6")
            elif "GP6" in dir(board):
                print("Read/Write Ground Pin:   ","board.GP6")
            elif "IO6" in dir(board):
                print("Read/Write Ground Pin:   ","board.IO6")
            elif "D2" in dir(board):
                print("Read/Write Ground Pin:   ","board.D2")
            elif "GP2" in dir(board):
                print("Read/Write Ground Pin:   ","board.GP2")
            elif "IO2" in dir(board):
                print("Read/Write Ground Pin:   ","board.IO2")
            else:
                print("Read/Write Ground Pin:   ","None")
                print("To set the PyDOS FS readonly and give the host write access")
                print("the following command at the PyDOS prompt: fs ro")

        print()
        print('*The Read/Write Ground Pin will no longer function')
        print('after the PyDOS "fs" command has been used')


    return

printPinAssignments()
