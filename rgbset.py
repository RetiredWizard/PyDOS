import sys
from pydos_hw import neoPixel
try:
    from pydos_ui import input
except:
    pass

if __name__ != "PyDOS":
    passedIn = ""
    envVars = {}

nano_connect = False
pixels = None

if sys.implementation.name.upper() == 'CIRCUITPYTHON':
    import board
    if board.board_id == 'arduino_nano_rp2040_connect':
        import busio
        from digitalio import DigitalInOut
        from adafruit_esp32spi import adafruit_esp32spi

        #  uses the secondary SPI connected through the ESP32
        spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)

        #  ESP32 pins
        esp32_cs = DigitalInOut(board.CS1)
        esp32_ready = DigitalInOut(board.ESP_BUSY)
        esp32_reset = DigitalInOut(board.ESP_RESET)

        nano_connect = True

elif sys.implementation.name.upper() == 'MICROPYTHON':
    import machine
    from os import uname
    if uname().machine == 'Arduino Nano RP2040 Connect with RP2040':
        import mp_esp32spi as adafruit_esp32spi

        #  uses the secondary SPI connected through the ESP32
        spi = machine.SPI(1)

        #  ESP32 pins
        esp32_cs = machine.Pin(9,machine.Pin.OUT)
        esp32_ready = machine.Pin(10,machine.Pin.IN)
        esp32_reset = machine.Pin(3,machine.Pin.OUT)

        nano_connect = True

    elif uname().machine == 'TinyPICO with ESP32-PICO-D4':
        from os import umount
        try:
            umount(drive) # Nano Connect uses LED pin for SPI SCK
            print("Unmounting SD card to free up SPI bus")
        except:
            pass

        from dotstar import DotStar
        import tinypico
        spi = machine.SoftSPI(sck=machine.Pin(tinypico.DOTSTAR_CLK),
            mosi=machine.Pin(tinypico.DOTSTAR_DATA), miso=machine.Pin(tinypico.SPI_MISO))
        pixels = DotStar(spi, 1)
        tinypico.set_dotstar_power(True)

if nano_connect:
    #  Nano LED Pins
    LEDG = 25
    LEDB = 26
    LEDR = 27
    OUT = 1   # I/O Direction

    esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

    #esp.set_pin_mode(LEDG,OUT)
    #esp.set_pin_mode(LEDR,OUT)
    #esp.set_pin_mode(LEDB,OUT)

    pixels = True

if not pixels:
    if neoPixel:
        import neopixel
        if ".neopixel" in envVars.keys():
            pixels = envVars['.neopixel']
        else:
            pixels = neopixel.NeoPixel(neoPixel, 1)
            # save instance so we can leave neopixel on when we exit
            envVars[".neopixel"] = pixels
    else:
        print("Neopixel not found")

if pixels:
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

    if nano_connect:
        if r+g+b != 0:
            #esp.set_pin_mode(LEDR,OUT)
            #esp.set_pin_mode(LEDG,OUT)
            #esp.set_pin_mode(LEDB,OUT)

            esp.set_analog_write(LEDR,(255-r)/255)
            esp.set_analog_write(LEDG,(255-g)/255)
            esp.set_analog_write(LEDB,(255-b)/255)
        else:
            try:
                esp32_reset.value(0)
            except:
                esp32_reset.value = 0

        try:
            esp32_cs.deinit()
            esp32_ready.deinit()
            esp32_reset.deinit()
            spi.deinit()
        except:
            pass

    elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
        if r+g+b == 0:
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

        envVars.pop('.neopixel',None)
