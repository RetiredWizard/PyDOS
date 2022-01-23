# Rainbow algorithm adapted from
# https://learnembeddedsystems.co.uk/using-the-rgb-led-on-the-arduino-nano-rp2040-connect

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

    #if supervisor.runtime.serial_bytes_available:
    if Pydos_ui.serial_bytes_available():
        cmnd = input().strip()
        if cmnd == "":
            sba = False
        else:
            sba = True

    return sba, cmnd

pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)

rgbValues = [255,0,0]
upIndex = 0
downIndex = 1

# Cycle colours.
print("listening... 'q' to quit")

while True:

    kbdInt, cmnd = kbdInterrupt()
    if kbdInt:
        if cmnd == "q":
            break

    rgbValues[upIndex] += 1
    rgbValues[downIndex] -= 1

    if rgbValues[upIndex] > 255:
        rgbValues[upIndex] = 255
        upIndex = (upIndex + 1) % 3

    if rgbValues[downIndex] < 0:
        rgbValues[downIndex] = 0
        downIndex = (downIndex + 1) % 3

    pixels.fill((rgbValues[1], rgbValues[2], rgbValues[0]))

    time.sleep(0.005)

pixels.deinit()
