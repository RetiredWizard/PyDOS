import os
from pydos_ui import Pydos_ui
try:
    from pydos_ui import input
except:
    pass
#import uselect

def viewFile(args):

    #def kbdInterrupt():

        #spoll = uselect.poll()
        #spoll.register(sys.stdin,uselect.POLLIN)

        #while not spoll.poll(0):
            #time.sleep(.25)

        #cmnd = sys.stdin.read(1)

        #spoll.unregister(sys.stdin)

        #return(cmnd)

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

        scrLines = int(envVars["_scrHeight"])
        scrWidth = int(envVars["_scrWidth"])
    else:
        scrLines = 24
        scrWidth = 80

    savDir = os.getcwd()
    args = absolutePath(args,savDir)

    aPath = args.split("/")
    newdir = aPath.pop(-1)
    (validPath, tmpDir) = chkPath(aPath)

    if validPath and newdir in os.listdir(tmpDir) and os.stat(tmpDir+("/" if tmpDir[-1] != "/" else "")+newdir)[0] & (2**15) != 0:
        f = open(args)
        index = [0]
        currLineNum = 0
        maxRead = 0
        eof = -1
        for i in range(scrLines):
            line = f.readline()
            if line != "":
                index.append(index[i]+len(line))
                print()
                print((line[:-1])[:scrWidth],end="")
                currLineNum += 1
                maxRead += 1
            else:
                eof = currLineNum
                break

        cmnd = ""
        seqCnt = 0
        while cmnd.upper() != "Q":
            #cmnd = kbdInterrupt()
            cmnd = Pydos_ui.read_keyboard(1)

            if ord(cmnd) == 27 and seqCnt == 0:
                seqCnt = 1
            elif ord(cmnd) == 91 and seqCnt == 1:
                seqCnt = 2
            elif ord(cmnd) == 65 and seqCnt == 2:
                # Up Arrow
                seqCnt = 0
                if currLineNum > scrLines:
                    currLineNum -= 1
                    print (chr(27)+"[1;1H"+chr(27)+"M",end="")
                    #print (chr(27)+"[2;0H"+chr(27)+"[T",end="")
                    f.seek(index[currLineNum-scrLines])
                    print((f.readline()[:-1])[:scrWidth],end="")

            elif ord(cmnd) == 66 and seqCnt == 2:
                # Down Arrow
                seqCnt = 0
                if eof == -1 or currLineNum < eof:
                    f.seek(index[currLineNum])
                    line = f.readline()
                    if line != "":
                        if currLineNum == maxRead:
                            index.append(index[currLineNum]+len(line))
                            maxRead += 1
                        print(chr(27)+"["+str(scrLines)+";1H"+chr(27)+"D",end="")
                        #print(chr(27)+"["+str(scrLines+1)+";0H"+chr(27)+"[S",end="")
                        print((line[:-1])[:scrWidth],end="")
                        currLineNum += 1
                    else:
                        eof = currLineNum

            elif ord(cmnd) == 67 and seqCnt == 2:
                # Right Arrow
                seqCnt = 0
            elif ord(cmnd) == 68 and seqCnt == 2:
                # Left Arrow
                seqCnt = 0
            else:
                seqCnt = 0


        print(chr(27)+"["+str(scrLines)+";1H",end="")
        f.close()
    else:
        print("Unable to display: "+args+". File not found.")

if __name__ != "PyDOS":
    passedIn = ""

if passedIn == "":
    passedIn = input("Enter filename:")

viewFile(passedIn)
