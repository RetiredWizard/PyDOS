import os
drive = "/sd"
if passedIn != "":
    drive = passedIn
os.umount(drive)
