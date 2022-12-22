from sys import implementation
from pydos_hw import Pydos_hw
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

unmounted = False
for i in range(len(Pydos_hw.SDdrive)):
    if drive == Pydos_hw.SDdrive[i]:
        umount(drive)
        unmounted = True
        if Pydos_hw.SD[i]:    # Micropython doesn't use Pydos_hw.SD
            if 'deinit' in dir(Pydos_hw.SD[i]):
                Pydos_hw.SD[i].deinit()
            Pydos_hw.SD[i] = None
        Pydos_hw.SDdrive[i] = None
        break

if not unmounted and drive != '/':
    try:
        umount(drive)
    except:
        print("Mount point "+drive+" not found.")
elif drive == '/':
    print("Can't umount root folder")
