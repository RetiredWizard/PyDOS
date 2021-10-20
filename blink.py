import time
import sys
if sys.implementation.name.upper() == 'MICROPYTHON':
    from machine import Pin
    import uselect
elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    import board
    from digitalio import DigitalInOut, Direction
    import supervisor
try:
    from pydos_ui import input
except:
    pass

def blink():
    def kbdInterrupt():

        cmnd = ""
        sba = False

        if sys.implementation.name.upper() == "CIRCUITPYTHON":
            if supervisor.runtime.serial_bytes_available:
                cmnd = input().strip()
        else:
            spoll = uselect.poll()
            spoll.register(sys.stdin,uselect.POLLIN)
            cmnd = sys.stdin.read(1) if spoll.poll(0) else ""
            spoll.unregister(sys.stdin)

        if cmnd == "":
            sba = False
        else:
            sba = True

        return sba,cmnd



    print("listening..., Enter q to quit")

    if sys.implementation.name.upper() == "MICROPYTHON":

        led = Pin(25, Pin.OUT)
        cmnd = ""

        while cmnd.upper() != "Q":
            kbdInt, cmnd = kbdInterrupt()
            print(cmnd, end="", sep="")

            led.value(not led.value())
            time.sleep(1)

    elif sys.implementation.name.upper() == "CIRCUITPYTHON":
        # LED setup for onboard LED
        led = DigitalInOut(board.LED)
        led.direction = Direction.OUTPUT

        cmnd = ""

        while cmnd.upper() != "Q":
            kbdInt, cmnd = kbdInterrupt()

            led.value = True
            time.sleep(1)

            led.value = False
            time.sleep(1)

        led.deinit()

blink()
