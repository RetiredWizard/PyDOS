import time
import sys
from pydos_hw import Pydos_hw
from pydos_ui import Pydos_ui

if sys.implementation.name.upper() == 'MICROPYTHON':
    from machine import Pin
    from pydos_bcfg import Pydos_pins
elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    import board
    from digitalio import DigitalInOut, Direction

def blink(passed_envVars={}):
    global envVars
    cmnd = ""


    if "envVars" not in globals().keys():
        envVars = passed_envVars
    elif envVars == {}:
        envVars = passed_envVars

    if sys.implementation.name.upper() == 'MICROPYTHON':

        # nano connect is special case becuase LED uses the SPI SCK pin
        if sys.implementation._machine in ['Arduino Nano RP2040 Connect with RP2040','Teensy 4.1 with MIMXRT1062DVJ6A']:
            ledPin = [6,13][(['Arduino Nano RP2040 Connect with RP2040','Teensy 4.1 with MIMXRT1062DVJ6A'].index(sys.implementation._machine))]

            for i in range(len(Pydos_hw.SDdrive)):
                if Pydos_hw.SCK[i] == Pydos_pins["led"][0]:
                    if Pydos_hw.SDdrive[i] != None:
                        from os import umount
                        print("Unmounting SD card ("+Pydos_hw.SDdrive[i]+") because of shared SCK pin")
                        umount(Pydos_hw.SDdrive[i]) # Nano Connect uses LED pin for SPI SCK
                        Pydos_hw.SDdrive[i] = None
                    # If anything has used the SPI interface need to free up SCK
                    Pydos_hw.SPI_deinit(i)
                    break

        if Pydos_hw.led:
            led = Pin(Pydos_hw.led, Pin.OUT)
        else:
            raise ValueError("LED pin not defined in pydos_bcfg.py!")

    elif sys.implementation.name.upper() == 'CIRCUITPYTHON':

        # nano connect/Tennsy 4.1 are special cases becuase LED uses the SPI SCK pin
        if board.board_id in ["arduino_nano_rp2040_connect","teensy41"]:

            for i in range(len(Pydos_hw.SDdrive)):
                if Pydos_hw.SCK[i] == Pydos_hw.led:
                    if Pydos_hw.SDdrive[i] != None:
                        from storage import umount
                        print("Unmounting SD card ("+Pydos_hw.SDdrive[i]+") because of shared SCK pin")
                        umount(Pydos_hw.SDdrive[i]) # Nano Connect uses LED pin for SPI SCK
                        if "deinit" in dir(Pydos_hw.SD[i]):
                            Pydos_hw.SD[i].deinit()
                        Pydos_hw.SD[i] = None
                        Pydos_hw.SDdrive[i] = None
                    # If anything has used the SPI interface need to free up SCK
                    Pydos_hw.SPI_deinit(i)
                    break

        # LED setup for onboard LED
        if Pydos_hw.led:
            led = DigitalInOut(Pydos_hw.led)
            led.direction = Direction.OUTPUT
        else:
            print("LED pin not defined in pydos_bcfg.py!")
            cmnd = "Q"

    if cmnd != "Q":
        print("listening..., Enter q to quit")
    blinkstate = True
    while cmnd.upper() != "Q":

        while Pydos_ui.serial_bytes_available():
            cmnd = Pydos_ui.read_keyboard(1)
            print(cmnd, end="", sep="")
            if cmnd in "qQ":
                break

        if sys.implementation.name.upper() == "MICROPYTHON":
            led.value(blinkstate)
        elif sys.implementation.name.upper() == "CIRCUITPYTHON":
            led.value = blinkstate

        blinkstate = not blinkstate
        time.sleep(1)

    if sys.implementation.name.upper() == "CIRCUITPYTHON":
        led.deinit()
    else:
        led.value(False)


blink()
