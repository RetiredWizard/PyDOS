from sys import stdin,stdout,implementation

import board
from supervisor import runtime
from pydos_hw import Pydos_hw
from adafruit_bus_device.i2c_device import I2CDevice
import countio
import keypad
import time

class PyDOS_UI:

    def __init__(self):
    	self._key = bytearray(1)
       	self._touched = False
       	_ADDRESS_KBD = 0x55

        self.commandHistory = [""]

       	self._i2c = I2CDevice(Pydos_hw.I2C(), _ADDRESS_KBD)
        self.trackball = {
            "A": countio.Counter(board.TRACKBALL_UP),
            "B": countio.Counter(board.TRACKBALL_DOWN),
            "C": countio.Counter(board.TRACKBALL_RIGHT),
            "D": countio.Counter(board.TRACKBALL_LEFT)
        }
        self.click = keypad.Keys([board.TRACKBALL_CLICK], value_when_pressed=False)

    def get_screensize(self):
        #return (round(self._display.height*.04),round(self._display.width*.0817))
        #return (
        #    round(self._display.height/(terminalio.FONT.bitmap.height*displayio.CIRCUITPYTHON_TERMINAL.scale))-1,
        #    round(self._display.width/((terminalio.FONT.bitmap.width/95)*displayio.CIRCUITPYTHON_TERMINAL.scale))-1
        #)
        return (19,53)

    def serial_bytes_available(self):
        if not self._touched:
            retval = 0
            with self._i2c as i2c:
                try:
                    i2c.readinto(self._key)
                except:
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
                retval = chr(self._key[0])
                self._touched = False
                num -= 1
            else:
                if self.uart_bytes_available():
                    retval = stdin.read(1)
                    num -= 1

        return retval

Pydos_ui = PyDOS_UI()

def input(disp_text=None):

    if disp_text != None:
        print(disp_text,end="")

    bld_chr1 = '_(+'
    bld_chr2 = '-+)'
    bld_chr =  '=[]'
    bld_started = False

    histPntr = len(Pydos_ui.commandHistory)

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
            trackloop = True
        else:
            ctrlkeys = ''
            trackloop = False

        # Find the last direction the trackball was moved
        #  and wait for trackball to stop moving
        largestDir = 0
        while trackloop:
            trackloop = False
            for p,c in Pydos_ui.trackball.items():
                if c.count > largestDir:
                    trackloop = True
                    if p not in "AB" or onLast:
                        arrow = p
                        largestDir = c.count
                    c.reset()
                else:
                    c.reset()
            if arrow != "" and not trackloop:
                time.sleep(.05)
                # clear all counters
                for p,c in Pydos_ui.trackball.items():
                    if c.count > 0:
                        c.reset()

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

        if Pydos_ui.serial_bytes_available():
            if Pydos_ui.uart_bytes_available():
                keys = keys[:editCol]+stdin.read(1)+keys[editCol:]
                editCol += 1
                if keys[editCol-1] == '\x1b':
                    keys = keys[:editCol-1]+keys[editCol:]
                    ctrlkeys = stdin.read(2)
                    # ctrlkeys = up:[A down:[B right:[C left:[D
                    arrow = ctrlkeys[1]
            else:
                keys = keys[:editCol]+Pydos_ui.read_keyboard(1)+keys[editCol:]
                editCol += 1

            # Convert two character sequences into missing keyboard keys
            # '_-' -> '='     '(+' -> '['       '+)' -> ']'
            bld_done = False
            bcindx = bld_chr2.find(keys[editCol-1:editCol])
            if bld_chr1.find(keys[editCol-1:editCol]) != -1 and not bld_started and arrow == "":
                bld_started = True
            elif keys[editCol-2:editCol] ==  bld_chr1[bcindx]+bld_chr2[bcindx] and bld_started:
                bld_started = False
                keys = keys[:editCol-2]+bld_chr[bcindx]+keys[editCol:]
                print('\x08'+keys[editCol-2:]+' '+('\x08'*(len(keys[editCol:])+(1 if onLast else 2))),end="")
                editCol -= 1
                bld_done = True
            else:
                bld_started = False
                
            if arrow != "" and ctrlkeys != "":
                editCol -= 1
            elif arrow !='':
                pass
            elif keys[editCol-1:editCol] == '\x08':
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
