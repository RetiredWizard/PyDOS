import os
import time
import sys
import gc
import uselect


def PyDOS():

    def anyKey():

        print("Press any key to continue . . . .")

        spoll = uselect.poll()
        spoll.register(sys.stdin,uselect.POLLIN)

        while not spoll.poll(0):
            time.sleep(.25)

        sys.stdin.read(1)

        spoll.unregister(sys.stdin)

        return()

# The main function that checks if two given strings match.
# The first string may contain wildcard characters
    def match(first, second):

        # If we reach at the end of both strings, we are done
        if len(first) == 0 and len(second) == 0:
            return True

        # Make sure that the characters after '*' are present
        # in second string. This function assumes that the first
        # string will not contain two consecutive '*'
        if len(first) > 1 and first[0] == '*' and  len(second) == 0:
            return False

        # If the first string contains '?', or current characters
        # of both strings match
        if (len(first) > 1 and first[0] == '?') or (len(first) != 0
            and len(second) !=0 and first[0] == second[0]):
            return match(first[1:],second[1:]);

        # If there is *, then there are two possibilities
        # a) We consider current character of second string
        # b) We ignore current character of second string.
        if len(first) !=0 and first[0] == '*':
            return match(first[1:],second) or match(first,second[1:])

        return False

    def weekDay():
        offset = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        week   = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
        month = time.localtime()[1]
        day = time.localtime()[2]
        year = time.localtime()[0]
        afterFeb = 1
        if month > 2: afterFeb = 0
        aux = year - 1700 - afterFeb
        # dayOfWeek for 1700/1/1 = 5, Friday
        dayOfWeek  = 5
        # partial sum of days betweem current date and 1700/1/1
        dayOfWeek += (aux + afterFeb) * 365
        # leap year correction
        dayOfWeek += aux / 4 - aux / 100 + (aux + 100) / 400
        # sum monthly and day offsets
        dayOfWeek += offset[month - 1] + (day - 1)
        dayOfWeek %= 7
        return week[int(dayOfWeek)]

    def exCmd(cFile,passedIn):
    #    try:
        if True:
            exec("passedIn = '"+passedIn+"'\n"+open(cFile).read())
    #    except SyntaxError:
    #        print("A syntax error was detected in",cFile)
    #    except:
    #        print("An exception occurred in the",cFile,"python script")

        return


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

    def prDir(dirPath,switches):
        screenlines = 22
        wideCount = 0

        def dirLine(fType,dFile,fSize,fTime,swWide):

            if swWide:
                if fType == "D":
                    print("["+dFile[:13]+"]"+" "*(14-len(dFile[:13])),end="")
                else:
                    print(dFile[:15]+" "*(16-len(dFile[:15])),end="")
            else:
                if fType == "D":
                    print(dFile+" "*(24-len(dFile))+"<DIR>"+" "*18+"%2.2i-%2.2i-%4.4i %2.2i:%2.2i" % (fTime[0], fTime[1], fTime[2], fTime[3], fTime[4]))
                else:
                    print(dFile+" "*(35-len(dFile)+10-len(fSize)),fSize,"%2.2i-%2.2i-%4.4i %2.2i:%2.2i" % (fTime[0], fTime[1], fTime[2], fTime[3], fTime[4]))

            return()

        def dirSummary(screenlines,swPause,swWide,nLines,nFiles,tFSize,nDirs,availDisk):
            retLines = 2
            if swWide:
                print()
            if swPause and nLines == screenlines:
                anyKey()
                retLines = -2
            print(" "*(4-len(str(nFiles))),nFiles,"File(s)"+" "*(32-len(str(tFSize))),tFSize,"Bytes.")
            if swPause and nLines+1 == screenlines:
                anyKey()
                retLines = -1
            print(" "*(4-len(str(nDirs))),nDirs,"Dir(s)"+" "*(33-len(str(availDisk))),availDisk,"Bytes free.")
            return(retLines)


        def txtFileTime(fPath):
            retTime = time.localtime(min(2145916800,os.stat(fPath)[9]))
            fTime = []
            fTime.append(retTime[1])
            fTime.append(retTime[2])
            fTime.append(retTime[0])
            fTime.append(retTime[3])
            fTime.append(retTime[4])
            return(fTime)

        swError = False
        swPause = False
        swWide = False
        for i in range(len(switches)):
            if switches[i][0] == 'P':
                swPause = True
            elif switches[i][0] == 'W':
                swWide = True
            else:
                print("Illeagal switch:",switches[i][0],"Command Format: DIR/p/w/o:[[-]n,e,s,d]/s [path][file]")
                swError = True
                break
        if swError:
            return

        savDir = os.getcwd()
        fullPath = absolutePath(dirPath,savDir)

        pathDirs = fullPath.split("/")
        lastDir = pathDirs.pop(-1)

        (validPath, tmpDir) = chkPath(pathDirs)

        if validPath:

            os.chdir(tmpDir)

            if tmpDir == "/":
                pathDirs = [""]
            else:
                pathDirs = tmpDir.split("/")

            # Check for relative directory from possible mount point root
            if len(pathDirs) == 2:
                if lastDir == ".":
                    os.chdir('/')
                    lastDir = tmpDir[1:]
                elif lastDir == "..":
                    os.chdir('/')
                    lastDir = ""

            tmpDir = os.getcwd()
            # listdir() doesn't return sd mount point in some cases if chdir not done here
            # os.chdir(tmpDir)

            if lastDir in os.listdir() or lastDir in ".." or "*" in lastDir or "?" in lastDir:

                if "*" in lastDir or "?" in lastDir:
                    nDirs = 0
                    nFiles = 0
                    nLines = 1
                    dPath = tmpDir+("/" if tmpDir[-1] != "/" else "")
                    print("Directory of", tmpDir)
                    for dir in os.listdir():
                        if os.stat(dPath+dir)[0] & (2**15) == 0 and match(lastDir,dir[:16]):
                            fTime = txtFileTime(dPath+dir)
                            if swPause and nLines == screenlines:
                                anyKey()
                                nLines = 0
                            if swWide:
                                if wideCount == 4:
                                    wideCount = 0
                                    print()
                                    nLines += 1
                                wideCount += 1

                            dirLine("D",dir,0,fTime,swWide)
                            nDirs += 1
                            if not swWide:
                                nLines += 1

                    tFSize = 0
                    availDisk = os.statvfs(tmpDir)[1]*os.statvfs(tmpDir)[4]
                    for dir in os.listdir():
                        if os.stat(dPath+dir)[0] & (2**15) != 0 and match(lastDir,dir[:16]):
                            fSize = str(os.stat(dPath+dir)[6])
                            tFSize += os.stat(dPath+dir)[6]
                            fTime = txtFileTime(dPath+dir)
                            if swPause and nLines == screenlines:
                                anyKey()
                                nLines = 0
                            if swWide:
                                if wideCount == 4:
                                    wideCount = 0
                                    print()
                                    nLines += 1
                                wideCount += 1

                            dirLine("F",dir,fSize,fTime,swWide)
                            nFiles += 1
                            if not swWide:
                                nLines += 1

                    rLines = dirSummary(screenlines,swPause,swWide,nLines,nFiles,tFSize,nDirs,availDisk)
                    if rLines < 0:
                        nLines = -rLines
                    else:
                        nLines += rLines

                elif os.stat(lastDir)[0] & (2**15) == 0:

                    nDirs = 2
                    nFiles = 0
                    nLines = 3
                    dPath = tmpDir+("/" if tmpDir[-1] != "/" else "")+lastDir
                    # when dPath = "/." sd mount point not included in directory list
                    if dPath == "/.":
                        dPath = "/"
                        lastDir = ""
                    print("Directory of", dPath)
                    if swWide:
                        print("[.]             [..]            ",end="")
                        wideCount = 2
                    else:
                        print("."+" "*23+"<DIR>")
                        print(".."+" "*22+"<DIR>")
                    for dir in os.listdir(lastDir):
                        if os.stat(lastDir+"/"+dir)[0] & (2**15) == 0:
                            fTime = txtFileTime(lastDir+"/"+dir)
                            if swPause and nLines == screenlines:
                                anyKey()
                                nLines = 0
                            if swWide:
                                if wideCount == 4:
                                    wideCount = 0
                                    print()
                                    nLines += 1
                                wideCount += 1

                            dirLine("D",dir,0,fTime,swWide)
                            nDirs += 1
                            if not swWide:
                                nLines += 1

                    tFSize = 0
                    availDisk = os.statvfs(dPath)[1]*os.statvfs(dPath)[4]
                    for dir in os.listdir(lastDir):
                        if os.stat(lastDir+"/"+dir)[0] & (2**15) != 0:
                            fSize = str(os.stat(lastDir+"/"+dir)[6])
                            tFSize += int(fSize)
                            fTime = txtFileTime(lastDir+"/"+dir)
                            if swPause and nLines == screenlines:
                                anyKey()
                                nLines = 0
                            if swWide:
                                if wideCount == 4:
                                    wideCount = 0
                                    print()
                                    nLines += 1
                                wideCount += 1

                            dirLine("F",dir,fSize,fTime,swWide)
                            nFiles += 1
                            if not swWide:
                                nLines += 1

                    rLines = dirSummary(screenlines,swPause,swWide,nLines,nFiles,tFSize,nDirs,availDisk)
                    if rLines < 0:
                        nLines = -rLines
                    else:
                        nLines += rLines
                else:
                    nDirs = 0
                    nFiles = 1
                    nLines = 1
                    availDisk = os.statvfs(tmpDir)[1]*os.statvfs(tmpDir)[4]
                    print("Directory of",tmpDir)
                    fSize = str(os.stat(lastDir)[6])
                    tFSize = int(fSize)
                    fTime = txtFileTime(lastDir)
                    dirLine("F",lastDir,fSize,fTime,swWide)
                    rLines = dirSummary(screenlines,swPause,swWide,nLines,nFiles,tFSize,nDirs,availDisk)
                    if rLines < 0:
                        nLines = -rLines
                    else:
                        nLines += rLines
            else:
                print("File",dirPath,"not found. (1)")

            os.chdir(savDir)
        else:
            print("File",dirPath,"not found. (2)")

        return

    def filecpy(file1,file2):
        gc.collect()
        gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
        fOrig = open(file1)
        gc.collect()
        fCopy = open(file2, "wb")
        gc.collect()
        fCopy.write(fOrig.read())
        fOrig.close()
        fCopy.close()
        gc.collect()
        return


    cmd = ""
    os.chdir("/")
    while True:
        cmdLine = input("\n("+str(gc.mem_free())+") "+os.getcwd()+">")
        args = cmdLine.split(" ")

        if len(args) > 1:
            i = 0
            iEnd = len(args)
            for e in range(0, iEnd):
                if args[i].strip() == "":
                    args.pop(i)
                else:
                    i += 1

        switches = (args[0].upper()).split('/')
        cmd = switches.pop(0)

        if cmd == "DIR":
# Command switches /p/w/a:[d]/o:[[-]n,e,s,d]/s needs to be implemented

            if len(args) == 1:

                prDir(os.getcwd(),switches)

            elif len(args) == 2:

                prDir(args[1],switches)

            else:
                print("Too many arguments. Command Format: DIR/p/w/o:[[-]n,e,s,d]/s [path][file]")

        elif cmd == "DATE":
            print("The current date is: "+weekDay()+" %2.2i/%2.2i/%4.4i" % (time.localtime()[1], time.localtime()[2], time.localtime()[0]))

        elif cmd == "TIME":
            print("The current time is: %2.2i:%2.2i:%2.2i" % (time.localtime()[3], time.localtime()[4], time.localtime()[5]))

        elif cmd == "MEM":
            gc.collect()
            gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
            print("\n%10i Kb free conventional memory" % (int(gc.mem_free()/1000)))

        elif cmd == "RENAME" or cmd == "REN" or cmd == "MOVE" or cmd == "MV":
# Move command should really work more like copy where source can be file and target can be a directory
# Wildcard renames should be implemented

            if len(args) == 3:
                aPath = args[1].split("/")
                newdir = aPath.pop(-1)

# Check that first argument has a valid path and exists
                if chkPath(aPath)[0] and newdir in os.listdir(args[1][0:max(0,len(args[1])-len(newdir)-1)]) and args[1][-1] != "/":

                    aPath2 = args[2].split("/")
                    newdir2 = aPath2.pop(-1)

# Second argument has valid path
                    if chkPath(aPath2)[0] and args[2][-1] != "/":
# Check that second argument doesn't specify an existing target
                        if newdir2 not in os.listdir(args[2][0:max(0,len(args[2])-len(newdir2)-1)]):
                            currDRen = False
                            savDir = os.getcwd()
                            os.chdir(args[1][0:max(0,len(args[1])-len(newdir)-1)])
                            if os.stat(newdir)[0] & (2**15) == 0:
                                os.chdir(newdir)
                                if savDir == os.getcwd():
                                    currDRen = True
                            os.chdir(savDir)
                            os.rename(args[1],args[2])
                            if currDRen:
                                os.chdir("..")

                        else:
                            print("Target file exists")
                    else:
                        print("Invalid target:",args[2])
                else:
                    print("No such file:",args[1])
            else:
                print("Wrong number of arguments")

        elif cmd == "DELETE" or cmd == "DEL":

            if len(args) == 2:
                savDir = os.getcwd()
                args[1] = absolutePath(args[1],savDir)

                aPath = args[1].split("/")
                newdir = aPath.pop(-1)
                (validPath, tmpDir) = chkPath(aPath)
                if tmpDir[-1] != "/":
                    tmpDir += "/"
                if validPath:
                    if "*" in newdir or "?" in newdir:
                        ans = "Y"
                        if newdir == "*" or newdir == "*.*":
                            ans = input(tmpDir+newdir+", Are you sure (y/n)? ").upper()

                        if ans == "Y":
                            for dir in os.listdir(tmpDir[:(-1 if tmpDir != "/" else None)]):
                                if os.stat(tmpDir+dir)[0] & (2**15) != 0 and match(newdir,dir[:16]):
                                    if dir == dir[:16]:
                                        os.remove(tmpDir+dir)
                                        print(tmpDir+dir,"deleted.")
                                    else:
                                        print("Unable to delete: "+tmpDir+dir+". Filename too long for wildcard operation.")
                    else:
                        if newdir in os.listdir(tmpDir[:(-1 if tmpDir != "/" else None)]) and os.stat(tmpDir+newdir)[0] & (2**15) != 0:
                            os.remove(tmpDir+newdir)
                            print(tmpDir+newdir,"deleted.")
                        else:
                            print("Unable to delete: "+tmpDir+newdir+". File not found.")
                else:
                    print("Unable to delete: "+tmpDir+newdir+". File not found.")
            else:
                print("Illeagal Path.")

        elif cmd == "TYPE":

            if len(args) == 2:
                aPath = args[1].split("/")
                newdir = aPath.pop(-1)

                if chkPath(aPath)[0] and newdir in os.listdir(args[1][0:max(0,len(args[1])-len(newdir)-1)]) and os.stat(args[1])[0] & (2**15) != 0:
                    f = open(args[1])
                    print(f.read())
                    f.close()
                else:
                    print("Unable to display: "+args[1]+". File not found.")
            else:
                print("Illeagal Path.")


        elif cmd == "CD":

            if len(args) == 1:
                print(os.getcwd())

            else:
                pathDirs = args[1].split("/")
                if chkPath(pathDirs)[0]:
                    newdir = os.getcwd()
                    os.chdir(args[1])
                    # if change to .. did nothing assume we're in root of mount point
                    if args[1] == ".." and newdir == os.getcwd():
                        os.chdir("/")
                else:
                    print("Unable to change to:",args[1])

        elif cmd == "MKDIR":
            if len(args) == 1:
                print("Unable to make .")
            elif len(args) > 2:
                print("Too many arguments")
            else:
                aPath = args[1].split("/")
                newdir = aPath.pop(-1)

                if chkPath(aPath)[0]:
                    if newdir not in os.listdir(args[1][0:max(0,len(args[1])-len(newdir)-1)]):
                        os.mkdir(args[1])
                    else:
                        print("Target name already exists")
                else:
                    print("Invalid path")

        elif cmd == "RMDIR":
            if len(args) == 1:
                print("The syntax of the command is incorrect")
            elif len(args) > 2:
                print("Too many arguments")
            else:
                aPath = args[1].split("/")
                if chkPath(aPath)[0]:
# Directory must be empty to be removed
                    if os.listdir(args[1]) == []:
                        savDir = os.getcwd()
                        os.chdir(args[1])
                        arg1Dir = os.getcwd()
                        os.chdir(savDir)
                        if arg1Dir != "/":
                            os.rmdir(args[1])
                            if savDir == arg1Dir:
                                os.chdir("..")
                        else:
                            print("Can not remove root directory")
                            os.chdir(savDir)
                    else:
                        print("The directory is not empty")
                else:
                    print("Invalid path")

        elif cmd == "COPY":

            if len(args) == 3 or len(args) == 2:
                if len(args) == 2:
                    args.append('.')

                nFiles = 0
                earlyError = False
                trailingSlash = False
                if args[1][-1] == "/":
                    print("The source file cannot be a directory")
                    earlyError = True
                if args[2][-1] == "/":
                    trailingSlash = True
                enteredArg = args[2]

                savDir = os.getcwd()
                args[1] = absolutePath(args[1],savDir)
                args[2] = absolutePath(args[2],savDir)

                aPath = args[1].split("/")
                newdir = aPath.pop(-1)

# Check that first argument has a valid path, exists and is not a directory file
                (validPath, tmpDir) = chkPath(aPath)
                if not earlyError and validPath and ("*" in newdir or "?" in newdir or (newdir in os.listdir(tmpDir) and os.stat(tmpDir+("/" if tmpDir[-1] != "/" else "")+newdir)[0] & (2**15))) != 0:
                    sourcePath = tmpDir
                    if "*" in newdir or "?" in newdir:
                        wildCardOp = True
                    else:
                        wildCardOp = False

                    aPath2 = args[2].split("/")
                    newdir2 = aPath2.pop(-1)

# Second argument has valid path
                    (validPath, tmpDir) = chkPath(aPath2)
                    if validPath:
                        gc.collect()
                        targetPath = tmpDir

                        if newdir2 in "..":
                            tmpDir = chkPath((targetPath+("/" if targetPath[-1] != "/" else "")+newdir2).split("/"))[1]
                            aPath2 = tmpDir.split("/")
                            newdir2 = aPath2.pop(-1)
                            targetPath = chkPath(aPath2)[1]


# Second argument specifies an existing target
                        if newdir2 in os.listdir(targetPath) or (targetPath == "/" and newdir2 == ""):

# Second argument target is a file
                            if os.stat(targetPath+("/" if targetPath[-1] != "/" else "")+newdir2)[0] & (2**15) != 0:
                                if trailingSlash:
                                    print("Cannot find the specified path: ",enteredArg)
                                elif wildCardOp:
                                    print("Target must be directory for wildcard copy ",enteredArg)

                                elif sourcePath == targetPath and newdir == newdir2:
                                    print("The file cannot be copied onto itself")

                                elif input("Overwrite "+args[2]+"? (y/n): ").upper() == "Y":
                                    os.remove(targetPath+("/" if targetPath[-1] != "/" else "")+newdir2)
                                    filecpy(sourcePath+("/" if sourcePath[-1] != "/" else "")+newdir,targetPath+("/" if targetPath[-1] != "/" else "")+newdir2)
                                    nFiles += 1

# Second argument target is a directory
                            else:
                                if sourcePath[-1] != "/":
                                    sourcePath += "/"
                                if targetPath[-1] != "/":
                                    targetPath += "/"

                                if wildCardOp:
                                    ans = ""
                                    for dir in os.listdir(sourcePath[:(-1 if sourcePath != "/" else None)]):
                                        if os.stat(sourcePath+dir)[0] & (2**15) != 0 and match(newdir,dir[:16]):
                                            print("copy",sourcePath+dir,"to",targetPath+newdir2+("" if newdir2 == "" else "/")+dir)
                                            if dir in os.listdir(targetPath+newdir2):
                                                if sourcePath == targetPath+newdir2+("" if newdir2 == "" else "/"):
                                                    print("The file cannot be copied onto itself")
                                                    break
                                                else:
                                                    if ans != "A":
                                                        ans = input("Overwrite "+targetPath+newdir2+("" if newdir2 == "" else "/")+dir+"? (y/n/(q)uit/(a)ll): ").upper()
                                                    if ans  == "Y" or ans == "A":
                                                        filecpy(sourcePath+dir,targetPath+newdir2+("" if newdir2 == "" else "/")+dir)
                                                        nFiles += 1
                                                    elif ans == "Q":
                                                        break
                                            else:
                                                filecpy(sourcePath+dir,targetPath+newdir2+("" if newdir2 == "" else "/")+dir)
                                                nFiles += 1
                                            gc.collect()

                                elif newdir in os.listdir(targetPath+newdir2):
                                    if input("Overwrite "+targetPath+newdir2+("" if newdir2 == "" else "/")+newdir+"? (y/n): ").upper() == "Y":
                                        os.remove(targetPath+newdir2+("" if newdir2 == "" else "/")+newdir)
                                        filecpy(sourcePath+newdir,targetPath+newdir2+("" if newdir2 == "" else "/")+newdir)
                                        nFiles += 1

                                else:
                                    filecpy(sourcePath+newdir,targetPath+newdir2+("" if newdir2 == "" else "/")+newdir)
                                    nFiles += 1

# Second argument is a new file
                        else:
                            if trailingSlash or wildCardOp:
                                if wildCardOp:
                                    print("Target must be directory for wildcard copy ",enteredArg)
                                else:
                                    print("Cannot find the specified path: ",enteredArg)
                            else:
                                filecpy(sourcePath+("/" if sourcePath[-1] != "/" else "")+newdir,targetPath+("/" if targetPath[-1] != "/" else "")+newdir2)
                                nFiles += 1

                        print(" "*7,nFiles,"files(s) copied.")
                    else:
                        print("Invalid destination:",args[2])
                else:
                    print("No such file:",args[1])
            else:
                print("Wrong number of arguments")

        elif cmd == "EXIT":
            break

        elif cmd == "":
            continue

        else:
            aPath = args[0].split("/")
            newdir = aPath.pop(-1)
            if len(args) == 1:
                passedIn = ""
            elif len(args) > 1:
                passedIn = args[1]

#            if args[0] in os.listdir() and os.stat(args[0])[0] & (2**15)!= 0 and ((args[0].split("."))[1]).upper() == "PY":

            if  ((args[0].split("."))[-1]).upper() == "PY":
                if chkPath(aPath)[0] and newdir in os.listdir(args[0][0:max(0,len(args[0])-len(newdir)-1)]) and os.stat(args[0])[0] & (2**15) != 0:

#               __import__((args[0].split("."))[0])
                    exCmd(args[0],passedIn)
                else:
                    print("Illegal command:",args[0]+".")
            elif chkPath(aPath)[0]:
                if newdir+".py" in os.listdir(args[0][0:max(0,len(args[0])-len(newdir)-1)]) and os.stat(args[0]+".py")[0] & (2**15) != 0:
                    exCmd(args[0]+".py",passedIn)
                elif newdir+".PY" in os.listdir(args[0][0:max(0,len(args[0])-len(newdir)-1)]) and os.stat(args[0]+".PY")[0] & (2**15) != 0:
                    exCmd(args[0]+".PY",passedIn)
                elif newdir+".Py" in os.listdir(args[0][0:max(0,len(args[0])-len(newdir)-1)]) and os.stat(args[0]+".Py")[0] & (2**15) != 0:
                    exCmd(args[0]+".Py",passedIn)
                elif newdir+".pY" in os.listdir(args[0][0:max(0,len(args[0])-len(newdir)-1)]) and os.stat(args[0]+".pY")[0] & (2**15) != 0:
                    exCmd(args[0]+".pY",passedIn)
                else:
                    print("Illegal command:",args[0]+".")
            else:
                print("Illegal command:",args[0]+".")


if __name__ == "__PyDOS__":
    PyDOS()

PyDOS()