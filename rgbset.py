import sys
from pydos_ui import Pydos_ui
try:
    from pydos_ui import input
except:
    pass

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
   

if __name__ != "PyDOS":
    passedIn = ""

if passedIn == "":
    ans = input("R,G,B: ")
else:
    ans = passedIn

if len(ans.split(",")) == 3:
    r = max(0,min(255,int((ans.split(',')[0] if ans.split(",")[0].isdigit() else 0))))
    g = max(0,min(255,int((ans.split(',')[1] if ans.split(",")[1].isdigit() else 0))))
    b = max(0,min(255,int((ans.split(',')[2] if ans.split(",")[2].isdigit() else 0))))
else:
    r = 0
    g = 0
    b = 0



if sys.implementation.name.upper() == 'CIRCUITPYTHON':
    pixels.fill((r, g, b))
    time.sleep(0.005)
elif sys.implementation.name.upper() == 'MICROPYTHON':
    if uname().machine == 'TinyPICO with ESP32-PICO-D4':
        pixels.fill((r, g, b))
    else:
        pixels[0] = (r, g, b)
        pixels.write()

try:
    pixels.deinit()
except:
    pass
