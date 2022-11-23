from sys import implementation
if implementation.name.upper() == "MICROPYTHON":
    from os import umount
elif implementation.name.upper() == "CIRCUITPYTHON":
    from storage import umount
    from pydos_hw import Pydos_hw

drive = "/sd"

if __name__ != "PyDOS":
    passedIn = ""
    envVars = {}

if passedIn != "":
    drive = passedIn

if drive[0] != '/':
    drive = '/'+drive

if drive == envVars.get('.sd_drive',""):
    envVars.pop('.sd_drive',None)

umount(drive)

if implementation.name.upper() == "CIRCUITPYTHON":
    if drive == Pydos_hw.SDdrive:
        Pydos_hw.SD.deinit()
        Pydos_hw.SD = None
        Pydos_hw.SDdrive = None
    elif drive == Pydos_hw.ALT_SDdrive:
        Pydos_hw.ALT_SD.deinit()
        Pydos_hw.Alt_SD = None
        Pydos_hw.ALT_SDdrive = None
