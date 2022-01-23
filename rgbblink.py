"""
Blink example for QT Py using onboard NeoPixel.
Requires two libraries from the Adafruit CircuitPython Library Bundle.
from circuitpython.org/libraries and copy to your CIRCUITPY/lib folder:
* neopixel.mpy
* adafruit_pypixelbuf.mpy
Save this file as code.py to your CIRCUITPY drive to run it.
"""
import time
import sys
from pydos_ui import Pydos_ui

if sys.implementation.name.upper() == 'CIRCUITPYTHON':
    import neopixel
    import board

    if 'NEOPIXEL' not in dir(board):
        try:
            import cyt_mpp_board as board
            foundBoard = True
        except:
            foundBoard = False

        if not foundBoard:
            if board.board_id == "raspberry_pi_pico":
                try:
                    import kfw_pico_board as board
                except:
                    pass
            else:
                try:
                    import kfw_s2_board as board
                except:
                    pass

    pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)

elif sys.implementation.name.upper() == 'MICROPYTHON':
    import machine
    from os import uname
    if uname().machine == 'TinyPICO with ESP32-PICO-D4':
        from micropython_dotstar import DotStar
        spi = machine.SPI(sck=machine.Pin(12), mosi=machine.Pin(13), miso=machine.Pin(18))
        pixels = DotStar(spi, 1)
    elif uname().machine == 'SparkFun Thing Plus RP2040 with RP2040':
        import neopixel
        pixels = neopixel.NeoPixel(machine.Pin(8), 1)
    elif uname().machine == 'Raspberry Pi Pico with RP2040':
        import neopixel
        pixels = neopixel.NeoPixel(machine.Pin(28), 1)
   
icolor = 0
cmnd = ""

print("listening..., enter Q to exit")

while cmnd.upper() != "Q":

    if Pydos_ui.serial_bytes_available():
        cmnd = Pydos_ui.read_keyboard(1)

    icolor = icolor + 1
    icolor = icolor % 3

    if sys.implementation.name.upper() == 'CIRCUITPYTHON':
        pixels.fill(((icolor == 1) * 20, (icolor == 2) * 50, (icolor == 0)*150))
        time.sleep(0.5)
        pixels.fill((0, 0, 0))
        time.sleep(0.5)
    elif sys.implementation.name.upper() == 'MICROPYTHON':
        if uname().machine == 'TinyPICO with ESP32-PICO-D4':
            pixels.fill(((icolor == 1) * 20, (icolor == 2) * 50, (icolor == 0)*150))
            time.sleep(0.5)
            pixels.fill((0, 0, 0))
            time.sleep(0.5)
        else:
            pixels[0] = ((icolor == 1) * 20, (icolor == 2) * 50, (icolor == 0)*150)
            pixels.write()
            time.sleep(0.5)
            pixels[0] = (0, 0, 0)
            pixels.write()
            time.sleep(0.5)

try:
    pixels.deinit()
except:
    pass
