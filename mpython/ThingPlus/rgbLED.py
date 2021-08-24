# Example using PIO to drive a WS2812 LED
# // Copy and paste directly into REPL from TeraTerm
# // Make sure baudrate is set to 115200 bps

import array, time
from machine import Pin
import rp2, sys, uselect

def kbdInterrupt():

    spoll = uselect.poll()
    spoll.register(sys.stdin,uselect.POLLIN)

    cmnd = sys.stdin.read(1) if spoll.poll(0) else None

    spoll.unregister(sys.stdin)

    return(cmnd)


# Configure the number of WS2812 LEDs.
NUM_LEDS = 1
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

# Create the StateMachine with the ws2812 program, outputting on Pin(08).
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(08))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

# Cycle colours.
icolor = 0
transition = [-4,1,2,-1,4,1,-2,-1]
cmnd = ""
cmndBuf = ""
steps = 25
r = 0
g = 0
b = 0

print("listening... 'q' to quit")

while True:

    cmnd = kbdInterrupt()
    if cmnd == "q":
        break
    elif cmnd == "\n":
        if cmndBuf.isdigit():
            steps = max(1,min(200,int(cmndBuf)))
        cmndBuf = ""
    elif cmnd != None:
        cmndBuf += cmnd
        print(cmnd, end="", sep="")

    icolor += 1
    icolor = icolor % 8


    for k in range(steps):
        for i in range(4 * NUM_LEDS):
            for j in range(NUM_LEDS):
                r += ((abs(transition[icolor]) & 1)/transition[icolor]) * (50 / (steps*NUM_LEDS*4))
                b += ((abs(transition[icolor]) & 2)/transition[icolor]) * (150 / (steps*NUM_LEDS*4))
                g += ((abs(transition[icolor]) & 4)/transition[icolor]) * (40 / (steps*NUM_LEDS*4))
                ar[j] = int(g) << 16 | int(r) << 8 | int(b)
                sm.put(ar, 8)
                time.sleep(0.01)

    time.sleep(0.5)
    r = int(r+.5)
    b = int(b+.5)
    g = int(g+.5)

    #for i in range(4 * NUM_LEDS):
        #for j in range(NUM_LEDS):
            #r = 0
            #b = 0
            #g = 0
            #ar[j] = g << 16 | r << 8 | b
            #sm.put(ar, 8)
    #time.sleep(0.5)

rp2.PIO(0).remove_program(ws2812)
