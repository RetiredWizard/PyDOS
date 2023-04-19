from sys import implementation
from pydos_hw import Pydos_hw
import os

if implementation.name.upper() == "MICROPYTHON":
    from sys import print_exception
    from machine import Pin
    try:
        from machine import SDCard
    except:
        pass
    import sdcard as sdcardLIB
elif implementation.name.upper() == "CIRCUITPYTHON":
    from digitalio import DigitalInOut
    # Teensy 4.1 needs adafruit_scard so must try that first
    try:
        import adafruit_sdcard
    except:
        import sdcardio as adafruit_sdcard
    import storage


def sdMount(drive,spiNo):

    def chkPath(tstPath):
        validPath = True

        simpPath = ""
        if tstPath == []:
            validPath = True
            simpPath = ""
        else:

            savDir = os.getcwd()

            for path in tstPath:
                if path == "":
                    os.chdir("/")

                elif os.getcwd() == "/" and path == "..":
                    validPath = False
                    break

                elif path == ".":
                    continue

                elif path == ".." and len(os.getcwd().split('/')) == 2:
                    os.chdir('/')

                elif path == "..":
                    os.chdir("..")

                elif path in os.listdir() and (os.stat(path)[0] & (2**15) == 0):
                    os.chdir(path)

                else:
                    validPath = False
                    simpPath = ""
                    break

            if validPath:
                simpPath = os.getcwd()
            os.chdir(savDir)

        return((validPath,simpPath))

    def absolutePath(argPath,currDir):

        if argPath[0] == '/':
            fullPath = argPath
        elif currDir == '/':
            fullPath = '/'+argPath
        else:
            fullPath = currDir+'/'+argPath

        if len(fullPath) > 1 and fullPath[-1] == '/':
            fullPath = fullPath[:-1]

        return(fullPath)

    def do_mount(drive,spiNo):
        sdMounted = False

        if implementation.name.upper() == "MICROPYTHON":

            if spiNo+1 > len(Pydos_hw.CS):
                print("CS Pin not allocated for Pydos_bcfg SPI interface #",spiNo)
            elif Pydos_hw.SDdrive[spiNo] != None:
                print("SD card on Pydos_bcfg SPI interface #",spiNo,"already mounted as",Pydos_hw.SDdrive[spiNo])
            else:
                if spiNo == 0:
                    try:
                        os.mount(SDCard(), drive)
                        os.listdir(drive)  # Check that card is accessible
                        Pydos_hw.SDdrive[spiNo] = drive
                        sdMounted = True
                    except:
                        # Failed use of machine.SDCard() may have corrupted SPI for DotStar
                        if Pydos_hw.dotStar_Clock:
                            from pydos_rgb import PyDOS_rgb
                            PyDOS_rgb._spi = [None]
                            PyDOS_rgb._pixels[0] = None
                            PyDOS_rgb._rgblist[0] = [()]
                            PyDOS_rgb._neoName[0] = None
                    if not sdMounted:
                        for slot in range(4):
                            try:
                                os.mount(SDCard(slot=slot), drive)
                                os.listdir(drive)  # Check that card is accessible
                                Pydos_hw.SDdrive[spiNo] = drive
                                sdMounted = True
                                break
                            except:
                                # Failed use of machine.SDCard() may have corrupted SPI for DotStar
                                if Pydos_hw.dotStar_Clock:
                                    from pydos_rgb import PyDOS_rgb
                                    PyDOS_rgb._spi = [None]
                                    PyDOS_rgb._pixels[0] = None
                                    PyDOS_rgb._rgblist[0] = [()]
                                    PyDOS_rgb._neoName[0] = None
                if not sdMounted:
                    try:
                        sd = sdcardLIB.SDCard(Pydos_hw.SPI(spiNo), Pin(Pydos_hw.CS[spiNo],Pin.OUT))
                        os.mount( sd, drive)
                        Pydos_hw.SDdrive[spiNo] = drive
                        sdMounted = True
                    except Exception as e:
                        print_exception(e)

        elif implementation.name.upper() == "CIRCUITPYTHON":

            if spiNo+1 > len(Pydos_hw.CS):
                print("CS Pin not allocated for Pydos_bcfg SPI interface #",spiNo)
            elif Pydos_hw.SDdrive[spiNo] != None:
                print("SD card on Pydos_bcfg SPI interface #",spiNo,"already mounted as",Pydos_hw.SDdrive[spiNo])
            else:
                _cs = Pydos_hw.CS[spiNo]

                try:
                    if not Pydos_hw.SD[spiNo]:
                        Pydos_hw.SD[spiNo] = adafruit_sdcard.SDCard(Pydos_hw.SPI(spiNo), _cs)
                    vfs = storage.VfsFat(Pydos_hw.SD[spiNo])
                    storage.mount(vfs, drive)
                    Pydos_hw.SDdrive[spiNo] = drive
                    sdMounted = True
                except Exception as e:
                    print('SD-Card: Fail,', e)

        if sdMounted:
            print(drive+" mounted")

        return

    savDir = os.getcwd()
    args = absolutePath(drive,savDir)

    aPath = drive.split("/")
    newdir = aPath.pop(-1)
    (validPath, tmpDir) = chkPath(aPath)
    if tmpDir == "" or tmpDir[-1] != "/":
        tmpDir += "/"

    if validPath:
        if newdir not in os.listdir(tmpDir[:(-1 if tmpDir != "/" else None)]):
            if (tmpDir+newdir)[1:].find('/') != -1:
                print("Target must be in root folder")
            elif tmpDir+newdir == '/':
                print("Target can not be root folder")
            else:
                do_mount(tmpDir+newdir,spiNo)
        else:
            print("Target name already exists")
    else:
        print("Invalid path")

    return

drive = "/sd"
spiNo = 0

if __name__ != "PyDOS":
    passedIn = ""
    envVars = {}

if passedIn != "":
    drive = passedIn.split(',')
    if len(drive) > 1:
        spiNo = int(drive[1])
    drive = drive[0]

sdMount(drive,spiNo)
