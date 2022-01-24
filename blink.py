import time
import sys
if sys.implementation.name.upper() == 'MICROPYTHON':
    from machine import Pin

    led = Pin(25, Pin.OUT)

elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    import board
    from digitalio import DigitalInOut, Direction

    # LED setup for onboard LED
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


blink()
