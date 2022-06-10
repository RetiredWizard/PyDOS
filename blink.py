import time
import sys
if sys.implementation.name.upper() == 'MICROPYTHON':
    from machine import Pin
    from os import uname

    if uname().machine == 'Adafruit Feather RP2040 with RP2040':
        led = Pin(13, Pin.OUT)
    elif uname().machine == 'Arduino Nano RP2040 Connect with RP2040':
        from os import umount
        try:
            umount(drive) # Nano Connect uses LED pin for SPI SCK
            print("Unmounting SD card because of shared SCK pin")
        except:
            pass
        led = Pin(6, Pin.OUT)
    else:
        led = Pin(25, Pin.OUT)

elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    import board
    from digitalio import DigitalInOut, Direction

    # LED setup for onboard LED
    if 'LED1' in dir(board):
        led = DigitalInOut(board.LED1)
    else:
        led = DigitalInOut(board.LED)
    led.direction = Direction.OUTPUT

from pydos_ui import Pydos_ui

def blink():

    print("listening..., Enter q to quit")
    cmnd = ""
    blinkstate = True
    while cmnd.upper() != "Q":

        while Pydos_ui.serial_bytes_available():
            cmnd = Pydos_ui.read_keyboard(1)
            print(cmnd, end="", sep="")
            if cmnd in "qQ":
                break

        if sys.implementation.name.upper() == "MICROPYTHON":
            led.value(blinkstate)
        elif sys.implementation.name.upper() == "CIRCUITPYTHON":
            led.value = blinkstate

        blinkstate = not blinkstate
        time.sleep(1)

    if sys.implementation.name.upper() == "CIRCUITPYTHON":
        led.deinit()
    else:
        led.value(False)


blink()
