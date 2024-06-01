from sys import stdin,stdout,implementation

import board
import keypad
import time
from supervisor import runtime
from pydos_hw import Pydos_hw
from adafruit_bus_device.i2c_device import I2CDevice

class PyDOS_UI:

    def __init__(self):
        self.trackevent = None
        self.scrollable = False
        self.arrow = ""
        self._cmdhistlock = False
        self._seqCnt = 0
    	self._key = bytearray(1)
       	self._touched = False
       	_ADDRESS_KBD = 0x55

        self.commandHistory = [""]

       	self._i2c = I2CDevice(Pydos_hw.I2C(), _ADDRESS_KBD)
        self.trackball = keypad.Keys(
            [
                board.TRACKBALL_CLICK,
                board.TRACKBALL_UP,
                board.TRACKBALL_DOWN,
                board.TRACKBALL_LEFT,
                board.TRACKBALL_RIGHT
            ],
            value_when_pressed=False
        )

    def get_screensize(self):
        return (19,51)

    def serial_bytes_available(self):
        if not self._touched:
            retval = 0

            # Find the last direction the trackball was moved
            #  and wait for trackball to stop moving
            self.arrow = ''
            self.trackevent = Pydos_ui.trackball.events.get()
            if self.trackevent and (self.trackevent.key_number not in [1,2] or not self._cmdhistlock):
                self.arrow = ' ABDC'[self.trackevent.key_number]
                if self.arrow == " ":
                    self.arrow = ""
                else:
                    retval = 1
                    self._touched = True

            if not self._touched:
                with self._i2c as i2c:
                    try:
                        i2c.readinto(self._key)
                    except Exception as err:
                        self._key=bytearray(1)
                if self._key[0] != 0:
                    retval = 1
                    self._touched = True
                else:
                    retval = self.uart_bytes_available()
        else:
            retval = 1

        return retval

    def uart_bytes_available(self):
        # Does the same function as supervisor.runtime.serial_bytes_available
        retval = runtime.serial_bytes_available

        return retval

    def read_keyboard(self,num):
        retval = ""
        while num > 0:
            self.serial_bytes_available()
            if self._touched:
                if self.arrow != "":
                    if self._seqCnt == 0:
                        retval += chr(27)
                        self._seqCnt = 1
                        num -= 1
                    elif self._seqCnt == 1:
                        retval += chr(91)
                        self._seqCnt = 2
                        num -= 1
                    elif self._seqCnt == 2:
                        retval += self.arrow
                        self._seqCnt = 0
                        self._touched = False
                        self.arrow = ""
                        num -= 1
                else:
                    retval += chr(self._key[0])
                    self._touched = False
                    num -= 1
            else:
                if self.uart_bytes_available():
                    retval = stdin.read(num)
                    num -= len(retval)

        return retval

Pydos_ui = PyDOS_UI()

def input(disp_text=None):

    if disp_text != None:
        print(disp_text,end="")

    bld_chr1 = '_(+(-__-'
    bld_chr2 = '-+)-)/#/'
    bld_chr =  '=[]<>\^%'
    bld_started = False

    histPntr = len(Pydos_ui.commandHistory)
    Pydos_ui._cmdhistlock = False

    keys = ''
    editCol = 0
    loop = True
    ctrlkeys = ''
    arrow = ''
    onLast = True
    onFirst = True
    blink = True
    timer = time.time()

    while loop:
        #print(editCol,keys)
        if ctrlkeys == '':
            arrow = ""
        else:
            ctrlkeys = ''

        if arrow == 'A' or arrow == 'B':
            if len(Pydos_ui.commandHistory) > 0:
                print(('\x08'*(editCol))+(" "*(len(keys)+1))+('\x08'*(len(keys)+1)),end="")

                if arrow == 'A':
                    histPntr -= 1
                else:
                    histPntr += 1

                histPntr = histPntr % len(Pydos_ui.commandHistory)
                print(Pydos_ui.commandHistory[histPntr],end="")
                keys = Pydos_ui.commandHistory[histPntr]
                editCol = len(keys)
                if editCol == 0:
                    onFirst = True
                else:
                    onFirst = False
        elif arrow == 'D':
            Pydos_ui._cmdhistlock = True
            if len(keys) > editCol:
                print(keys[editCol:editCol+1]+"\x08",end="")
            elif editCol == len(keys):
                print(" \x08",end="")

            editCol = max(0,editCol-1)
            if editCol > 0:
                print('\x08',end="")
                onLast = False
            elif editCol == 0:
                if not onFirst:
                    print('\x08',end="")
                    onFirst = True
        elif arrow == 'C':
            if len(keys) > editCol:
                print(keys[editCol:editCol+1]+"\x08",end="")

            editCol += 1
            editCol = min(len(keys),editCol)
            if editCol < len(keys):
                print(keys[editCol-1:editCol],end="")
                onFirst = False
            elif editCol == len(keys):
                if not onLast:
                    print(keys[editCol-1:],end="")
                    onLast = True
                    Pydos_ui._cmdhistlock = False

        if Pydos_ui.serial_bytes_available():
            if Pydos_ui.uart_bytes_available():
                keys = keys[:editCol]+stdin.read(1)+keys[editCol:]
            else:
                keys = keys[:editCol]+Pydos_ui.read_keyboard(1)+keys[editCol:]

            editCol += 1
            if keys[editCol-1] == '\x1b':
                keys = keys[:editCol-1]+keys[editCol:]
                if Pydos_ui.uart_bytes_available():
                    ctrlkeys = stdin.read(2)
                else:
                    ctrlkeys = Pydos_ui.read_keyboard(2)
                # ctrlkeys = up:[A down:[B right:[C left:[D
                arrow = ctrlkeys[1]

            # Convert two character sequences into missing keyboard keys
            # '_-' -> '='     '(+' -> '['       '+)' -> ']'
            bld_done = False
            if bld_started:

                bcindx = bld_chr2.find(keys[editCol-1:editCol])
                nextbc = 0
                while nextbc != -1 and bld_started:
                    if keys[editCol-2:editCol] ==  bld_chr1[bcindx]+bld_chr2[bcindx]:
                        bld_started = False
                        bld_done = True
                        keys = keys[:editCol-2]+bld_chr[bcindx]+keys[editCol:]
                        print('\x08'+keys[editCol-2:]+' '+('\x08'*(len(keys[editCol:])+(1 if onLast else 2))),end="")
                        editCol -= 1
                    else:
                        nextbc = bld_chr2[bcindx+1:].find(keys[editCol-1:editCol])
                        bcindx = bcindx + nextbc + 1

            if bld_chr1.find(keys[editCol-1:editCol]) != -1 and arrow == "" and not bld_done:
                bld_started = True
            else:
                bld_started = False
                
            if arrow != "" and ctrlkeys != "":
                editCol -= 1
            elif arrow !='':
                pass
            elif keys[editCol-1:editCol] in ['\x08','\x7f']:
                keys = keys[:max(0,editCol-2)]+keys[editCol:]
                if editCol > 1:
                    print(('\x08'*(editCol-1))+keys+'  \x08\x08',end="")
                    editCol = max(0,editCol-2)
                    if editCol < len(keys):
                        print("\x08"*(len(keys)-editCol),end="")
                else:
                    editCol -= 1
                    onFirst = True
            elif len(keys[editCol-1:editCol]) > 0 and keys[editCol-1:editCol] in '\n\r':
                if len(keys) > editCol:
                    print(keys[editCol:editCol+1]+"\x08",end="")
                elif editCol == len(keys):
                    print(" \x08",end="")
                keys = keys[:editCol-1]+keys[editCol:]
                if keys.strip() != "":
                    Pydos_ui.commandHistory.append(keys)
                    if len(Pydos_ui.commandHistory) > 10:
                        Pydos_ui.commandHistory.pop(1)
                    histPntr = len(Pydos_ui.commandHistory)
                print()
                loop = False
            elif not bld_done:
                onFirst = False
                print(keys[editCol-1:],end="")
                if len(keys[editCol-1:]) > 1:
                    print(" \x08",end="")
                if editCol < len(keys):
                    print("\x08"*(len(keys)-editCol),end="")

        if loop:
            if time.time() != timer:
                blink = not blink
                timer = time.time()

            if blink:
                print("_\x08",end="")
            else:
                if len(keys) > editCol:
                    print(keys[editCol:editCol+1]+"\x08",end="")
                else:
                    print(" \x08",end="")

    return keys
