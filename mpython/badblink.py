"""Example for Pico (pin 25), Nano Connect (Pin 6). Blinks the built-in LED."""
import time
from machine import Pin
from os import uname
from pydos_hw import Pydos_hw

import _thread
global threadLock
global envVars

if __name__ != "PyDOS":
    envVars = {}

threadLock = _thread.allocate_lock()
envVars['stopthread'] = 'go'

if uname().machine == 'Adafruit Feather RP2040 with RP2040':
    led = Pin(13, Pin.OUT)
elif uname().machine == 'Adafruit ItsyBitsy RP2040 with RP2040':
    led = Pin(11, Pin.OUT)
elif uname().machine == 'Arduino Nano RP2040 Connect with RP2040':
    led = Pin(6, Pin.OUT)
elif Pydos_hw.led:
    led = Pin(Pydos_hw.led, Pin.OUT)
else:
    led = Pin(25, Pin.OUT)

print("blinking started....")

#while not threadLock.locked():
while (not threadLock.locked()) and envVars.get('stopthread') == 'go':
#while True:
    led.value(not led.value())
    time.sleep(0.5)

print()
for i in range(6):
    print(5-i)
    time.sleep(0.5)
print("badblink exiting....")
