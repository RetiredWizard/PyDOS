"""
    Screen/Keyboard abstraction layer

"""
from sys import stdin,stdout,implementation
if implementation.name.upper() == "MICROPYTHON":
    import uselect
elif implementation.name.upper() == "CIRCUITPYTHON":
    from supervisor import runtime

class PyDOS_UI:

    def __init__(self):
        pass

    def serial_bytes_available(self):
        if implementation.name.upper() == "CIRCUITPYTHON":
            # Does the same function as supervisor.runtime.serial_bytes_available
            retval = runtime.serial_bytes_available

        elif implementation.name.upper() == "MICROPYTHON":
            spoll = uselect.poll()
            spoll.register(stdin,uselect.POLLIN)

            retval = spoll.poll(0)
            spoll.unregister(stdin)

            if not retval:
                retval = 0

        return retval

    def read_keyboard(self,num):
        # Does the same function as sys.stdin.read(num), blocking read
        return stdin.read(num)

    def get_screensize(self):
        print("Screen set to 24 rows, 80 col. Press any key to coninue...",end="")
        stdout.write('\x1b[2K')
        stdout.write('\x1b[999;999H\x1b[6n')
        pos = ''
        char = ''
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
