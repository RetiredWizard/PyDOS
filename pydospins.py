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
        print("SCL                    ",pydos_hw.PyDOS_HW.SCL)
        print("SDA                    ",pydos_hw.PyDOS_HW.SDA)
        if board.board_id == "cytron_maker_pi_rp2040":
            print('*** The "+" pins on the SERVO header put out 5V')
            print('Be sure to use a grove 3v3 pin when connecting 3v3 devices')
            print('The GPIO pins on the SERVO header use 3.3V logic')
            print("I2C                    ","Grove #2")
        elif 'STEMMA_I2C' in dir(board):
            print("I2C                    ","board.STEMMA_I2C")
        elif 'I2C' in dir(board):
            print("I2C                    ","board.I2C")

        if board.board_id == 'unexpectedmaker_feathers2':
            print("SD_CS                  ","board.IO1")
        elif "SD_CS" in dir(board):
            print("SD_CS                  ",board.SD_CS)
        else:
            if 'D5' in dir(board):
                print("SD_CS                  ",board.D5)
            elif 'GP5' in dir(board):
                print("SD_CS                  ",board.GP5)
            elif 'IO5' in dir(board):
                print("SD_CS                  ",board.IO5)

        if 'SD_SPI' in dir(board):
            print("SD_SPI                 ","board.SD_SPI()")
        elif 'SPI' in dir(board):
            print("SD_SPI                 ","board.SPI()")

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
            if 'SCK' in dir(board):
                if 'MOSI' in dir(board):
                    print("SD_SCK                 ",board.SCK)
                    print("SD_MOSI                ",board.MOSI)
                    print("SD_MISO                ",board.MISO)
                elif 'COPI' in dir(board):
                    print("SD_SCK                 ",board.SCK)
                    print("SD_COPI                ",board.COPI)
                    print("SD_CIPO                ",board.CIPO)
            elif board.board_id == 'raspberry_pi_pico':
                if pydos_hw.PyDOS_HW.KFW:
                    print("SD_SCK                 ",board.GP18)
                    print("SD_MOSI                ",board.GP19)
                    print("SD_MISO                ",board.GP16)
                else:
                    print("SD_SCK                 ",board.GP14)
                    print("SD_MOSI                ",board.GP15)
                    print("SD_MISO                ",board.GP12)
            elif 'D14' in dir(board):
                print("SD_SCK                 ",board.D14)
                print("SD_MOSI                ",board.D15)
                print("SD_MISO                ",board.D12)
            elif 'GP14' in dir(board):
                print("SD_SCK                 ",board.GP14)
                print("SD_MOSI                ",board.GP15)
                print("SD_MISO                ",board.GP12)
            elif 'IO14' in dir(board):
                print("SD_SCK                 ",board.IO14)
                print("SD_MOSI                ",board.IO15)
                print("SD_MISO                ",board.IO12)


        if board.board_id == 'arduino_nano_rp2040_connect':
            # For Gemma M0, Trinket M0, Metro M0/M4 Express, ItsyBitsy M0/M4 Express
            print("Read/Write Ground Pin: ","board.D2")
        elif board.board_id in ['raspberry_pi_pico','cytron_maker_pi_rp2040']:
            print("Read/Write Ground Pin: ","board.GP6")
        elif board.board_id == 'adafruit_qtpy_esp32c3':
            print("Read/Write Ground Pin: ","board.A1")
        elif board.board_id == 'unexpectedmaker_feathers2':
            print("Read/Write Ground Pin: ","board.IO1")
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

        elif uname().machine == 'Arduino Nano RP2040 Connect with RP2040':
            #sd = sdcard.SDCard(spi=1, sck=6, copi=7, cipo=4, cs=5, drive=drive)
            print("SD_CS                  ","GPIO5 D10")
            print("SD_SCK                 ","GPIO6 D13 LED")
            print("SD_MOSI                ","GPIO7 D11")
            print("SD_MISO                ","GPIO4 D12")
        elif uname().machine == 'Adafruit Feather RP2040 with RP2040':
            #sd = sdcard.SDCard(spi=0,sck=18,mosi=19,miso=20,cs=9,drive=drive)
            print("SD_CS                  ","GPIO9 D9")
            print("SD_SCK                 ","GPIO18 SCK")
            print("SD_MOSI                ","GPIO19 MOSI")
            print("SD_MISO                ","GPIO20 MISO")
        elif uname().machine == 'TinyPICO with ESP32-PICO-D4':
            #sd = sdcard.SDCard(spi=1,sck=18,mosi=19,miso=23,cs=5,drive=drive)
            print("SD_CS                  ","GPIO5 SS")
            print("SD_SCK                 ","GPIO18 SCK")
            print("SD_MOSI                ","GPIO19 MOSI")
            print("SD_MISO                ","GPIO23 MISO")
        else:
            #sd = sdcard.SDCard(spi=1, sck=14, mosi=15, miso=12, cs=9, drive=drive)
            print("SD_CS                  ","Pin(9)")
            print("SD_SCK                 ","Pin(14)")
            print("SD_MOSI                ","Pin(15)")
            print("SD_MISO                ","Pin(12)")

    return

printPinAssignments()
