# Scanner i2c en MicroPython | MicroPython i2c scanner
# Renvoi l'adresse en decimal et hexa de chaque device connecte sur le bus i2c
# Return decimal and hexa adress of each i2c device
# https://projetsdiy.fr - https://diyprojects.io (dec. 2017)

import sys
if sys.implementation.name.upper() == 'MICROPYTHON':
    import machine
    from os import uname

    if uname().machine == 'TinyPICO with ESP32-PICO-D4':
        i2c = machine.I2C(1,scl=machine.Pin(22),sda=machine.Pin(21))
    elif uname().machine == 'SparkFun Thing Plus RP2040 with RP2040':
        # i2c pins for qwic connect on thingplus SCL=7, SDA=6;
        i2c = machine.I2C(1,scl=machine.Pin(7), sda=machine.Pin(6))
    else:
        # raspberry pi pico physical pins 5,4 Gpio SCL=3, SDA=2
        i2c = machine.I2C(1,scl=machine.Pin(3), sda=machine.Pin(2))
elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    # If you run this and it seems to hang, try manually unlocking
    # your I2C bus from the REPL with
    #  >>> import board
    #  >>> board.I2C().unlock()
    import time
    from pydos_ui import PyDOS_UI

    i2c = PyDOS_UI.I2C()

print('Scan i2c bus...')

if sys.implementation.name.upper() == 'CIRCUITPYTHON':
    while not i2c.try_lock():
        pass

devices = i2c.scan()

if len(devices) == 0:
    print("No i2c device !")
else:
    print('i2c devices found:',len(devices))

for device in devices:
    print("Decimal address: ",device," | Hex address: ",hex(device))

if sys.implementation.name.upper() == 'CIRCUITPYTHON':
    i2c.unlock()
    #i2c.deinit()
