import time
import sys
if sys.implementation.name.upper() == 'MICROPYTHON':
    import machine
elif sys.implementation.name.upper() == 'CIRCUITPYTHON':
    from pwmio import PWMOut
    from board import board_id
    foundPin = True
    if board_id == "arduino_nano_rp2040_connect":
        #A5 is GPIO D19 on Nano Connect
        from board import A5 as sndPin
    elif board_id == "raspberry_pi_pico":
        #D12 is GP11 on the Raspberry PICO
        from board import GP11 as sndPin
    elif board_id == "cytron_maker_pi_rp2040":
        from board import GP22 as sndPin
    else:
        try:
            #Use D12 on Feathers
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
    if 'duty_u16' in dir(pwm):
        pwm.duty_u16(vol)
    else:
        pwm.duty(int((vol/65535)*1023))
    time.sleep(dur/1000)
    if 'duty_u16' in dir(pwm):
        pwm.duty_u16(0)
    else:
        pwm.duty(0)
elif sys.implementation.name.upper() == "CIRCUITPYTHON":
    if not foundPin:
        print("Sound Pin not found")
    else:
        audioPin = PWMOut(sndPin, duty_cycle=0, frequency=440, variable_frequency=True)
        audioPin.frequency = freq
        audioPin.duty_cycle = vol
        time.sleep(dur/1000)
        audioPin.duty_cycle = 0
        audioPin.deinit()
