import time
from pydos_ui import Pydos_ui
from pydos_rgb import PyDOS_rgb

def rgbrainbow(rgbPin=None,size=0):
    Pydos_rgb = PyDOS_rgb(rgbPin,size)

    if Pydos_rgb.size > 0:
        # attempt to balance colors
        MAXRED = 120
        MAXGREEN = 165
        MAXBLUE = 255

        # Cycle colours.
        icolor = 0
        transition = [-4,1,2,-1,4,1,-2,-1]
        cmnd = ""
        steps = 100
        r = 0
        g = 0
        b = 0

        newSteps = 0
        print("listening... Enter value to alter speed, 'q' to quit")

        while cmnd.upper() != "Q":

            icolor = (icolor + 1) % 8

            for k in range(steps):
                if Pydos_ui.serial_bytes_available():
                    cmnd = Pydos_ui.read_keyboard(1)

                    if cmnd.upper() == "Q":
                        Pydos_rgb.fill((0,0,0))
                        break
                    if cmnd == '\n':
                        if newSteps == 0:
                            print()
                        else:
                            steps = max(1,min(800,newSteps))
                            print(" New STEP value: ",steps)
                            newSteps = 0
                    if cmnd.isdigit():
                        newSteps = (newSteps * 10) + int(cmnd)
                        print(cmnd,end="")
                    elif cmnd != None:
                        print(cmnd,end="")

                r += ((abs(transition[icolor]) & 1)/transition[icolor]) * (MAXRED / steps)
                b += ((abs(transition[icolor]) & 2)/transition[icolor]) * (MAXBLUE / steps)
                g += ((abs(transition[icolor]) & 4)/transition[icolor]) * (MAXGREEN / steps)
                r = int(max(0,min(MAXRED,r)))
                b = int(max(0,min(MAXBLUE,b)))
                g = int(max(0,min(MAXGREEN,g)))

                Pydos_rgb.fill((r,g,b))

                time.sleep(0.5/steps)

            #time.sleep(0.5)

        Pydos_rgb.deinit()

if __name__ == "PyDOS":
    if passedIn != "":
        ledPin = passedIn
    else:
        ledPin = None

    rgbrainbow(ledPin,1)
else:
    print("Enter 'rgbrainbow.rgbrainbow(pin=Default,size=1)' in the REPL to run.")
