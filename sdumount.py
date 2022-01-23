from sys import implementation
from pydos_ui import PyDOS_UI
if implementation.name.upper() == "MICROPYTHON":
    from os import umount
elif implementation.name.upper() == "CIRCUITPYTHON":
    from storage import umount

drive = "/sd"

if __name__ != "PyDOS":
    passedIn = ""

if passedIn != "":
    drive = passedIn

umount(drive)
if implementation.name.upper() == "CIRCUITPYTHON":
    PyDOS_UI.SD_CSdeinit()
