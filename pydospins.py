from sys import implementation
import pydos_hw

if implementation.name.upper() == "CIRCUITPYTHON":
    import board
elif implementation.name.upper() == "MICROPYTHON":
    from os import uname


def printPinAssignments():

    if implementation.name.upper() == "CIRCUITPYTHON":
        print("Board ID:              ",board.board_id)
        print("PyDOS Sound Pin:       ",pydos_hw.sndPin)
        if "SCL" in dir(board):
            print("SCL                    ",board.SCL)
            print("SDA                    ",board.SDA)
        else:
            if board.board_id == "cytron_maker_pi_rp2040":
                print("I2C                    ","Grove #2")
            elif board.board_id == "raspberry_pi_pico":
                print("SCL                    ","board.GP3")
                print("SDA                    ","board.GP2")
            elif board.board_id == 'espressif_esp32s3_devkitc_1_n8r2':
                print("SCL                    ","board.IO7")
                print("SDA                    ","board.IO6")

        if board.board_id == 'arduino_nano_rp2040_connect':
            # For Gemma M0, Trinket M0, Metro M0/M4 Express, ItsyBitsy M0/M4 Express
            print("Read/Write Ground Pin: ","board.D2")
        elif board.board_id in ['raspberry_pi_pico','cytron_maker_pi_rp2040']:
            print("Read/Write Ground Pin: ","board.GP6")
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
        print('*The Read/Write Ground Pin will no longer function after')
        print('the PyDOS "fs" command has been used')

    elif implementation.name.upper() == "MICROPYTHON":
        print("Board ID:              ",uname().machine)
        print("PyDOS Sound Pin:       ",pydos_hw.sndPin)
        print("SCL Pin:               ",pydos_hw.Pydos_hw.SCL)
        print("SDA Pin:               ",pydos_hw.Pydos_hw.SDA)

    return

printPinAssignments()
