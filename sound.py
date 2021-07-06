import machine
import time
if passedIn=="":
    print("Syntax: sound Frequency,Duration(miliseconds),Volume")
    argv = "1000,0,0"
else:
    argv = passedIn
args = argv.split(",")
freq=int(args[0])
dur = int(args[1])
vol = int(args[2])
pwm=machine.PWM(machine.Pin(20))
pwm.freq(freq)
pwm.duty_u16(vol)
time.sleep(dur/1000)
pwm.duty_u16(0)
