from sys import implementation
from pydos_hw import Pydos_hw
import os

if implementation.name.upper() == "MICROPYTHON":
    from sys import print_exception
    from machine import Pin,SoftSPI,SPI
    try:
        from machine import SDCard
    except:
        pass
    import sdcard
elif implementation.name.upper() == "CIRCUITPYTHON":
    import adafruit_sdcard
    import storage


def sdMount(drive):

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

    def do_mount(drive):
        sdMounted = False

        if implementation.name.upper() == "MICROPYTHON":
            if Pydos_hw.SD_SCK and not altSPI:
                try:
                    os.mount(SDCard(), drive)
                    sdMounted = True
                except:
                    pass

                if not sdMounted:
                    try:
                        sd = sdcard.SDCard(Pydos_hw.SD_SPI(), Pin(Pydos_hw.SD_CS,Pin.OUT))
                        os.mount( sd, drive)
                        sdMounted = True
                    except Exception as e:
                        print_exception(e)
            else:
                try:
                    sd = sdcard.SDCard(Pydos_hw.SPI(), Pin(Pydos_hw.CS,Pin.OUT))
                    os.mount( sd, drive)
                    sdMounted = True
                except Exception as e:
                    print_exception(e)

        elif implementation.name.upper() == "CIRCUITPYTHON":
            if not Pydos_hw.SD_CS and not Pydos_hw.CS:
                print("CS Pin not allocated for SDCard SPI interface")
            else:
                try:
                    if altSPI:
                        sd = adafruit_sdcard.SDCard(Pydos_hw.SPI(), Pydos_hw.CS)
                    else:
                        if Pydos_hw.SD_CS:
                            sd = adafruit_sdcard.SDCard(Pydos_hw.SD_SPI(), Pydos_hw.SD_CS)
                        elif Pydos_hw.CS:
                            sd = adafruit_sdcard.SDCard(Pydos_hw.SD_SPI(), Pydos_hw.CS)
                    vfs = storage.VfsFat(sd)
                    storage.mount(vfs, drive)
                    sdMounted = True
                except Exception as e:
                    print('SD-Card: Fail,', e)

        if sdMounted:
            print(drive+" mounted")
            # nano connect/Tennsy 4.1 are special cases becuase LED uses the SPI SCK pin
            if os.uname().machine in ["Arduino Nano RP2040 Connect with rp2040", \
                "Arduino Nano RP2040 Connect with RP2040", \
                "TinyPICO with ESP32-PICO-D4"] and not altSPI:

                envVars[".sd_drive"] = drive

            if os.uname().machine in ["Teensy 4.1 with IMXRT1062DVJ6A", \
                'Teensy 4.1 with MIMXRT1062DVJ6A'] and altSPI:

                envVars[".sd_drive"] = drive

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
                print("Target must be in root")
            else:
                do_mount(tmpDir+newdir)
        else:
            print("Target name already exists")
    else:
        print("Invalid path")

    return

drive = "/sd"
altSPI = False

if __name__ != "PyDOS":
    passedIn = ""
    envVars = {}

if passedIn != "":
    drive = passedIn.split(',')
    if len(drive) > 1:
        altSPI = True
    drive = drive[0]

sdMount(drive)
