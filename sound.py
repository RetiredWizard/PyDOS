import time
import sys
if sys.implementation.name.upper() == 'MICROPYTHON':
    import machine
elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    from board import A5
    from pwmio import PWMOut
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
    audioPin = PWMOut(A5, duty_cycle=0, frequency=440, variable_frequency=True)
    audioPin.frequency = freq
    audioPin.duty_cycle = volume
    time.sleep(duration/18.2)
    audioPin.duty_cycle = 0
    audioPin.deinit()