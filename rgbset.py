from sys import implementation
from pydos_hw import Pydos_hw
from pydos_ui import Pydos_ui
try:
    from pydos_ui import input
except:
    pass

def rgbset(ans=""):
    global envVars

    if "envVars" in locals().keys():
        envVars = locals()['envVars']
    elif "envVars" not in globals().keys():
            envVars = {}

    nano_connect = False
    pixels = None

    if implementation.name.upper() == 'CIRCUITPYTHON':
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

    elif implementation.name.upper() == 'MICROPYTHON':
        import machine

        if Pydos_hw.neoPixel_Pow:
            Pydos_hw.neoPixel_Pow.on()

        if implementation._machine == 'Arduino Nano RP2040 Connect with RP2040':
            import mp_esp32spi as adafruit_esp32spi

            #  uses the secondary SPI connected through the ESP32
            spi = machine.SPI(1)

            #  ESP32 pins
            esp32_cs = machine.Pin(9,machine.Pin.OUT)
            esp32_ready = machine.Pin(10,machine.Pin.IN)
            esp32_reset = machine.Pin(3,machine.Pin.OUT)

            nano_connect = True

        elif implementation._machine == 'TinyPICO with ESP32-PICO-D4':
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
        if Pydos_hw.neoPixel or Pydos_hw.dotStar_Clock:
            if ".neopixel" in envVars.keys():
                pixels = envVars['.neopixel']
            elif Pydos_hw.neoPixel:
                import neopixel
                pixels = neopixel.NeoPixel(Pydos_hw.neoPixel, 1)
                if implementation.name.upper() == 'CIRCUITPYTHON':
                    # save instance so we can leave neopixel on when we exit
                    envVars[".neopixel"] = pixels
                    if 'envVars' not in locals().keys():
                        locals()['envVars'] = envVars
            elif Pydos_hw.dotStar_Clock:
                if implementation.name.upper() == 'CIRCUITPYTHON':
                    import adafruit_dotstar
                    pixels = adafruit_dotstar.DotStar(Pydos_hw.dotStar_Clock, \
                        Pydos_hw.dotStar_Data, 1, auto_write=True)
                    envVars[".neopixel"] = pixels
                    if 'envVars' not in locals().keys():
                        locals()['envVars'] = envVars
                elif implementation.name.upper() == 'MICROPYTHON':
                    from dotstar import DotStar
                    spi = machine.SoftSPI(sck=machine.Pin(Pydos_hw.dotStar_Clock), \
                        mosi=machine.Pin(Pydos_hw.dotStar_Data), miso=machine.Pin(Pydos_hw.MISO))
                    pixels = DotStar(spi, 1)
        else:
            print("Neopixel/Dotstar not found")

    if pixels:
        if ans == "":
            ans = input("R,G,B: ")

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

        elif implementation.name.upper() == 'CIRCUITPYTHON':
            if r+g+b == 0:
                pixels.deinit()
                envVars.pop('.neopixel',None)
                if 'envVars' not in locals().keys():
                    locals()['envVars'] = envVars
            else:
                pixels.fill((r, g, b))

        elif implementation.name.upper() == 'MICROPYTHON':
            if implementation._machine == 'TinyPICO with ESP32-PICO-D4':
                pixels.fill((r, g, b))
            else:
                pixels[0] = (r, g, b)
                try:
                    pixels.write()
                except:
                    pixels.show()
                if r+g+b == 0 and Pydos_hw.neoPixel_Pow:
                    Pydos_hw.neoPixel_Pow.off()

            # Shouldn't be set in Micropython but just in case...
            envVars.pop('.neopixel',None)

if __name__ == "PyDOS":
    rgbset(passedIn)
else:
    print("Enter 'rgbset.rgbset()' in the REPL to run.")
