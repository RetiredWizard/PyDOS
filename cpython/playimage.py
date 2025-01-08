import board
try:
    import gifio
except:
    pass
import adafruit_ticks
import adafruit_imageload
import bitmaptools
import displayio
from os import getenv
try:
    from pydos_ui import Pydos_ui
    from pydos_ui import input
    Pydos_display = ('display' in dir(Pydos_ui))
except:
    Pydos_display = False

try:
    type(envVars)
except:
    envVars = {}
    
if '_display' in envVars.keys():
    display = envVars['_display']
elif Pydos_display:
    display = Pydos_ui.display
elif 'DISPLAY' in dir(board):
    display = board.DISPLAY
else:
    try:
        import matrix
        display = matrix.envVars['_display']
    except:
        try:
            import framebufferio
            import dotclockframebuffer
        except:
            try:
                import adafruit_ili9341
            except:
                import framebufferio
                import picodvi

        displayio.release_displays()

        if 'TFT_PINS' in dir(board):
            sWdth = getenv('CIRCUITPY_DISPLAY_WIDTH')
            if sWdth == None:
                if board.board_id == "makerfabs_tft7":
                    sWdth = input("What is the resolution Width of the touch screen? (1024/800/...): ")
                else:
                    sWdth = board.TFT_TIMINGS['width']
                if 'updateTOML' in dir(Pydos_ui):
                    Pydos_ui.updateTOML("CIRCUITPY_DISPLAY_WIDTH",str(sWdth))

            if sWdth == 1024 and "TFT_TIMINGS1024" in dir(board):
                disp_bus=dotclockframebuffer.DotClockFramebuffer(**board.TFT_PINS,**board.TFT_TIMINGS1024)
            else:
                disp_bus=dotclockframebuffer.DotClockFramebuffer(**board.TFT_PINS,**board.TFT_TIMINGS)
            display=framebufferio.FramebufferDisplay(disp_bus)

        else:
            try:
                type(adafruit_ili9341)
                if 'SPI' in dir(board):
                    spi = board.SPI()
                else:
                    spi = busio.SPI(clock=board.SCK,MOSI=board.MOSI,MISO=board.MISO)
                disp_bus=displayio.FourWire(spi,command=board.D10,chip_select=board.D9, \
                    reset=board.D6)
                display=adafruit_ili9341.ILI9341(disp_bus,width=320,height=240)
            except:
                # DVI Sock
                fb = picodvi.Framebuffer(320,240,clk_dp=board.GP14, clk_dn=board.GP15, \
                    red_dp=board.GP12, red_dn=board.GP13,green_dp=board.GP18, \
                    green_dn=board.GP19,blue_dp=board.GP16, blue_dn=board.GP17,color_depth=8)
                display=framebufferio.FramebufferDisplay(fb)

def playimage(passedIn=""):

    if passedIn != "":
        flist = passedIn
    else:
        flist = ""
        
    if flist == "":
        flist = input("Enter filename: ")
    try:
        while Pydos_ui.virt_touched():
            pass
    except:
        pass

    if flist==passedIn:
        print('Press "q" to quit')
    else:
        input('Press "Enter" to continue, press "q" to quit')

    files = flist.split(',')
    try:
        dispseconds = int(files[-1])
        files = files[:-1]
    except:
        dispseconds = 15

    singleimage = False
    if len(files) == 1 and files[0][0] != '*':
        singleimage = True

    fileindx = 0
    wildindx = 0
    while True:
        fname = files[fileindx]

        if fname[0] == '*':
            wildlist = [f for f in os.listdir() if f[fname.find('.')-len(fname):] == fname[fname.find('.')-len(fname):]]
            fname = wildlist[wildindx]
            wildindx = (wildindx +1) % len(wildlist)
            if wildindx == 0:
                fileindx = (fileindx + 1) % len(files)
        else:
            fileindx = (fileindx + 1) % len(files)


        if fname[-4:].upper() in [".BMP",".PNG",".JPG",".RLE"]:

            bitmap, palette = adafruit_imageload.load( \
                fname, bitmap=displayio.Bitmap, palette=displayio.Palette)
            
            scalefactor = display.width / bitmap.width
            if display.height/bitmap.height < scalefactor:
                scalefactor = display.height/bitmap.height

            if scalefactor < 1:
                if singleimage:
                    print(f'scalefactor: {scalefactor}')
                bitframe = displayio.Bitmap(display.width,display.height,2**bitmap.bits_per_value)
                bitmaptools.rotozoom(bitframe,bitmap,scale=scalefactor)
                facecc = displayio.TileGrid(bitframe,pixel_shader=palette)
                    # pixel_shader=displayio.ColorConverter(input_colorspace=colorspace))
                pwidth = bitframe.width
                pheight = bitframe.height
            else:
                facecc = displayio.TileGrid(bitmap,pixel_shader=palette)
                    # pixel_shader=displayio.ColorConverter(input_colorspace=colorspace))
                pwidth = bitmap.width
                pheight = bitmap.height

            if singleimage:                
                print("bitmap (w,h): ",bitmap.width,bitmap.height)
                print("scaled bitmap (w,h): ",pwidth,pheight)
                print("facecc (w,h): ",facecc.width,facecc.height)
            
            if pwidth < display.width:
                facecc.x = (display.width-pwidth)//2
            if pheight < display.height:
                facecc.y = (display.height-pheight)//2
            splash = displayio.Group()
            splash.append(facecc)
            display.root_group = splash

            if singleimage:
                input('Press Enter to close')
                break
            else:
                cmnd = ""
                stop = adafruit_ticks.ticks_add(adafruit_ticks.ticks_ms(),int(dispseconds*1000))
                while adafruit_ticks.ticks_less(adafruit_ticks.ticks_ms(),stop):
                    if Pydos_ui.serial_bytes_available():
                        cmnd = Pydos_ui.read_keyboard(1)
                        print(cmnd, end="", sep="")
                        if cmnd.upper() == "Q":
                            break
                if cmnd.upper() == "Q":
                    break

            try:
                splash.pop()
                bitmap.deinit()
                bitmap = None
                facecc.bitmap.deinit()
                facecc = None
                if scalefactor < 1:
                    bitframe.deinit()
                    bitframe = None
            except:
                pass

        elif fname[-4:].upper() in [".GIF"]:

            odgcc = gifio.OnDiskGif(fname)
            with odgcc as odg:

                if getenv('PYDOS_DISPLAYIO_COLORSPACE',"").upper() == 'BGR565_SWAPPED':
                    colorspace = displayio.Colorspace.BGR565_SWAPPED
                else:
                    colorspace = displayio.Colorspace.RGB565_SWAPPED

                scalefactor = display.width / odg.width
                if display.height/odg.height < scalefactor:
                    scalefactor = display.height/odg.height

                if scalefactor < 1:
                    if singleimage:
                        print(f'scalefactor: {scalefactor}')
                    bitframe = displayio.Bitmap(display.width,display.height,2**odg.bitmap.bits_per_value)
                    bitmaptools.rotozoom(bitframe,odg.bitmap,scale=scalefactor)
                    facecc = displayio.TileGrid(bitframe, \
                        pixel_shader=displayio.ColorConverter(input_colorspace=colorspace))
                    pwidth = bitframe.width
                    pheight = bitframe.height
                else:
                    facecc = displayio.TileGrid(odg.bitmap, \
                        pixel_shader=displayio.ColorConverter(input_colorspace=colorspace))
                    pwidth = odg.bitmap.width
                    pheight = odg.bitmap.height

                if pwidth < display.width:
                    facecc.x = (display.width-pwidth)//2
                if pheight < display.height:
                    facecc.y = (display.height-pheight)//2
                splash = displayio.Group()
                splash.append(facecc)
                display.root_group = splash

                cmnd = ""
                # Display repeatedly.
                stop = adafruit_ticks.ticks_add(adafruit_ticks.ticks_ms(),int(dispseconds*1000))
                while adafruit_ticks.ticks_less(adafruit_ticks.ticks_ms(),stop) or dispseconds==-1:

                    if Pydos_ui.serial_bytes_available():
                        cmnd = Pydos_ui.read_keyboard(1)
                        print(cmnd, end="", sep="")
                        if cmnd.upper() == "Q":
                            break
                    start = adafruit_ticks.ticks_ms()
                    next_delay = odg.next_frame()
                    start = adafruit_ticks.ticks_add(start,int(next_delay*1000))
                    if next_delay > 0:
                        if scalefactor < 1:
                            bitmaptools.rotozoom(bitframe,odg.bitmap,scale=scalefactor)
                    while adafruit_ticks.ticks_less(adafruit_ticks.ticks_ms(),start):
                        pass
                if cmnd.upper() == "Q":
                    break

            try:
                splash.pop()
                odgcc = None
                facecc.bitmap.deinit()
                facecc = None
                if scalefactor < 1:
                    bitframe.deinit()
                    bitframe = None
            except:
                pass

        else:
            print('Unknown filetype')

    try:
        splash.pop()
        odgcc = None
        facecc.bitmap.deinit()
        facecc = None
        if scalefactor < 1:
            bitframe.deinit()
            bitframe = None
    except:
        pass
        
    display.root_group = displayio.CIRCUITPYTHON_TERMINAL
    if '_display' not in envVars.keys():
        envVars['_display'] = display


if __name__ == "PyDOS":
    playimage(passedIn)
else:
    print("Enter 'playimage.playimage('filename')' in the REPL or PEXEC command to run.")
