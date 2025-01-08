# This will initalize connected HUB75 RGB Matrix panels as a CircuitPython Display

import board
import displayio
import terminalio
import framebufferio
import rgbmatrix
import supervisor

try:
    type(passedIn)
    args = passedIn.split(',')
    [base_width,base_height,bit_depth,chain_across,tile_down] = [int(p) for p in args]
except:
    passedIn = ""
    args = ""

if len(args) != 5 or args[0] not in ['32','64'] or args[1] not in ['32','64'] or bit_depth < 1 or bit_depth > 8:
    try:
        base_width = int(input('Panel pixel width (64): '))
    except:
        base_width = 64
    try:
        base_height = int(input('Panel pixel height (32): '))
    except:
        base_height = 32
    try:
        bit_depth = int(input('Bit Depth (2): '))
    except:
        bit_depth = 2
    try:
        chain_across = int(input('Number of panels across (1): '))
    except:
        chain_across = 1
    try:
        tile_down = int(input('Number of panels down (1): '))
    except:
        tile_down = 1
    
serpentine = True

width = base_width * chain_across
height = base_height * tile_down

displayio.release_displays()

addrPins = [
        board.MTX_ADDRA,
        board.MTX_ADDRB,
        board.MTX_ADDRC,
        board.MTX_ADDRD
]
if base_height == 64:
    addrPins.append(board.MTX_ADDRE)

matrix = rgbmatrix.RGBMatrix(
    width=width,height=height, bit_depth=bit_depth,
    rgb_pins=[
        board.MTX_R1,
        board.MTX_G1,
        board.MTX_B1,
        board.MTX_R2,
        board.MTX_G2,
        board.MTX_B2
    ],
    addr_pins=addrPins,
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE,
    tile=tile_down, serpentine=serpentine,
)
# Associate the RGB matrix with a Display so that we can use displayio features

try:
    type(envVars)
except:
    envVars = {}
    
envVars["_display"] = framebufferio.FramebufferDisplay(matrix)

# Remove Blinka and CP Status from top line of display
envVars["_display"].root_group[0].hidden = False
envVars["_display"].root_group[1].hidden = True # logo
envVars["_display"].root_group[2].hidden = True # status bar
supervisor.reset_terminal(envVars["_display"].width, height+11)
envVars["_display"].root_group[0].y=-2
envVars["_display"].root_group[0].x=0

envVars["_scrWidth"]=round(envVars["_display"].width/((terminalio.FONT.bitmap.width/95)*displayio.CIRCUITPYTHON_TERMINAL.scale))-2
envVars["_scrHeight"]=round(envVars["_display"].height/(terminalio.FONT.bitmap.height*displayio.CIRCUITPYTHON_TERMINAL.scale))-1

