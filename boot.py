"""CircuitPython Essentials Storage logging boot.py file"""
from sys import implementation
if implementation.name.upper() == "CIRCUITPYTHON":
    import board
    import digitalio
    import storage

# Changing the value of PyDOSReadOnly from False to True changes the behavior of this program.
# When PyDOSReadOnly is False the PyDOS file system will be set to Read/Write status for next
# power cycle unless a control GPIO is grounded (GP2,5 or 6 depending on the Microcontroller)
# in which case the host computer will have Read/Write access and PyDOS will have readonly access.

    # Changing PyDOSReadOnly to True will allow the host computer write access even if the
    # GPIO pin is not grounded.

    # If a grounding Pin is not available on the microcontroller, the PyDOS file system is set to
    # ReadOnly so the host file has access unless PyDOSReadOnly is set to True in which case
    # the PyDOS file system is set to Read/Write.

    PyDOSReadOnly = False

    if board.board_id == 'arduino_nano_rp2040_connect':
# For Gemma M0, Trinket M0, Metro M0/M4 Express, ItsyBitsy M0/M4 Express
        switch = digitalio.DigitalInOut(board.D2)
    elif board.board_id in ['raspberry_pi_pico','cytron_maker_pi_rp2040']:
        switch = digitalio.DigitalInOut(board.GP6)
    elif board.board_id == 'adafruit_qtpy_esp32c3':
        switch = digitalio.DigitalInOut(board.A1)
    elif board.board_id == 'adafruit_itsybitsy_rp2040':
        switch = digitalio.DigitalInOut(board.D7)
    else:
        if "D5" in dir(board):
            switch = digitalio.DigitalInOut(board.D5)
        elif "GP5" in dir(board):
            switch = digitalio.DigitalInOut(board.GP5)
        elif "IO5" in dir(board):
            switch = digitalio.DigitalInOut(board.IO5)
        elif "D6" in dir(board):
            switch = digitalio.DigitalInOut(board.D6)
        elif "GP6" in dir(board):
            switch = digitalio.DigitalInOut(board.GP6)
        elif "IO6" in dir(board):
            switch = digitalio.DigitalInOut(board.IO6)
        elif "D2" in dir(board):
            switch = digitalio.DigitalInOut(board.D2)
        elif "GP2" in dir(board):
            switch = digitalio.DigitalInOut(board.GP2)
        elif "IO2" in dir(board):
            switch = digitalio.DigitalInOut(board.IO2)
        else:
            switch = None


    if switch:
        switch.direction = digitalio.Direction.INPUT
        switch.pull = digitalio.Pull.UP

# If the switch pin is connected to ground (switch.value == False) allow host to write to the drive
        if switch.value == False:
            # Mounts so Host computer can write to micro-flash
            storage.remount("/", True)
            print("Switch False (pin grounded), PyDOS FS is ReadOnly")
        else:
            storage.remount("/", PyDOSReadOnly)
            print("Switch True (not grounded), ",end="")
            if PyDOSReadOnly:
                print("PyDOS FS is ReadOnly")
            else:
                print("PyDOS FS is ReadWrite")

        switch.deinit()
    else:
        print("No GPIO override pin found - set to Microcontroller access mode, PyDOS FS is ReadWrite")
        print("To set the PyDOS FS readonly and give the host write access enter the following command")
        print("at the PyDOS prompt: fs ro")
        storage.remount("/", PyDOSReadOnly )
elif implementation.name.upper() == "MICROPYTHON":
    from os import uname
    if uname().machine == 'Teensy 4.1 with MIMXRT1062DVJ6A':
        import uos, sys
        uos.umount("/flash")
        uos.mount(vfs,"/")
        sys.path.pop(-1)
        sys.path.pop(-1)
        sys.path.append("/")
        sys.path.append("/lib")
