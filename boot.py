"""CircuitPython Essentials Storage logging boot.py file"""
from sys import implementation
if implementation.name.upper() == "CIRCUITPYTHON":
    import board
    import digitalio
    import storage

# The PyDOS file system will be set to Read/Write status for next
# power cycle unless a control GPIO is grounded (GP2,5 or 6 depending on the Microcontroller)
# in which case the host computer will have Read/Write access and PyDOS will have readonly access.

    if board.board_id == 'arduino_nano_rp2040_connect':
        swpin = board.D2
    elif board.board_id in ['raspberry_pi_pico','cytron_maker_pi_rp2040']:
        swpin = board.GP6
    elif board.board_id == 'adafruit_qtpy_esp32c3':
        swpin = board.A1
    elif board.board_id == 'adafruit_itsybitsy_rp2040':
        swpin = board.D7
    else:
        if "D5" in dir(board):
            swpin = board.D5
        elif "GP5" in dir(board):
            swpin = board.GP5
        elif "IO5" in dir(board):
            swpin = board.IO5
        elif "D6" in dir(board):
            swpin = board.D6
        elif "GP6" in dir(board):
            swpin = board.GP6
        elif "IO6" in dir(board):
            swpin = board.IO6
        elif "D2" in dir(board):
            swpin = board.D2
        elif "GP2" in dir(board):
            swpin = board.GP2
        elif "IO2" in dir(board):
            swpin = board.IO2
        else:
            swpin = None

    if swpin:
        switch = digitalio.DigitalInOut(swpin)
        switch.direction = digitalio.Direction.INPUT
        switch.pull = digitalio.Pull.UP

# If the switch pin is connected to ground (switch.value == False) allow host to write to the drive
        if switch.value == False:
            # Mounts so Host computer can write to micro-flash
            storage.remount("/", True)
            print("Switch False (pin grounded), PyDOS FS is ReadOnly")
        else:
            storage.remount("/", False)
            print("Switch True (not grounded), PyDOS FS is ReadWrite")

        switch.deinit()
    else:
        print("If write access from the host is needed, enter the following PyDOS command:\nfs ro")
        storage.remount("/", False )
elif implementation.name.upper() == "MICROPYTHON":
    spcBoards = ['Teensy 4.1 with MIMXRT1062DVJ6A', \
        'Sparkfun SAMD51 Thing Plus with SAMD51J20A', 
        'XIAO nRF52840 Sense with NRF52840']

    if '_machine' in dir(implementation) and \
       implementation._machine in spcBoards:

        boardNo = spcBoards.index(implementation._machine)
    else:
        boardNo = -1

    if boardNo == 0:
        import uos, sys
        uos.umount("/flash")
        uos.mount(vfs,"/")
        uos.chdir("/")
        sys.path.pop(-1)
        sys.path.pop(-1)
        sys.path.append("/")
        sys.path.append("/lib")
    elif boardNo == 1 or boardNo == 2:
        import sys
        sys.path.append("/lib")
        sys.path.append("/mpython/extFlash/lib")
        sys.path.append("/flash/mpython/extFlash/lib")
        if boardNo == 1:
            import ThngPls_SAMD51
        else:
            import XIAO_nRF52840
        sys.path.pop(-1)
        sys.path.pop(-1)
