if passedIn == "":
    passedIn = input("Enter RO or RW: ")
    
if passedIn.upper() != "RO" and passedIn.upper() != "RW":
    print ("Invalid Option")
else:
    if passedIn.upper() == "RW":
        readOnly = "False"
    else:
        readOnly = "True"
    f = open('boot.py','w')
    f.write('import storage'+"\n")
    f.write('storage.remount("/",'+readOnly+")\n")
    f.close()
