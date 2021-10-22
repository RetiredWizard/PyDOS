from sys import implementation

print("This program will set the CircuitPython filesystem access mode AFTER the next")
print("Powercycle. A Control-D softboot will NOT reset the filesystem access mode.\n")

if implementation.name.upper() != "CIRCUITPYTHON":
    print("This program only works under CircuitPython.")
    print('This microcontroller is currently running: "'+implementation.name+'"')
else:

    if __name__ != "PyDOS":
        passedIn = ""

    if passedIn == "":
        passedIn = input("Enter RO or RW: ")

    if passedIn.upper() != "RO" and passedIn.upper() != "RW":
        print ("Invalid Option")
    else:
        if passedIn.upper() == "RW":
            readOnly = "False"
        else:
            readOnly = "True"

        try:
            f = open('/boot.py','w')
            f.write('import storage'+"\n")
            f.write('storage.remount("/",'+readOnly+")\n")
            f.close()
        except:
            print("The filesystem currently appears to be readonly, you should be able to access")
            print("the flash storage as a mounted USB drive on your host system. To switch the")
            print("filesystem back to Read/Write, copy the boot.rw file to boot.py, safely")
            print("dismount the USB drive from the host and powercycle the microcontroller board.")
