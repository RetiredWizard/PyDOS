import os
import time
import sys
try:
    from pydos_ui import input
except:
    pass
if sys.implementation.name.upper() == "MICROPYTHON":
    import uselect

def fileDiff(args):

    def anyKey():

        if sys.implementation.name.upper() == "CIRCUITPYTHON":

            keyIn = input("Press enter to continue . . . .")

        else:

            spoll = uselect.poll()
            spoll.register(sys.stdin,uselect.POLLIN)

            while spoll.poll(0):
                sys.stdin.read(1)

            print("Press any key to continue . . . .",end="")

            keyIn=chr(1)
            while ord(keyIn) < 30 and ord(keyIn) != 10:
                spoll.poll(-1)  # [0][1] != uselect.POLLIN
                keyIn = sys.stdin.read(1)

            spoll.unregister(sys.stdin)
            print("")

        return(keyIn)

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

    if __name__ == "PyDOS":
        global envVars

        scrLines = int(envVars["_scrHeight"])-1
    else:
        scrLines = 23

    dispdLns = 0

    file1 = args.split(",")[0]
    file2 = args.split(",")[1]

    savDir = os.getcwd()
    file1 = absolutePath(file1,savDir)
    file2 = absolutePath(file2,savDir)

    file1Path = file1.split("/")
    file2Path = file2.split("/")

    file1Dir = file1Path.pop(-1)
    (validPath, tmpDir) = chkPath(file1Path)

    if validPath and file1Dir in os.listdir(tmpDir) and os.stat(tmpDir+("/" if tmpDir[-1] != "/" else "")+file1Dir)[0] & (2**15) != 0:

        file2Dir = file2Path.pop(-1)
        (validPath, tmpDir) = chkPath(file2Path)

        if validPath and file2Dir in os.listdir(tmpDir) and os.stat(tmpDir+("/" if tmpDir[-1] != "/" else "")+file2Dir)[0] & (2**15) != 0:

            f1 = open(file1)
            f2 = open(file2)
            filesSame = True

            line1 = f1.readline()
            fndDiff = False
            sndDiff = False
            lastMatchPos = 0

            while line1 != "":
                f2.seek(lastMatchPos)
                fpos = lastMatchPos
                line2 = f2.readline()

                # find first line2 that matches current line1
                while line2 != "" and line1 != line2:
                    fpos += len(line2)
                    line2 = f2.readline()
                    filesSame = False

                if line1 == line2:

                    # print any mis-matched records from file 2 up until current matched records
                    f2.seek(lastMatchPos)
                    while line2 != "" and lastMatchPos < fpos:
                        line2 = f2.readline()
                        if not sndDiff:
                            dispdLns += 1
                            if dispdLns >= scrLines:
                                anyKey()
                                dispdLns = 0
                            print("***** "+file2+" *****")
                            sndDiff = True
                        dispdLns += 1
                        if dispdLns >= scrLines:
                            anyKey()
                            dispdLns = 0
                        print(line2,end="")
                        lastMatchPos += len(line2)
                        filesSame = False

                    line2 = f2.readline()
                    lastMatchPos = fpos + len(line2)
                    line1 = f1.readline()
                    fndDiff = False
                    sndDiff = False
                else:
                    filesSame = False
                    if not fndDiff:
                        dispdLns += 1
                        if dispdLns >= scrLines:
                            anyKey()
                            dispdLns = 0
                        print("***** "+file1+" *****")
                        fndDiff = True
                    dispdLns += 1
                    if dispdLns >= scrLines:
                        anyKey()
                        dispdLns = 0
                    print(line1,end="")
                    line1 = f1.readline()


            f2.seek(lastMatchPos)
            line2 = f2.readline()
            while line2 != "":
                filesSame = False
                if not sndDiff:
                    dispdLns += 1
                    if dispdLns >= scrLines:
                        anyKey()
                        dispdLns = 0
                    print("***** "+file2+" *****")
                    sndDiff = True
                dispdLns += 1
                if dispdLns >= scrLines:
                    anyKey()
                    dispdLns = 0
                print(line2,end="")
                line2 = f2.readline()

            f1.close()
            f2.close()

            if filesSame:
                print("No differences encountered")

        else:
            print("File not found: "+file2)

    else:
        print("File not found: "+file1)

if __name__ != "PyDOS":
    passedIn = ""

if passedIn == "":
    passedIn = input("Enter filenames (file1,file2):")

if len(passedIn.split(",")) != 2:
    print("Wrong number of arguments, command syntax: diff file1,file2")
else:
    fileDiff(passedIn)
