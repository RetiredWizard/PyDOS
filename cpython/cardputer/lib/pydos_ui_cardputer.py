from sys import stdin,stdout

import board
import displayio
import terminalio
#from adafruit_display_text import bitmap_label as label
import time
from supervisor import runtime

import m5stackcardputerkbd as cardputer

class PyDOS_UI:

    def __init__(self):
        self.scrollable = False

        self.commandHistory = [""]
        self.arrow = ""

        self.kbd = cardputer.Cardputer()

        self._seqCnt = 0
    	self._key = ""
       	self._touched = False

#        self.CAPLOCK = False

#        self.display=board.DISPLAY
#        self._kbd_group = displayio.Group()
#        self.display.root_group = self._kbd_group
#        self._kbd_group.append(displayio.CIRCUITPYTHON_TERMINAL)

#        font = terminalio.FONT
#        self._shftIndicator = label.Label(font,text="",color=0x0000FF)
#        self._shftIndicator.x = 20
#        self._shftIndicator.y = 20
#        self._shftIndicator.scale = 2
#        self._kbd_group.append(self._shftIndicator)
#        self._fnIndicator = label.Label(font,text="",color=0xFF0000)
#        self._fnIndicator.x = 105
#        self._fnIndicator.y = 20
#        self._fnIndicator.scale = 2
#        self._kbd_group.append(self._fnIndicator)

    def get_screensize(self):
        return (
            round(board.DISPLAY.height/(terminalio.FONT.bitmap.height*displayio.CIRCUITPYTHON_TERMINAL.scale))-1,
            round(board.DISPLAY.width/((terminalio.FONT.bitmap.width/95)*displayio.CIRCUITPYTHON_TERMINAL.scale))-2
        )

    def serial_bytes_available(self):
        if not self._touched:
            retval = False

            self._key = self.kbd.check_keyboard()
            if self._key != "":
                retval = True
                self._touched = True

                if self._key in ['UP','DOWN','RIGHT','LEFT']:
                    self.arrow = 'ABCD'[['UP','DOWN','RIGHT','LEFT'].index(self._key)]
                    self._key = ""
            else:
                retval = self.uart_bytes_available()
        else:
            retval = True

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
                    retval += self._key
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
                if Pydos_ui.serial_bytes_available():
                    keys = keys[:editCol-1]+keys[editCol:]
                    if Pydos_ui.uart_bytes_available():
                        ctrlkeys = stdin.read(2)
                    else:
                        ctrlkeys = Pydos_ui.read_keyboard(2)
                    # ctrlkeys = up:[A down:[B right:[C left:[D
                    arrow = ctrlkeys[1]

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
