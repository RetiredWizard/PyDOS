from sys import implementation
from pydos_bcfg import Pydos_pins
from pydos_hw import Pydos_hw

if implementation.name.upper() == "CIRCUITPYTHON":
    import board
    import microcontroller
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
        i2cBus = ""
        print("Board ID:                ",board.board_id)
        if board.board_id == "cytron_maker_pi_rp2040":
            print('*** The "+" pins on the SERVO header put out 5V')
            print('Be sure to use a grove 3v3 pin when connecting 3v3 devices')
            print('The GPIO pins on the SERVO header use 3.3V logic\n')
            i2cBus += "Grove #2, "
        if 'STEMMA_I2C' in dir(board):
            i2cBus += "STEMMA_I2C, "
        if 'I2C' in dir(board):
            i2cBus += "I2C, "
        if 'SCL' in dir(board):
            i2cBus += 'busio.I2C(SCL,SDA), '
        if 'SCL1' in dir(board):
            i2cBus += 'busio.I2C(SCL1,SDA1), '

        if len(i2cBus) > 0:
            print("I2C                      ",i2cBus[:-2])

        if 'SD_SPI' in dir(board):
            print("SPI                   ","board.SD_SPI()")
        if 'SPI' in dir(board):
            print("SPI                      ","board.SPI()")

    elif implementation.name.upper() == "MICROPYTHON":
        print("Board ID:                ",Pydos_hw.boardName)

    for entry in sorted(Pydos_pins):
        prnt_complete = False
        if entry == 'sndPin':
            print("PyDOS Sound Pin:         ",Pydos_pins['sndPin'][1],end="")
        elif entry in ['led','SCL','SDA','neoPixel','neoPixel_Pow','dotStar_Clock', \
            'dotStar_Data','dotStar_Extra','dotStar_Pow','LED_RED','LED_GREEN', \
            'LED_BLUE','i2s_BitClock','i2s_WordSelect','i2s_Data','SDIO_CLK', \
            'SDIO_CMD','SDIO_DPINS']:

            print(entry+" Pin:"+(20-len(entry))*" ",Pydos_pins[entry][1],end="")
        elif entry in ['I2C_NUM']:
            print("Machine "+entry+":"+(16-len(entry))*" ",Pydos_pins[entry][0],Pydos_pins[entry][1],end="")
        elif entry in ['CS','SCK','MOSI','MISO']:
            for i in range(len(Pydos_pins[entry])):
                print(entry+" ("+str(i)+") Pin:"+(16-len(entry))*" ",Pydos_pins[entry][i][1],end="")
                prnt_complete = True
                if implementation.name.upper() == "CIRCUITPYTHON":
                    try:
                        strAttr = str(getattr(board,Pydos_pins[entry][i][1].split(" ")[0])).split('.')[1]
                        if strAttr != Pydos_pins[entry][i][1].split(" ")[0]:
                            print(",",strAttr)
                        else:
                            print()
                    except:
                        print()
                else:
                    print()
        elif entry in ["SPI_NUM"]:
            prnt_complete = True
            for i in range(len(Pydos_pins[entry])):
                print("Machine "+entry+" ("+str(i)+"):"+(12-len(entry))*" ",Pydos_pins[entry][i][0],Pydos_pins[entry][i][1])
        else:
            try:
                if Pydos_pins[entry][1] != None:
                    print("*Custom Pin ["+entry+"]:"+(max(0,10-len(entry)))*" ",Pydos_pins[entry][1],end="")
            except:
                print("*Custom Pin ["+entry+"]:"+((max(0,10-len(entry)))*" ")+" ***ERROR***",end="")
        if implementation.name.upper() == "CIRCUITPYTHON" and not prnt_complete:
            try:
                strAttr = str(getattr(board,Pydos_pins[entry][1].split(" ")[0])).split('.')[1]
                if strAttr != Pydos_pins[entry][1].split(" ")[0]:
                    print(",",strAttr)
                else:
                    print()
            except:
                print()
        elif not prnt_complete:
            print()

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

        ans =  input("Press enter to display GPIO mapping, Q to exit now: ").upper()
        if ans != "Q":
            print()
            allpins = []
            for pin in dir(microcontroller.pin):
                if isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin):
                    pins = []
                    for alias in dir(board):
                        if getattr(board, alias) is getattr(microcontroller.pin, pin):
                            pins.append("board.{}".format(alias))
                        pins.sort()
                    pins = ["microcontroller."+pin] + pins
                    if len(pins)>0:
                        allpins.append(" ".join(pins))
            allpins.sort(key=lambda x:x[x.index('.')+1:].split(' ')[0])
            for pins in allpins:
                print(pins)            

    return

printPinAssignments()
