import sys
from pydos_ui import Pydos_ui
try:
    from pydos_ui import input
except:
    pass

if sys.implementation.name.upper() == 'CIRCUITPYTHON':
    import board

    if board.board_id == 'arduino_nano_rp2040_connect':
        import busio
        from digitalio import DigitalInOut
        import adafruit_requests as requests
        import adafruit_esp32spi.adafruit_esp32spi_socket as socket
        from adafruit_esp32spi import adafruit_esp32spi

        #  Nano LED Pins
        LEDG = 25
        LEDB = 26
        LEDR = 27

        OUT = 1   # I/O Direction

        #  ESP32 pins
        esp32_cs = DigitalInOut(board.CS1)
        esp32_ready = DigitalInOut(board.ESP_BUSY)
        esp32_reset = DigitalInOut(board.ESP_RESET)

        #  uses the secondary SPI connected through the ESP32
        spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)

        esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

        requests.set_socket(socket, esp)

    else:
        import neopixel

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

        if ".neopixel" in envVars.keys():
            pixels = envVars['.neopixel']
        else:
            pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
            envVars[".neopixel"] = pixels

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
    if board.board_id == 'arduino_nano_rp2040_connect':
        if r+g+b != 0:
            esp.set_pin_mode(LEDR,OUT)
            esp.set_pin_mode(LEDG,OUT)
            esp.set_pin_mode(LEDB,OUT)

            esp.set_analog_write(LEDR,(255-r)/255)
            esp.set_analog_write(LEDG,(255-g)/255)
            esp.set_analog_write(LEDB,(255-b)/255)

        esp32_cs.deinit()
        esp32_ready.deinit()
        esp32_reset.deinit()
        spi.deinit()

    elif r+g+b == 0:
        pixels.deinit()
        envVars.pop('.neopixel',None)
    else:
        pixels.fill((r, g, b))
elif sys.implementation.name.upper() == 'MICROPYTHON':
    if uname().machine == 'TinyPICO with ESP32-PICO-D4':
        pixels.fill((r, g, b))
    else:
        pixels[0] = (r, g, b)
        pixels.write()
