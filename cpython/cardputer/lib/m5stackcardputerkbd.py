"""
`M5StackCardputerKbd`
====================================================

CircuitPython M5Stack Cardputer Matrix Keyboard driver.

* Author(s): foamyguy during YouTube livestream
             https://www.youtube.com/watch?v=la7g24fP7IQ&t=4s

             retiredwizard added modifier keys (shift, alt, ...) and minor performance changes

"""


import board
import digitalio
import keypad
from adafruit_debouncer import Debouncer
#import time

class MultiplexerKeys():

    def __init__(self,multiplexed_row_pins, column_pins, value_when_pressed=False):
        self.row_pins = multiplexed_row_pins
        self.column_pins = column_pins
        self.row_dio_objs = []
        self.col_dio_objs = []
        
        # Initialize the row pins as outputs
        for row_pin in self.row_pins:
            _cur_dio = digitalio.DigitalInOut(row_pin)
            _cur_dio.direction = digitalio.Direction.OUTPUT
            self.row_dio_objs.append(_cur_dio)
            
        # Initialize the colun pins as inputs with pull-ups
        for column_pin in self.column_pins:
            _cur_dio = digitalio.DigitalInOut(column_pin)
            _cur_dio.direction = digitalio.Direction.INPUT
            _cur_dio.pull = digitalio.Pull.UP
            self.col_dio_objs.append(Debouncer(_cur_dio,.1))
#            self.col_dio_objs.append(_cur_dio)
        
        self.value_when_pressed = value_when_pressed
        
        self._events = []
        self._last_key = None
        
    @property
    def events(self):
        self._scan()
        return self._events
    
# Function to scan the key matrix
    def _scan(self):
        self._events = []
        key_num = -1   # Set so held button can be differentiated from no key pressed
        for i in range(8):
            self.set_multiplexer_state(i)
            for col, column_pin in enumerate(self.col_dio_objs):
                column_pin.update()
                column_pin.update()
                while column_pin.state not in [0,3]:
                    column_pin.update()
                if column_pin.value == self.value_when_pressed:  # If a key is pressed
                    key_num = (i * len(self.col_dio_objs)) + col
                    #print("Key ({}, {:03b}, {}) pressed".format(key_num, i, col))
                    self._events.append(keypad.Event(key_number=key_num, pressed=True))
                    self._last_key = key_num
#                    time.sleep(.1)
        if key_num == -1:    # No keys pressed
            if self._last_key is not None:
                self._events.append(keypad.Event(key_number=self._last_key, pressed=False))
                self._last_key = None
#                time.sleep(.1)

    def set_multiplexer_state(self, state_binary):
        for idx, compare in enumerate((0b100,0b010,0b001)):
            self.row_dio_objs[idx].value = True if state_binary & compare else False
    
class Cardputer():
    def __init__(self):
        row_pins = (board.KB_A_0, board.KB_A_1, board.KB_A_2)
        column_pins = (
            board.KB_COL_0, board.KB_COL_1, board.KB_COL_2, board.KB_COL_3, board.KB_COL_4, board.KB_COL_5, board.KB_COL_6)

        self._KEY_MATRIX_LUT = [
            # row 4
            ("OPT","",""), ("z","Z",""), ("c","C",""), ("b","B",""),
            ("m","M",""), (".",">","DOWN"), (" ","",""), ("CTRL","",""),
            ("ALT","",""), ("x","X",""), ("v","V",""), ("n","N",""),
            (",","<","LEFT"), ("/","?","RIGHT"),
            
            # row 2
            ("q","Q",""), ("e","E",""), ("t","T",""), ("u","U",""),
            ("o","O",""), ("[","{",""), ("\\","|",""), ("\t","",""), 
            ("w","W",""), ("r","R",""), ("y","Y",""), ("i","I",""),
            ("p","P",""), ("]","}",""),
            
            # row 3
            ("SHIFT","",""), ("s","S",""), ("f","F",""), ("h","H",""),
            ("k","K",""), (";",":","UP"), ("\n","",""), ("FN","",""),
            ("a","A",""), ("d","D",""), ("g","G",""), ("j","J",""),
            ("l","L",""), ("'",'"',""),
            
            # row 1
            ("1","!",""), ("3","#",""), ("5","%",""), ("7","&",""),
            ("9","(",""), ("_","-",""), ("\x08","",""), ("`","~","\x1b"),
            ("2","@",""), ("4","$",""), ("6","^",""), ("8","*",""),
            ("0",")",""), ("=","+","")
        ]
        
        self.keyboard = MultiplexerKeys(row_pins, column_pins)
        
        self.shift = False
        self.funct = False
        self.ctrl = False
        self.opt = False
        self.alt = False
        
    def check_keyboard(self):
        events = self.keyboard.events
        new_char_buffer = ""
        if events:
            for event in events:
                if event.pressed:
                    new_char = self._KEY_MATRIX_LUT[event.key_number][0]
                    if new_char in ['SHIFT','FN','CTRL','OPT','ALT']:
                        new_char = ""
                    else:
                        if self.shift:
                            new_char = self._KEY_MATRIX_LUT[event.key_number][1]
                            self.shift = False
                        elif self.funct:
                            new_char = self._KEY_MATRIX_LUT[event.key_number][2]
                            self.funct = False
                        #new_char_buffer += new_char    # Replaced so only last char if multiple events
                        new_char_buffer = new_char      # (multiple keys simultaneously pressed)
                        
                else:
                # For modifer keys disable auto-repeat by only responding to "RELEASE" events
                    new_char = self._KEY_MATRIX_LUT[event.key_number][0]
                    if new_char == "SHIFT":
                        self.shift = not self.shift
                    elif new_char == "FN":
                        self.funct = not self.funct
                    elif new_char == "CTRL":
                        self.ctrl = not self.ctrl
                    elif new_char == "OPT":
                        self.opt = not self.opt
                    elif new_char == "ALT":
                        self.alt = not self.alt
                    

        return new_char_buffer

# Exmple Usage:
#
#cardputer = Cardputer()

#while True:
#    print(cardputer.check_keyboard(),end="")

