from sys import implementation
if implementation.name.upper() == "MICROPYTHON":
    from os import umount
elif implementation.name.upper() == "CIRCUITPYTHON":
    from storage import umount

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
