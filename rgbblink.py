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
from pydos_hw import Pydos_hw
from os import uname

def rgbblink():
    global envVars

    if "envVars" in locals().keys():
        envVars = locals()['envVars']
    elif "envVars" not in globals().keys():
            envVars = {}

    pixels = None
    nano_connect = False
    if sys.implementation.name.upper() == 'CIRCUITPYTHON':
        import board

        if board.board_id == 'arduino_nano_rp2040_connect':
            import busio
            from digitalio import DigitalInOut
            from adafruit_esp32spi import adafruit_esp32spi

            nano_connect = True

            #  Nano LED Pins
            LEDG = 25
            LEDB = 26
            LEDR = 27

            #  ESP32 pins
            esp32_cs = DigitalInOut(board.CS1)
            esp32_ready = DigitalInOut(board.ESP_BUSY)
            esp32_reset = DigitalInOut(board.ESP_RESET)

            #  uses the secondary SPI connected through the ESP32
            spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)

            esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

            pixels = True

    elif sys.implementation.name.upper() == 'MICROPYTHON':
        import machine

        if Pydos_hw.neoPixel_Pow:
            Pydos_hw.neoPixel_Pow.on()

        if uname().machine == 'TinyPICO with ESP32-PICO-D4':
            from os import umount
            drive = envVars.get('.sd_drive',drive)
            try:
                umount(drive) # Nano Connect uses LED pin for SPI SCK
                print("Unmounting SD card to free up SPI bus")
                envVars.pop('.sd_drive',None)
            except:
                pass

            from dotstar import DotStar
            import tinypico

            spi = machine.SoftSPI(sck=machine.Pin(tinypico.DOTSTAR_CLK),
                mosi=machine.Pin(tinypico.DOTSTAR_DATA), miso=machine.Pin(tinypico.SPI_MISO))
            pixels = DotStar(spi, 1)
            tinypico.set_dotstar_power(True)
        elif uname().machine == 'Arduino Nano RP2040 Connect with RP2040':
            import mp_esp32spi

            nano_connect = True

            #  Nano LED Pins
            LEDG = 25
            LEDB = 26
            LEDR = 27

            OUT = 1   # I/O Direction

            #  uses the secondary SPI connected through the ESP32
            spi = machine.SPI(1)

            #  ESP32 pins
            esp32_cs = machine.Pin(9,machine.Pin.OUT)
            esp32_ready = machine.Pin(10,machine.Pin.IN)
            esp32_reset = machine.Pin(3,machine.Pin.OUT)

            esp = mp_esp32spi.ESP_SPIcontrol(spi,esp32_cs,esp32_ready,esp32_reset)

            pixels = True

    if not pixels:
        if Pydos_hw.neoPixel or Pydos_hw.dotStar_Clock:
            if ".neopixel" in envVars.keys():
                pixels = envVars['.neopixel']
                envVars.pop('.neopixel',None)
                if 'envVars' not in locals().keys():
                    locals()['envVars'] = envVars
            elif Pydos_hw.neoPixel:
                import neopixel
                pixels = neopixel.NeoPixel(Pydos_hw.neoPixel, 1)
            elif Pydos_hw.dotStar_Clock:
                if sys.implementation.name.upper() == 'CIRCUITPYTHON':
                    import adafruit_dotstar
                    pixels = adafruit_dotstar.DotStar(Pydos_hw.dotStar_Clock, \
                        Pydos_hw.dotStar_Data, 1, auto_write=True)
                elif sys.implementation.name.upper() == 'MICROPYTHON':
                    from dotstar import DotStar
                    spi = machine.SoftSPI(sck=machine.Pin(Pydos_hw.dotStar_Clock), \
                        mosi=machine.Pin(Pydos_hw.dotStar_Data), miso=machine.Pin(Pydos_hw.MISO))
                    pixels = DotStar(spi, 1)
        else:
            print("Neopixel not found")

    if pixels:
        icolor = 0
        cmnd = ""

        print("listening..., enter Q to exit")

        while cmnd.upper() != "Q":

            if Pydos_ui.serial_bytes_available():
                cmnd = Pydos_ui.read_keyboard(1)

            icolor = icolor + 1
            icolor = icolor % 3

            if sys.implementation.name.upper() == 'CIRCUITPYTHON':
                if board.board_id == 'arduino_nano_rp2040_connect':
                    esp.set_analog_write(LEDR,(0 if icolor == 1 else 1))
                    esp.set_analog_write(LEDG,(0 if icolor == 2 else 1))
                    esp.set_analog_write(LEDB,(0 if icolor == 0 else 1))
                    time.sleep(0.5)
                    # Hack to completly turn off RGB LED
                    #spi.deinit()
                    #spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
                    #esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

                    # If Hack is used, comment out these 4 lines
                    esp.set_analog_write(LEDR,1)
                    esp.set_analog_write(LEDG,1)
                    esp.set_analog_write(LEDB,1)
                    time.sleep(0.5)

                else:
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
                elif uname().machine == 'Arduino Nano RP2040 Connect with RP2040':
                    esp.set_analog_write(LEDR,(0 if icolor == 1 else 1))
                    esp.set_analog_write(LEDG,(0 if icolor == 2 else 1))
                    esp.set_analog_write(LEDB,(0 if icolor == 0 else 1))
                    time.sleep(0.5)

                    esp.set_analog_write(LEDR,1)
                    esp.set_analog_write(LEDG,1)
                    esp.set_analog_write(LEDB,1)
                    time.sleep(0.5)
                else:
                    pixels[0] = ((icolor == 1) * 20, (icolor == 2) * 50, (icolor == 0)*150)
                    try:
                        pixels.write()
                    except:
                        pixels.show()
                    time.sleep(0.5)
                    pixels[0] = (0, 0, 0)
                    try:
                        pixels.write()
                    except:
                        pixels.show()
                    time.sleep(0.5)

        if nano_connect:
            # Hack to completly turn off RGB LED
            #spi.deinit()
            #spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
            #esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
            try:
                esp32_reset.value = 0

                esp32_cs.deinit()
                esp32_ready.deinit()
                esp32_reset.deinit()
                spi.deinit()
            except:
                esp32_reset.value(0)

        if Pydos_hw.neoPixel_Pow:
            try:
                Pydos_hw.neoPixel_Pow.off()
            except:
                pass

        try:
            pixels.deinit()
        except:
            pass

if __name__ == "PyDOS":
    rgbblink()
else:
    print("Enter 'rgbblink.rgbblink()' in the REPL to run.")
