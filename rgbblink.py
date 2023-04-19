import time
from pydos_ui import Pydos_ui
from pydos_rgb import PyDOS_rgb

def rgbblink(rgbPin=None,size=0):
    Pydos_rgb = PyDOS_rgb(rgbPin,size)

    if Pydos_rgb.size > 0:
        icolor = 0
        cmnd = ""

        print("listening..., enter Q to exit")

        while cmnd.upper() != "Q":

            if Pydos_ui.serial_bytes_available():
                cmnd = Pydos_ui.read_keyboard(1)

            icolor = icolor + 1
            icolor = icolor % 3

            Pydos_rgb.fill(((icolor == 1) * 20, (icolor == 2) * 50, (icolor == 0)*150))
            time.sleep(0.5)
            Pydos_rgb.fill((0, 0, 0))
            time.sleep(0.5)

        Pydos_rgb.deinit()

if __name__ == "PyDOS":
    if passedIn != "":
        ledPin = passedIn
    else:
        ledPin = None

    rgbblink(ledPin,1)
else:
    print("Enter 'rgbblink.rgbblink(pin=Default,size=1)' in the REPL to run.")
