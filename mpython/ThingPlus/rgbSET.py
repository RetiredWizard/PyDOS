# Example using PIO to drive a WS2812 LED
# // Copy and paste directly into REPL from TeraTerm
# // Make sure baudrate is set to 115200 bps

#import array
from machine import Pin
import rp2


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
#ar = array.array("I", [0])

if __name__ != "PyDOS":
    passedIn = ""

if passedIn == "":
    ans = input("R,G,B: ")
else:
    ans = passedIn

if len(ans.split(",")) == 3:
    r = max(0,min(255,int((ans.split(',')[0] if ans.split(",")[0].isdigit() else 0))))
    g = max(0,min(255,int((ans.split(',')[1] if ans.split(",")[1].isdigit() else 0))))
    b = max(0,min(255,int((ans.split(',')[2] if ans.split(",")[2].isdigit() else 0))))
else:
    r = 0
    g = 0
    b = 0

#ar[0] = g << 16 | r << 8 | b
ar0 = g << 16 | r << 8 | b

#sm.put(ar, 8)
sm.put(ar0, 8)
rp2.PIO(0).remove_program(ws2812)