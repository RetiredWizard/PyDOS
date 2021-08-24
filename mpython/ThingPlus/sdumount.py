import os
drive = "/sd"

if __name__ != "PyDOS":
    passedIn = ""

if passedIn != "":
    drive = passedIn
os.umount(drive)