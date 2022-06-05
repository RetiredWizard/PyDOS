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

        if "SD_CS" in dir(board):
            print("SD_CS                  ",board.SD_CS)
        else:
            print("SD_CS                  ","board.D5")

        if 'SD_SPI' in dir(board):
            print("SD_SPI                 ","board.SD_SPI()")
        else:
            if 'SD_SCK' in dir(board):
                if 'SD_MOSI' in dir(board):
                    print("SD_SCK                 ",board.SD_SCK)
                    print("SD_MOSI                ",board.SD_MOSI)
                    print("SD_MISO                ",board.SD_MISO)
                elif 'SD_COPI' in dir(board):
                    print("SD_SCK                 ",board.SD_SCK)
                    print("SD_COPI                ",board.SD_COPI)
                    print("SD_CIPO                ",board.SD_CIPO)
            else:
                if 'SPI' in dir(board):
                    print("SD_SPI                 ","board.SPI()")
                else:
                    if 'SCK' in dir(board):
                        if 'MOSI' in dir(board):
                            print("SD_SCK                 ",board.SCK)
                            print("SD_MOSI                ",board.MOSI)
                            print("SD_MISO                ",board.MISO)
                        elif 'COPI' in dir(board):
                            print("SD_SCK                 ",board.SCK)
                            print("SD_COPI                ",board.COPI)
                            print("SD_CIPO                ",board.CIPO)

        if board.board_id == 'arduino_nano_rp2040_connect':
            # For Gemma M0, Trinket M0, Metro M0/M4 Express, ItsyBitsy M0/M4 Express
            print("Read/Write Ground Pin: ","board.D2")
        elif board.board_id in ['raspberry_pi_pico','cytron_maker_pi_rp2040']:
            print("Read/Write Ground Pin: ","board.GP6")
        elif board.board_id == 'adafruit_qtpy_esp32c3':
            print("Read/Write Ground Pin: ","board.A1")
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

        if uname().machine == 'Raspberry Pi Pico with RP2040':
            #sd = sdcard.SDCard(spi=1, sck=10, mosi=11, miso=12, cs=15, drive=drive)
            print("SD_CS                  ","Pin(15)")
            print("SD_SCK                 ","Pin(10)")
            print("SD_MOSI                ","Pin(11)")
            print("SD_MISO                ","Pin(12)")

        else:
            #sd = sdcard.SDCard(spi=1, sck=14, mosi=15, miso=12, cs=9, drive=drive)
            print("SD_CS                  ","Pin(9)")
            print("SD_SCK                 ","Pin(14)")
            print("SD_MOSI                ","Pin(15)")
            print("SD_MISO                ","Pin(12)")

    return

printPinAssignments()
