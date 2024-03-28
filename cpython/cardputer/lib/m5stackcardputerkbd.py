"""
`M5StackCardputerKbd`
====================================================

CircuitPython M5Stack Cardputer Matrix Keyboard driver.

* Author(s): foamyguy during YouTube livestream
             https://www.youtube.com/watch?v=la7g24fP7IQ&t=4s

             retiredwizard added modifier keys (shift, alt, ...) and minor performance changes

"""


import board
import keypad
import keypad_demux
import time

class Cardputer():
    def __init__(self):
        row_pins = (board.KB_A_0, board.KB_A_1, board.KB_A_2)
        column_pins = (
            board.KB_COL_0, board.KB_COL_1, board.KB_COL_2, board.KB_COL_3, board.KB_COL_4, board.KB_COL_5, board.KB_COL_6)

        self._KEY_MATRIX_LUT = [
            ("OPT","OPT","OPT"), ("z","Z",""), ("c","C",""), ("b","B",""),
            ("m","M",""), (".",">","DOWN"), (" "," "," "),
            ("SHIFT","SHIFT","SHIFT"), ("s","S",""), ("f","F",""), ("h","H",""),
            ("k","K",""), (";",":","UP"), ("\n","\n","\n"), 
            ("q","Q",""), ("e","E",""), ("t","T",""), ("u","U",""),
            ("o","O",""), ("[","{",""), ("\\","|",""), 
            ("1","!",""), ("3","#",""), ("5","%",""), ("7","&",""),
            ("9","(",""), ("_","-",""), ("\x08","\x08","\x08"), 
            ("CTRL","CTRL","CTRL"),
            ("ALT","ALT","ALT"), ("x","X",""), ("v","V",""), ("n","N",""),
            (",","<","LEFT"), ("/","?","RIGHT"),
            ("FN","FN","FN"),
            ("a","A",""), ("d","D",""), ("g","G",""), ("j","J",""),
            ("l","L",""), ("'",'"',""),
            ("\t","\t","\t"), 
            ("w","W",""), ("r","R",""), ("y","Y",""), ("i","I",""),
            ("p","P",""), ("]","}",""),
            ("`","~","\x1b"),
            ("2","@",""), ("4","$",""), ("6","^",""), ("8","*",""),
            ("0",")",""), ("=","+","")
        ]
        
        self.keyboard = keypad_demux.DemuxKeyMatrix(row_pins, column_pins)
        
        self._last_key_number = None
        self._pressedkey = None
        self._timestamp = None
        self._repeat_key = None
        self._repeat_started = False

        self.shift = False
        self.funct = False
        self.ctrl = False
        self.opt = False
        self.alt = False
        self.shift_lock = False
        self.funct_lock = False
        self._hold_modkey = False
        
    def check_keyboard(self):
        event = keypad.Event()
        new_char_buffer = ""

        while True:
            if self.keyboard.events.get_into(event):
                new_char = self._KEY_MATRIX_LUT[event.key_number][0]
                single_press = False
                if self._last_key_number == event.key_number:
                    single_press = True
                self._last_key_number = event.key_number

                if event.pressed:
                    if self._timestamp is None and self._pressedkey is None:
                        self._pressedkey = event.key_number
                        self._timestamp = int(time.monotonic_ns()/1000000)
                    elif event.key_number != self._pressedkey:
                        # Second key paressed, reset repeat timer
                        self._repeat_key = None
                        self._repeat_started = False

                    if new_char not in ['SHIFT','FN','CTRL','OPT','ALT']:
                        if self.shift:
                            new_char = self._KEY_MATRIX_LUT[event.key_number][1]
                            if not self._hold_modkey and not self.shift_lock:
                                self.shift = False
                        elif self.funct:
                            new_char = self._KEY_MATRIX_LUT[event.key_number][2]
                            if not self._hold_modkey and not self.funct_lock:
                                self.funct = False
                        elif self.opt:
                            if not self._hold_modkey:
                                self.opt = False
                        new_char_buffer += new_char

                        if self._timestamp is not None and self._repeat_key is None:
                            self._repeat_key = new_char
                    else:
                        self._hold_modkey = True
                        self._timestamp = None  # Don't repeat modifier keys
                        self._repeat_started = False
                        self._repeat_key = None
                        self._pressedkey = None # Allow next key to repeat
                        if new_char == "SHIFT":
                            if self.opt:
                                self.shift_lock = not self.shift_lock
                                self.shift = self.shift_lock
                                self.opt = False
                            else:
                                if not self.shift_lock:
                                    self.shift = not self.shift
                        elif new_char == "FN":
                            if self.opt:
                                self.funct_lock = not self.funct_lock
                                self.funct = self.funct_lock
                                self.opt = False
                            else:
                                if not self.funct_lock:
                                    self.funct = not self.funct
                        elif new_char == "CTRL":
                            self.ctrl = not self.ctrl
                        elif new_char == "OPT":
                            self.opt = not self.opt
                        elif new_char == "ALT":
                            self.alt = not self.alt
                else:
                    if event.key_number == self._pressedkey:
                        self._pressedkey = None
                        self._timestamp = None
                        self._repeat_started = False
                        self._repeat_key = None

                    if new_char in ['SHIFT','FN','CTRL','OPT','ALT']:
                        #print(f'shifted:{self.shift} hold:{self._hold_modkey} pressed:{self._pressedkey} time:{self._timestamp} repeat_started:{self._repeat_started} repeat_key:{self._repeat_key}')
                        self._hold_modkey = False
                        if not single_press:
                            if new_char == "SHIFT":
                                if self.opt and self.shift_lock:
                                    self.shift = False
                                    self.shift_lock = False
                                elif not self.shift_lock:
                                    self.shift = False
                            elif new_char == "FN":
                                if self.opt and self.funct_lock:
                                    self.funct = False
                                    self.funct_lock = False
                                elif not self.funct_lock:
                                    self.funct = False
                            elif new_char == "CTRL":
                                self.ctrl = False
                            elif new_char == "OPT":
                                self.opt = False
                            elif new_char == "ALT":
                                self.alt = False
            else:
                if new_char_buffer == "" and self._timestamp is not None:
                    hold_time = int(time.monotonic_ns()/1000000) - self._timestamp
                    if hold_time < 0:
                        self._timestamp = int(time.monotonic_ns()/1000000)
                        hold_time = int(time.monotonic_ns()/1000000)
                    if hold_time > 1000 or (hold_time > 100 and self._repeat_started):
                        if self._repeat_key is not None:
                            new_char_buffer = self._repeat_key
                        self._repeat_started = True
                        self._timestamp = int(time.monotonic_ns()/1000000)

                break

        return new_char_buffer

