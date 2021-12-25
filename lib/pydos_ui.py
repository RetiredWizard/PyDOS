"""
    Terminal abstraction layer for USB UART

"""
from sys import stdin,stdout,implementation
if implementation.name.upper() == "MICROPYTHON":
    import uselect
elif implementation.name.upper() == "CIRCUITPYTHON":
    from supervisor import runtime
    import digitalio
    import board
    if board.board_id == "cytron_maker_pi_rp2040":
        import busio

class PyDOS_UI:

    _I2C = None
    _I2C_power = None

    def __init__(self):
        pass

    if implementation.name.upper() == "CIRCUITPYTHON":

        def serial_bytes_available(self):
            # Does the same function as supervisor.runtime.serial_bytes_available
            return runtime.serial_bytes_available

        def I2C():
            if board.board_id == "cytron_maker_pi_rp2040":
                if not PyDOS_UI._I2C:
                    # Grove #1, GP1 & GP2
                    PyDOS_UI._I2C = busio.I2C(board.GP1, board.GP0)

                return PyDOS_UI._I2C
            else:
                if 'I2C_POWER_INVERTED' in dir(board) and not PyDOS_UI._I2C_power:
                    PyDOS_UI._I2C_power = digitalio.DigitalInOut(board.I2C_POWER_INVERTED)
                    PyDOS_UI._I2C_power.direction = digitalio.Direction.OUTPUT
                    PyDOS_UI._I2C_power.value = False

                return board.I2C()

    elif implementation.name.upper() == "MICROPYTHON":
        def serial_bytes_available(self):

            spoll = uselect.poll()
            spoll.register(stdin,uselect.POLLIN)

            retval = spoll.poll(0)
            spoll.unregister(stdin)

            if not retval:
                retval = 0

            return retval

    def read_keyboard(self,num):
        # Does the same function as sys.stdin.read(num)
        # Reads num characters from keyboard and returns
        # This is a blocking read, ie the program will wait for the input
        return stdin.read(num)

    def get_screensize(self):
        print("Press any key...",end="")
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
