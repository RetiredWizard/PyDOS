"""
Blink example for QT Py using onboard NeoPixel.
Requires two libraries from the Adafruit CircuitPython Library Bundle.
from circuitpython.org/libraries and copy to your CIRCUITPY/lib folder:
* neopixel.mpy
* adafruit_pypixelbuf.mpy
Save this file as code.py to your CIRCUITPY drive to run it.
"""
import time
import board
import neopixel
from pydos_ui import Pydos_ui
try:
    from pydos_ui import input
except:
    pass

def kbdInterrupt():

    cmnd = ""
    sba = False

    if Pydos_ui.serial_bytes_available():
        cmnd = input().strip()
        if cmnd == "":
            sba = False
        else:
            sba = True

    return sba, cmnd

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
icolor = 0
cmnd = ""

print("listening..., enter Q to exit")

while cmnd.upper() != "Q":

    kbdInt, cmnd = kbdInterrupt()

    icolor = icolor + 1
    icolor = icolor % 3
    pixels.fill(((icolor == 1) * 20, (icolor == 2) * 50, (icolor == 0)*150))
    time.sleep(0.5)
    pixels.fill((0, 0, 0))
    time.sleep(0.5)

pixels.deinit()
