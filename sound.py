import time
import sys
from pydos_hw import Pydos_hw
from pydos_hw import quietSnd
if sys.implementation.name.upper() == "MICROPYTHON":
    import machine
elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    from supervisor import ticks_ms
    from pwmio import PWMOut

if __name__ != "PyDOS":
    passedIn = ""

if passedIn=="":
    print("Syntax: sound Frequency,Duration(miliseconds),Volume")
    argv = "1000,0,0"
else:
    argv = passedIn
args = argv.split(",")
if len(args) != 3:
    print("Syntax: sound Frequency,Duration(miliseconds),Volume")
    args = [1000,0,0]

freq=int(args[0])
dur = int(args[1])
vol = int(args[2])

if sys.implementation.name.upper() == "MICROPYTHON":
    oldPWM = False
    try:
        # Check if alternate PWM mode (nrf boards) is being used
        pwm=machine.PWM(0,period=(1000-freq)*20,pin=Pydos_hw.sndPin,freq=250,duty=int((vol/65535)*100))
        oldPWM = True
    except:
        pwm=machine.PWM(Pydos_hw.sndPin)
        pwm.freq(freq)

    if oldPWM:
        pwm.init()
    elif 'duty_u16' in dir(pwm):
        pwm.duty_u16(vol)
    else:
        pwm.duty(int((vol/65535)*1023))

    time.sleep(dur/1000)
    if oldPWM:
        pwm.deinit()
    elif 'duty_u16' in dir(pwm):
        pwm.duty_u16(0)
    else:
        pwm.duty(0)
elif sys.implementation.name.upper() == "CIRCUITPYTHON":
    if not Pydos_hw.sndPin:
        print("Sound Pin not found")
    else:
        Pydos_hw.sndGPIO.deinit() # Workaround for ESP32-S2 GPIO issue
        audioPin = PWMOut(Pydos_hw.sndPin, duty_cycle=vol, frequency=freq)
        #audioPin.frequency = freq
        #audioPin.duty_cycle = vol
        time.sleep(dur/1000)
        #audioPin.duty_cycle = 0
        audioPin.deinit()
        quietSnd() # Workaround for ESP32-S2 GPIO issue
