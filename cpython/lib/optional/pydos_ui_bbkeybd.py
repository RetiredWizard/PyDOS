"""
    Terminal abstraction layer for Keboard FeatherWing by @Arturo182 and @solderparty

"""

from bbq10keyboard import BBQ10Keyboard, STATE_PRESS, STATE_RELEASE, STATE_LONG_PRESS
import board
from pydos_hw import Pydos_hw

class PyDOS_UI:

    SHIFT = 1
    ALT = 2
    #_kbd = None

    def __init__(self):
        Pydos_hw.KFW = True
        self.kbd = BBQ10Keyboard(Pydos_hw.I2C(),BBQI2CDevice=Pydos_hw.I2CbbqDevice)

        self._contrl_seq = []

        self.shift_Lock = False
        self.shift_Mode = self.SHIFT # Default Cap lock/Long Press mode

        self.lastCmdLine = ""
        self.commandHistory = []

    def serial_bytes_available(self):
        # Does the same function as supervisor.runtime.serial_bytes_available
        try:
            sba = (self.kbd.key_count != 0)
        except:
            print("Trouble on startup, waiting a bit",end="")
            for i in range(100000):
                if i % 10000 == 0:
                    print (".",end="")
            print()
            sba = (self.kbd.key_count != 0)

        return sba


    def process_key(self,key,time_Param):
        # Modified the pressed key value per translation table or
        # held key modifications (shift for 3 seconds, alt for 6 seconds)

        altChars = {'q':'#', 'w':'1', 'e':'2', 'r':'3', 't':'(', 'y':')', 'u':'_', 'i':'-', 'o':'+', 'p':'@',
                    'a':'*', 's':'4', 'd':'5', 'f':'6', 'g':'/', 'h':':', 'j':';', 'k':"'", 'l':'"',
                    'z':'7', 'x':'8', 'c':'9', 'v':'?', 'b':'!', 'n':',', 'm':'.', '$':'=', '~':'0'}

        if time_Param == None and not self.shift_Lock:
            if key == '\x60': # change speaker symbol to equal sign
                retVal = '='
            elif key == '~': # change microphone symbol to left bracket
                retVal = '['
            else:
                retVal = key
        elif self.shift_Mode == self.SHIFT:
            if key == '~':
                retVal = ']'
            elif key == '$':
                retVal = '%'
            else:
                if key != key.upper():
                    retVal = key.upper()
                else:
                    retVal = key.lower()
            print(retVal+'\x08',end="")
        elif self.shift_Mode == self.ALT:
            retVal = altChars.get(key,key)
            print(retVal+'\x08',end="")

        return retVal

    def read_keyboard(self,num):
        # Does the same function as sys.stdin.read(num)
        input_text = ""

        while self.kbd.key_count == 0 and len(self._contrl_seq) == 0:
            pass

        while num > 0:
            if len(self._contrl_seq) > 0:
                input_text += self._contrl_seq.pop(0)
                num -= 1
            else:
                k = self.kbd.key
                if k != None:
                    if k[0] == STATE_RELEASE:
                        if k[1] == '\x01':   # Up Arrow - emulate terminal behavior
                            self._contrl_seq = ['\x5b','\x41']
                            input_text += '\x1b'
                            num -= 1
                        elif k[1] == '\x02': # Down Arrow - emulate terminal behavior
                            self._contrl_seq = ['\x5b','\x42']
                            input_text += '\x1b'
                            num -= 1
                        else:
                            input_text += k[1]
                            num -= 1

        return input_text

    def get_screensize(self):
        return(19,54)

Pydos_ui = PyDOS_UI()

def input(disp_text=None):
    # Does the same function as input(disp_text)
    input_text = ""

    # There seems to be an initial timing issue so running this
    # extra key_count seems to avoid random startup crashes

    try:
        Pydos_ui.kbd.key_count
    except:
        print("Trouble on startup, waiting a bit",end="")
        for i in range(100000):
            if i % 10000 == 0:
                print (".",end="")
        print()

    if Pydos_ui.kbd.key_count != 0:
        while Pydos_ui.kbd.key_count != 0:
            Pydos_ui.kbd.key

    if disp_text != None:
        print(disp_text,end='')

    while Pydos_ui.kbd.key_count == 0:
        pass

    k = Pydos_ui.kbd.key
    histPntr = len(Pydos_ui.commandHistory)
    currEditLine = Pydos_ui.lastCmdLine
    loop = True
    time_Param = None
    while loop:
        if k != None:
            if k[0] == STATE_RELEASE:
                if k[1] not in  '\n\x07\x11\x01\x02':
                    if k[1] == '\x08': # Backspace
                        if len(input_text) > 0:
                            input_text = input_text[:-1]
                            print(k[1]+" "+k[1],end="")
                    elif k[1] == '\x09': # Alt-Space toggles the Shift/Alt lock on or off
                        Pydos_ui.shift_Lock = not Pydos_ui.shift_Lock
                    elif k[1] == '\x7c': # Alt-Enter toggles between Shift & Alt for long press
                        if Pydos_ui.shift_Mode == Pydos_ui.SHIFT:
                            Pydos_ui.shift_Mode = Pydos_ui.ALT
                        else:
                            Pydos_ui.shift_Mode = Pydos_ui.SHIFT
                    else: # Anything else, we add to the text field
                        retKey = Pydos_ui.process_key(k[1],time_Param)
                        input_text += retKey
                        time_Param = None
                        print(retKey,end="")
                elif k[1] == '\x01': # Up Arrow
                    if len(Pydos_ui.commandHistory) > 0:
                        print('\x08'*(len(input_text))+" "*(len(input_text))+'\x08'*(len(input_text)),end="")

                        histPntr -= 1
                        if histPntr < 0:
                            histPntr = len(Pydos_ui.commandHistory) - 1
                        print(Pydos_ui.commandHistory[histPntr],end="")
                        input_text = Pydos_ui.commandHistory[histPntr]
                        currEditLine = input_text
                elif k[1] == '\x02': # Down Arrow
                    if len(Pydos_ui.commandHistory) > 0:
                        print('\x08'*(len(input_text))+" "*(len(input_text))+'\x08'*(len(input_text)),end="")

                        histPntr += 1
                        if histPntr >= len(Pydos_ui.commandHistory):
                            histPntr = 0
                        print(Pydos_ui.commandHistory[histPntr],end="")
                        input_text = Pydos_ui.commandHistory[histPntr]
                        currEditLine = input_text
                elif k[1] == '\x07': # F3 pressed

                    print(currEditLine[len(input_text):],end="")
                    input_text += currEditLine[len(input_text):]
                elif k[1] == '\x11': # F2 Pressed
                    searchLoc = currEditLine[len(input_text):].find(Pydos_ui.read_keyboard(1))
                    if searchLoc >= 0:
                        print(currEditLine[len(input_text):len(input_text)+searchLoc],end="")
                        input_text += currEditLine[len(input_text):len(input_text)+searchLoc]
                else: # Enter pressed
                    print()
                    if input_text != "":
                        Pydos_ui.lastCmdLine = input_text
                        Pydos_ui.commandHistory.append(input_text)
                        if len(Pydos_ui.commandHistory) > 10:
                            Pydos_ui.commandHistory.pop(0)
                    loop = False
            elif k[0] == STATE_LONG_PRESS:
                if k[1] not in '\x08\x09\x7c':
                    time_Param = STATE_LONG_PRESS
                    Pydos_ui.process_key(k[1],time_Param)

        if loop:
            k = Pydos_ui.kbd.key

    return input_text
