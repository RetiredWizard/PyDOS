"""CircuitPython Essentials Storage logging boot.py file"""
from sys import implementation
if implementation.name.upper() == "CIRCUITPYTHON":
    import board
    import digitalio
    import storage

# PyDOSReadOnly of False sets the PyDOS file system to Read/Write status for next power cycle
# This selection is ignored if D2 is grounded, if so the PyDOS file system is set to readonly
# giving the host computer write access to the flash

    PyDOSReadOnly = False

    if board.board_id == 'arduino_nano_rp2040_connect':
# For Gemma M0, Trinket M0, Metro M0/M4 Express, ItsyBitsy M0/M4 Express
        switch = digitalio.DigitalInOut(board.D2)
    elif board.board_id == 'raspberry_pi_pico':
        switch = digitalio.DigitalInOut(board.GP6)
    else:
        switch = digitalio.DigitalInOut(board.D5)

    switch.direction = digitalio.Direction.INPUT
    switch.pull = digitalio.Pull.UP

# If the switch pin is connected to ground (switch.value == False) allow host to write to the drive
    if switch.value == False:
        # Mounts so Host computer can write to micro-flash
        storage.remount("/", True)
        print("Switch False (pin grounded), FS is ReadOnly")
    else:
        storage.remount("/", PyDOSReadOnly)
        print("Switch True (not grounded), ",end="")
        if PyDOSReadOnly:
            print("FS is ReadOnly")
        else:
            print("FS is ReadWrite")

    switch.deinit()