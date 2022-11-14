import time
from sys import implementation
from pydos_ui import Pydos_ui
from pydos_hw import Pydos_hw

def rgbrainbow():
    global envVars

    if "envVars" in locals().keys():
        envVars = locals()['envVars']
    elif "envVars" not in globals().keys():
            envVars = {}

    pixels = None
    nano_connect = False
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
        # attempt to balance colors
        MAXRED = 120
        MAXGREEN = 165
        MAXBLUE = 255

        # Cycle colours.
        icolor = 0
        transition = [-4,1,2,-1,4,1,-2,-1]
        cmnd = ""
        steps = 100
        r = 0
        g = 0
        b = 0

        cmnd = ""
        newSteps = 0
        print("listening... Enter value to alter speed, 'q' to quit")

        while cmnd.upper() != "Q":

            if Pydos_ui.serial_bytes_available():
                cmnd = Pydos_ui.read_keyboard(1)

                if cmnd.upper() == "Q":
                    break
                if cmnd == '\n':
                    if newSteps == 0:
                        print()
                    else:
                        steps = max(1,min(800,newSteps))
                        print(" New STEP value: ",steps)
                        newSteps = 0
                if cmnd.isdigit():
                    newSteps = (newSteps * 10) + int(cmnd)
                    print(cmnd,end="")
                elif cmnd != None:
                    print(cmnd,end="")

            icolor = (icolor + 1) % 8

            for k in range(steps):
                r += ((abs(transition[icolor]) & 1)/transition[icolor]) * (MAXRED / steps)
                b += ((abs(transition[icolor]) & 2)/transition[icolor]) * (MAXBLUE / steps)
                g += ((abs(transition[icolor]) & 4)/transition[icolor]) * (MAXGREEN / steps)
                r = int(max(0,min(MAXRED,r)))
                b = int(max(0,min(MAXBLUE,b)))
                g = int(max(0,min(MAXGREEN,g)))

                if nano_connect:
                    esp.set_analog_write(LEDR,(255-r)/255)
                    esp.set_analog_write(LEDG,(255-g)/255)
                    esp.set_analog_write(LEDB,(255-b)/255)
                elif implementation.name.upper() == 'CIRCUITPYTHON':
                    pixels.fill((r,g,b))
                elif implementation.name.upper() == 'MICROPYTHON':
                    if implementation._machine == 'TinyPICO with ESP32-PICO-D4':
                        pixels.fill((r,g,b))
                    else:
                        pixels[0] = (r,g,b)
                        try:
                            pixels.write()
                        except:
                            pixels.show()

                time.sleep(0.5/steps)

            #time.sleep(0.5)

        if nano_connect:
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
    rgbrainbow()
else:
    print("Enter 'rgbrainbow.rgbrainbow()' in the REPL to run.")
