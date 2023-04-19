# Scanner i2c en MicroPython | MicroPython i2c scanner
# Renvoi l'adresse en decimal et hexa de chaque device connecte sur le bus i2c
# Return decimal and hexa adress of each i2c device
# https://projetsdiy.fr - https://diyprojects.io (dec. 2017)

# If you run this and it seems to hang, try manually unlocking
# your I2C bus from the REPL with
#  >>> import board
#  >>> board.I2C().unlock()
from pydos_hw import Pydos_hw
from sys import implementation

if __name__ != "PyDOS":
    passedIn = ""

if passedIn == "":
    i2cNo = 0
else:
    i2cNo = int(passedIn)

try:
    i2c = Pydos_hw.I2C(i2cNo)
except:
    print("Trying next i2c bus")
    i2cNo += 1
    i2c = Pydos_hw.I2C(i2cNo)

if i2c:

    print('Scan i2c bus '+str(i2cNo)+'...\n')

    if implementation.name.upper() == 'CIRCUITPYTHON':
        while not i2c.try_lock():
            pass

    devices = i2c.scan()

    if len(devices) == 0:
        print("No i2c device !")
    else:
        print('i2c devices found:',len(devices))

    for device in devices:
        print("Decimal address: ",device," | Hex address: ",hex(device))

    if implementation.name.upper() == 'CIRCUITPYTHON':
        i2c.unlock()
        #i2c.deinit()
else:
    print('i2c bus '+str(i2cNo)+' not found')