from pydos_rgb import PyDOS_rgb
from pydos_ui import Pydos_ui
try:
    from pydos_ui import input
except:
    pass

def rgbset(ans="",rgbPin=None,size=0,pix=None):
    Pydos_rgb = PyDOS_rgb(rgbPin,size)

    if Pydos_rgb.size > 0:
        if ans == "":
            ans = input("R,G,B: ")

        if len(ans.split(",")) == 3:
            r = max(0,min(255,int((ans.split(',')[0] if ans.split(",")[0].isdigit() else 0))))
            g = max(0,min(255,int((ans.split(',')[1] if ans.split(",")[1].isdigit() else 0))))
            b = max(0,min(255,int((ans.split(',')[2] if ans.split(",")[2].isdigit() else 0))))
        else:
            r = 0
            g = 0
            b = 0

        if pix != None:
            Pydos_rgb[pix] = (r,g,b)
        else:
            Pydos_rgb.fill((r, g, b))

        allZero = True
        for i in range(Pydos_rgb.size):
            if sum(Pydos_rgb[i]) != 0:
                allZero = False
                break
        if allZero:
            Pydos_rgb.deinit()


if __name__ == "PyDOS":
    splitparams = passedIn.split(',')
    numargs = 0
    if len(splitparams) >= 3:
        ans = ",".join(splitparams[0:3])
        numargs = 1
    if len(splitparams) >= 4:
        rgbPin = splitparams[3]
        numargs = 2
    if len(splitparams) >= 5:
        size = int(splitparams[4])
        numargs = 3
    if len(splitparams) >= 6:
        pix = int(splitparams[5])
        numargs = 4
    
    if numargs == 0:
        rgbset()
    elif numargs == 1:
        rgbset(ans)
    elif numargs == 2:
        rgbset(ans,rgbPin)
    elif numargs == 3:
        rgbset(ans,rgbPin,size)
    elif numargs == 4:
        rgbset(ans,rgbPin,size,pix)
else:
    print("Enter 'rgbset.rgbset(\"r,g,b\",pin=Default,size=1,pixElem=None)' in the REPL to run.")
