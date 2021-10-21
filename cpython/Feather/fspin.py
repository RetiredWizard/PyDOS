"""CircuitPython Essentials Storage logging boot.py file"""
import board
import digitalio
#import storage

# For Gemma M0, Trinket M0, Metro M0/M4 Express, ItsyBitsy M0/M4 Express
# switch = digitalio.DigitalInOut(board.D2)

# For Feather M0/M4 Express
switch = digitalio.DigitalInOut(board.D5)

# For Circuit Playground Express, Circuit Playground Bluefruit
# switch = digitalio.DigitalInOut(board.D7)

switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# If the switch pin is connected to ground CircuitPython can write to the drive
#storage.remount("/", switch.value)
print("File System Pin Status: ",switch.value)
if switch.value:
    print("\nPin not grounded")
    print("boot.py should make PyDOS file system writable on next power cycle")
    print("The host computer will have readonly access to the mounted FLASH drive")
else:
    print("\nPin grounded")
    print("boot.py should make PyDOS file system readonly on next power cycle")
    print("The host computer will have read/write access to the mounted FLASH drive")
switch.deinit()
