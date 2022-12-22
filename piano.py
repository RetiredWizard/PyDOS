import sys
from pydos_ui import Pydos_ui
from pydos_hw import Pydos_hw
from pydos_hw import quietSnd

if sys.implementation.name.upper() == 'MICROPYTHON':
    import machine
    from time import ticks_ms,sleep
elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    from time import sleep
    from supervisor import ticks_ms
    from pwmio import PWMOut
    from board import board_id

def piano():

    if sys.implementation.name.upper() == 'MICROPYTHON':
        pwm=machine.PWM(Pydos_hw.sndPin)
    elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
        Pydos_hw.sndGPIO.deinit() # Workaround for ESP32-S2 GPIO issue
        pwm=PWMOut(Pydos_hw.sndPin, duty_cycle=0, frequency=440, variable_frequency=True)
        # Hack for Teensy 4.1 PWM bug
        pwm.deinit()
        pwm = PWMOut(Pydos_hw.sndPin,duty_cycle=0,frequency=440,variable_frequency=True)
        pwm.deinit()
        pwm = PWMOut(Pydos_hw.sndPin,duty_cycle=0,frequency=440,variable_frequency=True)

    print ("\nPress +/- to change volume, 'q' to quit...")

    volume = 400
    cmnd = None
    press = False
    noneAt = ticks_ms()
    firstNone = True
    note = 0
    while cmnd != "q":
        if Pydos_ui.serial_bytes_available() != 0:
            cmnd = Pydos_ui.read_keyboard(1)
            #print("->"+cmnd+"<- : ",ord(cmnd[0]))
            firstNone = True
            if cmnd=="h": # middle C
                note=int(261.6256+.5)
                press = True
            elif cmnd == "a": # E
                note=int(164.8138+.5)
                press = True
            elif cmnd == "s": # F
                note=int(174.6141+.5)
                press = True
            elif cmnd == "d": # G
                note=int(195.9977+.5)
                press = True
            elif cmnd == "r": # G sharp/A flat
                note=int(207.6523+.5)
                press = True
            elif cmnd == "f": # A
                note=int(220)
                press = True
            elif cmnd == "t": # A sharp/B flat
                note=int(233.0819+.5)
                press = True
            elif cmnd == "g": # B
                note=int(246.9417+.5)
                press = True
            elif cmnd == "u": # C sharp/D flat
                note=int(277.1826+.5)
                press = True
            elif cmnd == "j": # D
                note=int(293.6648+.5)
                press = True
            elif cmnd == "k": # E
                note=int(329.6276+.5)
                press = True
            elif cmnd == "l": # F
                note=int(349.2262+.5)
                press = True
            elif cmnd == "o": # F sharp/G flat
                note=int(369.9944+.5)
                press = True
            elif cmnd == ";": # G
                note=int(391.9954+.5)
                press = True
            elif cmnd == "q":
                break

            if cmnd == "+":
                volume += 100
            elif cmnd == "-":
                volume -= 100
        else:
            if firstNone:
                noneAt = ticks_ms()
                firstNone = False
            else:
                if ticks_ms() > noneAt+500:
                    firstNone = True
                    press = False

        if press:
            if sys.implementation.name.upper() == 'MICROPYTHON':
                pwm.freq(note)
                if 'duty_u16' in dir(pwm):
                    pwm.duty_u16(volume)
                else:
                    pwm.duty(int((volume/65535)*1023))
                if "ESP32" in sys.implementation._machine or "S2" in sys.implementation._machine:
                    sleep(.1)
            elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
                if pwm.frequency != note:
                    pwm.frequency = note
                if pwm.duty_cycle != volume:
                    pwm.duty_cycle = volume
                if "s2" in board_id or "s3" in board_id:
                    sleep(.1)

            #time.sleep(.1)
            #cmnd = kbdInterrupt()
            #while cmnd != None:
                #cmnd = kbdInterrupt()
            #pressedat = time.time()
        else:
            if sys.implementation.name.upper() == 'MICROPYTHON':
                if 'duty_u16' in dir(pwm):
                    pwm.duty_u16(0)
                else:
                    pwm.duty(0)
            elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
                if pwm.duty_cycle != 0:
                    pwm.duty_cycle = 0
            #print("Release")

    if sys.implementation.name.upper() == 'CIRCUITPYTHON':
        pwm.deinit()
        quietSnd() # Workaround for ESP32-S2 GPIO issue

if Pydos_hw.sndPin:
    piano()
else:
    print("Sound Pin not found")
