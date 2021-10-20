"""
    Terminal abstraction layer for USB UART

"""
from sys import stdin,stdout

class PyDOS_UI:

    def __init__(self):
        pass

    def read_keyboard(self,num):
        # Does the same function as sys.stdin.read(num)
        # Reads num characters from keyboard and returns
        # This is a blocking read, ie the program will wait for the input
        return stdin.read(num)

    def get_screensize(self):
        stdout.write('\x1b[999;999H\x1b[6n')
        pos = ''
        char = stdin.read(1) ## expect ESC[yyy;xxxR
        while char != 'R':
            pos += char
            char = stdin.read(1)
        print()

        width = int(pos.lstrip("\n\x1b[").split(';')[1],10)
        height = int(pos.lstrip("\n\x1b[").split(';')[0],10)

        if width < 1:
            width = 80
        if height < 1:
            height = 24

        return(width,height)

Pydos_ui = PyDOS_UI()
