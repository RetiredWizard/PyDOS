import time
import sys
from pydos_hw import Pydos_hw

if not Pydos_hw.sndPin:
    print("Sound Pin not found")
else:
    if sys.implementation.name.upper() == "MICROPYTHON":
        import machine
        machine.PWM(Pydos_hw.sndPin)
        machine.PWM(Pydos_hw.sndPin)
        piezo=machine.PWM(Pydos_hw.sndPin)
    elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
        from pwmio import PWMOut
        Pydos_hw.sndGPIO.deinit() # Workaround for ESP32-S2 GPIO issue
        piezo = PWMOut(Pydos_hw.sndPin,duty_cycle=0,frequency=440,variable_frequency=True)
        # Hack for Teensy 4.1 PWM bug
        piezo.deinit()
        piezo = PWMOut(Pydos_hw.sndPin,duty_cycle=0,frequency=440,variable_frequency=True)
        piezo.deinit()
        piezo = PWMOut(Pydos_hw.sndPin,duty_cycle=0,frequency=440,variable_frequency=True)

    cmnd = "Y"
    while cmnd.upper() == "Y":
        for f in (200, 300, 400, 500, 600, 700, 800, 900):
            if sys.implementation.name.upper() == "MICROPYTHON":
                piezo.freq(f)
                if 'duty_u16' in dir(piezo):
                    piezo.duty_u16(65535 // 3)
                else:
                    piezo.duty(int(((65535 // 3)/65535)*1023))
                time.sleep(0.25)
                if 'duty_u16' in dir(piezo):
                    piezo.duty_u16(0)
                else:
                    piezo.duty(0)
            elif sys.implementation.name.upper() == "CIRCUITPYTHON":
                piezo.frequency = f
                piezo.duty_cycle = 65535 // 3
                time.sleep(0.25)
                piezo.duty_cycle = 0

            time.sleep(0.05)
        time.sleep(0.5)

        cmnd = input("Again (y/n): ")

    if sys.implementation.name.upper() == "CIRCUITPYTHON":
        piezo.deinit()
        Pydos_hw.quietSnd() # Workaround for ESP32-S2 GPIO issue
