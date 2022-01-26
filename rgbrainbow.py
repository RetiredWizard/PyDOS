# Rainbow algorithm adapted from
# https://learnembeddedsystems.co.uk/using-the-rgb-led-on-the-arduino-nano-rp2040-connect

import time
import sys
from pydos_ui import Pydos_ui

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

        esp.set_pin_mode(LEDR,OUT)
        esp.set_pin_mode(LEDG,OUT)
        esp.set_pin_mode(LEDB,OUT)

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
            envVars.pop('.neopixel',None)
        else:
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


rgbValues = [255,0,0]
upIndex = 0
downIndex = 1
cmnd = ""

# Cycle colours.
print("listening... 'q' to quit")

while cmnd.upper() != "Q":

    if Pydos_ui.serial_bytes_available():
        cmnd = Pydos_ui.read_keyboard(1)

    rgbValues[upIndex] += 1
    rgbValues[downIndex] -= 1

    if rgbValues[upIndex] > 255:
        rgbValues[upIndex] = 255
        upIndex = (upIndex + 1) % 3

    if rgbValues[downIndex] < 0:
        rgbValues[downIndex] = 0
        downIndex = (downIndex + 1) % 3

    if cmnd.upper() == "Q":
        rgbValues[0] = 0
        rgbValues[1] = 0
        rgbValues[2] = 0

    if sys.implementation.name.upper() == 'CIRCUITPYTHON':
        if board.board_id == 'arduino_nano_rp2040_connect':
            esp.set_analog_write(LEDR,rgbValues[0]/255)
            esp.set_analog_write(LEDG,rgbValues[1]/255)
            esp.set_analog_write(LEDB,rgbValues[2]/255)

        else:
            pixels.fill((rgbValues[1], rgbValues[2], rgbValues[0]))

        time.sleep(0.005)

    elif sys.implementation.name.upper() == 'MICROPYTHON':
        if uname().machine == 'TinyPICO with ESP32-PICO-D4':
            pixels.fill((rgbValues[1], rgbValues[2], rgbValues[0]))
            time.sleep(0.005)
        else:
            pixels[0] = (rgbValues[1], rgbValues[2], rgbValues[0])
            pixels.write()
            time.sleep(0.005)

if board.board_id == 'arduino_nano_rp2040_connect':
    # Hack to completly turn off RGB LED
    spi.deinit()
    spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
    esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

    esp32_cs.deinit()
    esp32_ready.deinit()
    esp32_reset.deinit()
    spi.deinit()

try:
    pixels.deinit()
except:
    pass
