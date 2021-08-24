"""Example for Pico (pin 25), Nano Connect (Pin 6). Blinks the built-in LED."""
import time
from machine import Pin

import _thread
global threadLock
global envVars

if __name__ != "PyDOS":
    envVars = {}

threadLock = _thread.allocate_lock()
envVars['stopthread'] = 'go'

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