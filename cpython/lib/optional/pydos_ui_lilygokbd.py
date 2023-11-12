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

        self.lastCmdLine = ""
        self.commandHistory = []

       	self._i2c = I2CDevice(Pydos_hw.I2C(), _ADDRESS_KBD)
        self.trackball = {
            "up": countio.Counter(board.TRACKBALL_UP),
            "down": countio.Counter(board.TRACKBALL_DOWN),
            "left": countio.Counter(board.TRACKBALL_LEFT),
            "right": countio.Counter(board.TRACKBALL_RIGHT)
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

        return retval

Pydos_ui = PyDOS_UI()

def input(disp_text=None):

    if disp_text != None:
        print(disp_text,end="")

    keys = ''
    editCol = 0
    histPntr = len(Pydos_ui.commandHistory)
    currEditLine = Pydos_ui.lastCmdLine
    loop = True
    ctrlkeys = ''
    arrow = ''
    onLast = True
    onFirst = True
    blink = True
    timer = time.time()

    while loop:
        #print(editCol,keys)
        # Find the last direction the trackball was moved
        #  and wait for trackball to stop moving
        if ctrlkeys == '':
            arrow = ""
            trackloop = True
        else:
            ctrlkeys = ''
            trackloop = False

        largestDir = 0
        while trackloop:
            trackloop = False
            for p,c in Pydos_ui.trackball.items():
                if c.count > largestDir:
                    trackloop = True
                    arrow = p
                    largestDir = c.count
                    c.reset()
                else:
                    c.reset()
            if arrow != "" and not trackloop:
                #time.sleep(.2)
                # clear all counters
                for p,c in Pydos_ui.trackball.items():
                    if c.count > 0:
                        c.reset()

        if arrow == 'up':
            if len(Pydos_ui.commandHistory) > 0:
                print('\x08'*(editCol)+" "*(len(keys))+'\x08'*(len(keys)),end="")

                histPntr -= 1
                if histPntr < 0:
                    histPntr = len(Pydos_ui.commandHistory) - 1
                print(Pydos_ui.commandHistory[histPntr],end="")
                keys = Pydos_ui.commandHistory[histPntr]
                currEditLine = keys
                editCol = len(keys)
                onFirst = False
        elif arrow == 'down':
            if len(Pydos_ui.commandHistory) > 0:
                print('\x08'*(editCol)+" "*(len(keys))+'\x08'*(len(keys)),end="")

                histPntr += 1
                if histPntr >= len(Pydos_ui.commandHistory):
                    histPntr = 0
                print(Pydos_ui.commandHistory[histPntr],end="")
                keys = Pydos_ui.commandHistory[histPntr]
                currEditLine = keys
                editCol = len(keys)
                onFirst = False
        elif arrow == 'left':
            if len(keys) > editCol:
                print(keys[editCol:editCol+1]+"\x08",end="")
            elif editCol == len(keys):
                print(" \x08",end="")

            editCol += 1
            editCol = max(0,editCol-2)
            if editCol > 0:
                print('\x08',end="")
                onLast = False
            elif editCol == 0:
                if not onFirst:
                    print('\x08',end="")
                    onFirst = True
        elif arrow == 'right':
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

        if Pydos_ui.uart_bytes_available() or Pydos_ui.serial_bytes_available():
            if Pydos_ui.uart_bytes_available():
                keys = keys[:editCol]+stdin.read(1)+keys[editCol:]
                editCol += 1
                if keys[editCol-1] == '\x1b':
                    keys = keys[:editCol-1]+keys[editCol:]
                    ctrlkeys = stdin.read(2)
                    if ctrlkeys == '[A':
                        keys += ' '
                        arrow = 'up'
                    elif ctrlkeys == '[B':
                        keys += ' '
                        arrow = 'down'
                    elif ctrlkeys == '[C':
                        arrow = 'right'
                        #editCol = min(len(keys),editCol)
                    elif ctrlkeys == '[D':
                        arrow = 'left'
                        #editCol = max(0,editCol-2)
            else:
                keys = keys[:editCol]+Pydos_ui.read_keyboard(1)+keys[editCol:]
                editCol += 1

            if keys[editCol-1:editCol] == '\x08':
                keys = keys[:max(0,editCol-2)]+keys[editCol:]
                if editCol > 1:
                    print(('\x08'*(editCol-1))+keys+'  \x08\x08',end="")
                    editCol = max(0,editCol-2)
                    if editCol < len(keys):
                        print("\x08"*(len(keys)-editCol),end="")
                else:
                    editCol -= 1
                    onFirst = True
            elif arrow == 'left':
                editCol -= 1
            elif arrow == 'right':
                editCol -= 1
            elif len(keys[editCol-1:editCol]) > 0 and keys[editCol-1:editCol] in '\n\r':
                if len(keys) > editCol:
                    print(keys[editCol:editCol+1]+"\x08",end="")
                elif editCol == len(keys):
                    print(" \x08",end="")
                keys = keys[:editCol-1]+keys[editCol:]
                Pydos_ui.commandHistory.append(keys)
                if len(Pydos_ui.commandHistory) > 10:
                    Pydos_ui.commandHistory.pop(0)
                print()
                loop = False
            else:
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