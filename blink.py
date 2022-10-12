import time
import sys
from pydos_hw import Pydos_hw
from pydos_ui import Pydos_ui

if sys.implementation.name.upper() == 'MICROPYTHON':
    from machine import Pin
    from os import uname
elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    import board
    from digitalio import DigitalInOut, Direction

def blink(passed_envVars={}):
    global envVars

    if "envVars" not in globals().keys():
        envVars = passed_envVars
    elif envVars == {}:
        envVars = passed_envVars

    if sys.implementation.name.upper() == 'MICROPYTHON':

        # nano connect is special case becuase LED uses the SPI SCK pin
        if uname().machine in ['Arduino Nano RP2040 Connect with RP2040','Teensy 4.1 with MIMXRT1062DVJ6A']:

            if envVars.get('.sd_drive',None) != None:
                from os import umount
                drive = envVars['.sd_drive']
                try:
                    umount(drive) # Nano Connect uses LED pin for SPI SCK
                    print("Unmounting SD card because of shared SCK pin")
                    envVars.pop('.sd_drive',None)
                except:
                    pass

            if uname().machine == 'Teensy 4.1 with MIMXRT1062DVJ6A':
                Pydos_hw.SPI_deinit()
            else:
                Pydos_hw.SD_deinit()

        if Pydos_hw.led:
            led = Pin(Pydos_hw.led, Pin.OUT)
        else:
            raise ValueError("LED pin not defined in pydos_bcfg.py!")

    elif sys.implementation.name.upper() == 'CIRCUITPYTHON':

        # nano connect/Tennsy 4.1 are special cases becuase LED uses the SPI SCK pin
        if board.board_id in ["arduino_nano_rp2040_connect","teensy41"]:

            if envVars.get('.sd_drive',None) != None:
                from storage import umount
                from pydos_hw import PyDOS_HW
                drive = envVars['.sd_drive']
                try:
                    umount(drive) # Nano Connect uses LED pin for SPI SCK
                    print("Unmounting SD card because of shared SCK pin")
                    envVars.pop('.sd_drive',None)
                except:
                    pass
            # If anything has used the SPI interface need to free up SCK
            if board.board_id == "teensy41":
                Pydos_hw.SPI_deinit()
            else:
                Pydos_hw.SD_deinit()

        # LED setup for onboard LED
        if Pydos_hw.led:
            led = DigitalInOut(Pydos_hw.led)
        elif 'LED1' in dir(board):
            led = DigitalInOut(board.LED1)
        else:
            led = DigitalInOut(board.LED)
        led.direction = Direction.OUTPUT

    print("listening..., Enter q to quit")
    cmnd = ""
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
