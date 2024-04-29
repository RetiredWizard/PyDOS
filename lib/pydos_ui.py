"""
    Screen/Keyboard abstraction layer

"""
from sys import stdin,stdout,implementation
import select
if implementation.name.upper() == "CIRCUITPYTHON":
    import board
    if 'DISPLAY' in dir(board):
        try:
            import displayio
            import terminalio
        except:
            pass

class PyDOS_UI:

    def __init__(self):
        if implementation.name.upper() == "CIRCUITPYTHON" and 'DISPLAY' in dir(board):
            self.scrollable = False
        else:
            self.scrollable = True

    def serial_bytes_available(self,timeout=1):
        # Does the same function as supervisor.runtime.serial_bytes_available
        spoll = select.poll()
        spoll.register(stdin,select.POLLIN)

        retval = spoll.poll(timeout)
        spoll.unregister(stdin)

        if not retval:
            retval = 0
        else:
            retval = 1
        retval = 1 if retval else 0

        return retval

    def read_keyboard(self,num):
        # Does the same function as sys.stdin.read(num), blocking read
        return stdin.read(num)

    def get_screensize(self):
        try:
            height = round(board.DISPLAY.height/(terminalio.FONT.bitmap.height*displayio.CIRCUITPYTHON_TERMINAL.scale))-1
            width = round(board.DISPLAY.width/((terminalio.FONT.bitmap.width/95)*displayio.CIRCUITPYTHON_TERMINAL.scale))-2
        except:
            print("Screen set to 24 rows, 80 col. Press any key to continue...",end="")
            stdout.write('\x1b[2K')
            stdout.write('\x1b[999;999H\x1b[6n')
            pos = ''
            char = ''
            if self.serial_bytes_available(100):
                try:
                    char = stdin.read(1) ## expect ESC[yyy;xxxR
                except:
                    return(24,80)
            if char != '\x1b':
                return(24,80)

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

        return(height,width)

Pydos_ui = PyDOS_UI()
