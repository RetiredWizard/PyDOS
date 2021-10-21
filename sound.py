import time
import sys
if sys.implementation.name.upper() == 'MICROPYTHON':
    import machine
elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    from pwmio import PWMOut
    foundPin = True
    try:
        #A5 is GPIO D19 on Nano Connect
        from board import A5 as sndPin
    except:
        foundPin = False
    if not foundPin:
        foundPin = True
        try:
            #Use D12 on Feather
            from board import D12 as sndPin
        except:
            foundPin = False

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
    pwm=machine.PWM(machine.Pin(19))
    pwm.freq(freq)
    pwm.duty_u16(vol)
    time.sleep(dur/1000)
    pwm.duty_u16(0)
elif sys.implementation.name.upper() == "CIRCUITPYTHON":
    audioPin = PWMOut(sndPin, duty_cycle=0, frequency=440, variable_frequency=True)
    audioPin.frequency = freq
    audioPin.duty_cycle = vol
    time.sleep(dur/1000)
    audioPin.duty_cycle = 0
    audioPin.deinit()
