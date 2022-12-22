import gc
import os
from sys import implementation

if "_match" not in dir():
    # The first string may contain wildcards
    def _match(first, second):

        # If we reach end of both strings, we are done
        if len(first) == 0 and len(second) == 0:
            return True

        # Make sure that the characters after '*' are present
        # in second string. Can't contain two consecutive '*'
        if len(first) > 1 and first[0] == '*' and  len(second) == 0:
            return False

        if (len(first) > 1 and first[0] == '?') or (len(first) != 0
            and len(second) !=0 and first[0] == second[0]):
            return _match(first[1:],second[1:]);

        if len(first) !=0 and first[0] == '*':
            return _match(first[1:],second) or _match(first,second[1:])

        return False

if "calcWildCardLen" not in dir():
    def calcWildCardLen(wildcardLen,recursiveFail):
        wildcardLen += 1
        if not recursiveFail and wildcardLen < 90:
            try:
                (wildcardLen,recursiveFail) = calcWildCardLen(wildcardLen,recursiveFail)
            except:
                recursiveFail = True

        return (wildcardLen,recursiveFail)

def xcopy():

    def chkPath(tstPath,makeDirs=False):
        validPath = True
        simpPath = ""

        if tstPath != []:
            savDir = os.getcwd()
            for path in tstPath:
                path = path.replace("C:","")
                if path == "":
                    os.chdir(slh)
                elif os.getcwd() == slh and path == "..":
                    validPath = False
                    break
                elif path == ".":
                    continue
                elif path == ".." and len(os.getcwd().split(slh)) == 2:
                    os.chdir(slh)
                elif path == "..":
                    os.chdir("..")
                elif path in os.listdir() and (os.stat(path)[0] & (2**15) == 0):
                    os.chdir(path)
                elif path in os.listdir():
                    validPath = False
                    break
                else:
                    if makeDirs:
                        os.mkdir(path)
                        os.chdir(path)
                    else:
                        validPath = False
                        break

            if validPath:
                simpPath = os.getcwd()
            os.chdir(savDir)

        return((validPath,simpPath))

    def absolutePath(argPath,currDir):

        if argPath[0] == slh:
            fullPath = argPath
        elif currDir == slh:
            fullPath = slh+argPath
        else:
            fullPath = currDir+slh+argPath

        if len(fullPath) > 1 and fullPath[-1] == slh:
            fullPath = fullPath[:-1]

        return(fullPath)

    def filecpy(file1,file2,verify=False):

        dstPath = "/".join(file2.split("/").pop(-1))
        if dstPath == "":
            dstPath = "/"
        availDisk = os.statvfs(dstPath)[1]*os.statvfs(dstPath)[4]

        if availDisk > os.stat(file1)[6]:
            print("copy",file1,"to",file2)
            gc.collect()
            with open(file2, "wb") as fCopy:
                with open(file1, 'rb') as fOrig:
                    for line in fOrig:
                        fCopy.write(line)
            if verify:
                print("Verifying "+file1+" = "+file2)
                gc.collect()
                with open(file2,'rb') as fCopy:
                    with open(file1,'rb') as fOrig:
                        for line in fOrig:
                            if line != fCopy.readline():
                                print("Error copying",file1+", new file doesn't match original")
                                break
            gc.collect()
            retVal = True
        else:
            print("Insufficient Disk Space to copy",file1)
            retVal = False

        return retVal

    def multicpy(sourcePath,newdir,targetPath,newdir2,swBits,ans=""):

        nFiles = 0
        curDLst = os.listdir(sourcePath[:(-1 if sourcePath != slh else None)])

        try:
            os.mkdir(targetPath+newdir2)
        except:
            pass

        for _dir in curDLst:
            if os.stat(sourcePath+_dir)[0] & (2**15) != 0 and _match(newdir,_dir[:wildcardLen]):
                if _dir in os.listdir(targetPath+newdir2):
                    if sourcePath == targetPath+newdir2+("" if newdir2 == "" else slh):
                        print("The file cannot be copied onto itself")
                        #break
                    else:
                        if ans != "A" and not swBits & int('001000',2):
                            ans = "*"
                            while "YNQA".find(ans) == -1:
                                ans = input("Overwrite "+targetPath+newdir2+("" if newdir2 == "" else slh)+_dir+"? (y/n/(q)uit/(a)ll): ").upper()
                        if ans  == "Y" or ans == "A" or swBits & int('001000',2):
                            if filecpy(sourcePath+_dir,targetPath+newdir2+("" if newdir2 == "" else slh)+_dir,bool(swBits&int('10000000'))):
                                nFiles += 1
                        elif ans == "Q":
                            break
                else:
                    if filecpy(sourcePath+_dir,targetPath+newdir2+("" if newdir2 == "" else slh)+_dir,bool(swBits&int('10000000'))):
                        nFiles += 1
                gc.collect()
            elif os.stat(sourcePath+_dir)[0] & (2**15) == 0 and swBits & int('000010',2):
                (nF,ans) = multicpy(sourcePath+_dir+slh,newdir,targetPath+newdir2+(slh if newdir2 != "" else ""),_dir,swBits,ans)
                if os.listdir(targetPath+newdir2+slh+_dir) == []:
                    os.rmdir(targetPath+newdir2+slh+_dir)
                nFiles += nF
                if ans == "Q":
                    break
        return (nFiles,ans)


    wildcardLen = 0
    recursiveFail = False
    slh = '/'

    (wildcardLen,recursiveFail) = calcWildCardLen(wildcardLen,recursiveFail)

    if implementation.name.upper() == "CIRCUITPYTHON":
        wildcardLen = max(1,wildcardLen-6)
    else:
        wildcardLen = max(1,wildcardLen-2)

    if wildcardLen < 40:
        print("*Warning* wild card length set to: ",wildcardLen)
    gc.collect()

    args = passedIn.strip().split(" ")
    if args == [""]:
        args = []
    switches = envVars.get("_switches",[])

    quotedArg = False
    if len(args) > 0:
        i = 0
        iEnd = len(args)
        for _ in range(0, iEnd):
            if args[i].strip() == "":
                args.pop(i)
            elif quotedArg:
                if args[i].find('"') > -1 and args[i].find('"') != len(args[i])-1:
                    break
                elif args[i][-1] == '"':
                    args[i-1] = args[i-1] + " " + args.pop(i)[:-1]
                    quotedArg = False
                else:
                    args[i-1] = args[i-1] + " " + args.pop(i)
            elif args[i][0] == '"':
                if args[i][-1] != '"':
                    args[i] = args[i][1:]
                    i += 1
                    quotedArg = True
                else:
                    args[i] = args[i][1:-1]
                    i += 1
            else:
                i += 1

        if quotedArg:
            print("Mismatched quotes.")
            cmd = ""

    # Error=1, (S)Recur=2, (P)Pause=4, (Y)Conf=8, (W)Wide=16, (D)debug=32, (Q)uiet=64,
    # (V)erify=128
    swBits = 0
    swAllB = int('11111111',2)
    for i in range(len(switches)):
        if switches[i] != "":
            swBits = swBits | (2**('SPYWDQV'.find(switches[i])+1))

#    print(args)
    earlyError = False
    trailingSlash = False
    nFiles = 0
    if len(args) < 1 or len(args) > 2:
        print ("Invalid command format: xcopy[/s][/y][/v] Source [Destination]")
        earlyError = True
    elif len(args) == 1:
        args.append(".")
    if args[1][-1] == slh:
        trailingSlash = True
    if len(args) == 2 and not swBits & (swAllB-int('10001010',2)):
        args[0] = absolutePath(args[0],os.getcwd())
        aPath = args[0].split(slh)

        n = 0
        for i in range(len(aPath)):
            if aPath[n] == ".":
                if len(aPath[n:]) > 1:
                    aPath[n:] = aPath[n+1:]
                else:
                    aPath.pop(-1)
            elif aPath[n] == "..":
                if n > 1 and len(aPath[n:]) > 1:
                    aPath[n-1:] = aPath[n+1:]
                    n -= 1
                elif n > 1 and len(aPath[n:]) <= 1: 
                    aPath.pop(-1)
                    aPath.pop(-1)
                    n -= 1
                else:
                    print("Invalid Source Path",args[0])
                    earlyError = True
                    break
            else:
                n += 1

        newdir = aPath.pop(-1)
        (validPath,tmpDir) = chkPath(aPath)
        sourcePath = tmpDir
        enteredArg = args[1]
        args[1] = absolutePath(args[1],os.getcwd())
        aPath2 = args[1].split(slh)

        n = 0
        for i in range(len(aPath2)):
            if aPath2[n] == ".":
                if len(aPath2[n:]) > 1:
                    aPath2[n:] = aPath2[n+1:]
                else:
                    aPath2.pop(-1)
            elif aPath2[n] == "..":
                if n > 1 and len(aPath2[n:]) > 1:
                    aPath2[n-1:] = aPath2[n+1:]
                    n -= 1
                elif n > 1 and len(aPath2[n:]) <= 1: 
                    aPath2.pop(-1)
                    aPath2.pop(-1)
                    n -= 1
                else:
                    print("Invalid Target Path",args[1])
                    earlyError = True
                    break
            else:
                n += 1

        newdir2 = aPath2.pop(-1)
        (validPath2,tmpDir) = chkPath(aPath2)
        targetPath = tmpDir

    # Check that first argument has a valid path, exists and (is not a directory file unless recursive copy)
        if not earlyError and validPath and ("*" in newdir or "?" in newdir or \
            (newdir in os.listdir(sourcePath) and (swBits & int('000010',2) or \
            os.stat(sourcePath+(slh if sourcePath[-1] != slh else "")+newdir)[0] & (2**15) != 0))):

            # Recursive copy from folder
            if newdir in os.listdir(sourcePath) and swBits & int('000010',2) and \
                os.stat(sourcePath+(slh if sourcePath[-1] != slh else "")+newdir)[0] & (2**15) == 0:

                aPath.append(newdir)
                newdir = "*"
                (validPath,tmpDir) = chkPath(aPath)
                sourcePath = tmpDir
                if not validPath:
                    print("Impossible Source Path Error")
                    earlyError = True
                    validPath2 = False

            # Recursive copy to a folder
            if newdir2 != ""  and swBits & int('000010',2) and \
                (newdir2 not in os.listdir(targetPath) or \
                (newdir2 in os.listdir(targetPath) and \
                os.stat(targetPath+(slh if targetPath[-1] != slh else "")+newdir2)[0] & (2**15) == 0)):

                if newdir2 != "*":
                    aPath2.append(newdir2)
                newdir2 = ""
                (validPath2,tmpDir) = chkPath(aPath2,True)
                targetPath = tmpDir
                if not validPath2:
                    print("Impossible Target Path Error")
                    earlyError = True
                    validPath2 = False

            if aPath == aPath2[:len(aPath)] and swBits & int('000010',2):
                print("Cannot perform a cyclic copy (source cannot contain target)")
                earlyError = True
                validPath2 = False
            elif aPath2 == aPath[:len(aPath2)] and swBits & int('000010',2):
                print("Cannot perform a cyclic copy (target cannot contain source)")
                earlyError = True
                validPath2 = False

            if "*" in newdir or "?" in newdir:
                wildCardOp = True
            else:
                wildCardOp = False

            if newdir2 == "*":
                newdir2 = ""
            if "*" in newdir2 or "?" in newdir2:
                validPath2 = False

    # Second argument has valid path
            if validPath2:
                if sourcePath == "" or sourcePath[-1] != slh:
                    sourcePath += slh
                if targetPath == "" or targetPath[-1] != slh:
                    targetPath += slh

                gc.collect()

    # Second argument specifies an existing target
                if newdir2 == "" or newdir2 in os.listdir(targetPath) or \
                    (targetPath == slh and newdir2 == ""):

    # Second argument target is a file
                    if os.stat(targetPath[:-1 if newdir2=="" else None]+newdir2)[0] & (2**15) != 0:
                        if trailingSlash:
                            print("Cannot find the specified path: ",enteredArg)
                        elif wildCardOp:
                            print("Target must be directory for wildcard copy ",enteredArg)
                        elif swBits & int('000010',2):
                            print("Target must be directory for recursive copy",enteredArg)

                        elif sourcePath == targetPath and newdir == newdir2:
                            print("The file cannot be copied onto itself")

                        elif swBits & int('001000',2) or input("Overwrite "+args[1]+"? (y/n): ").upper() == "Y":
                            os.remove(targetPath+(slh if targetPath[-1] != slh else "")+newdir2)
                            if filecpy(sourcePath+(slh if sourcePath[-1] != slh else "")+newdir,targetPath+(slh if targetPath[-1] != slh else "")+newdir2,bool(swBits&int('10000000'))):
                                nFiles += 1

    # Second argument target is a directory
                    else:
                        if wildCardOp or swBits & int('000010',2):
                            nFiles += multicpy(sourcePath,newdir,targetPath,newdir2,swBits)[0]
                        elif newdir in os.listdir(targetPath+newdir2):
                            if sourcePath == targetPath+newdir2+("" if newdir2 == "" else slh):
                                print("The file cannot be copied onto itself")
                            elif swBits & int('001000',2) or input("Overwrite "+targetPath+newdir2+("" if newdir2 == "" else slh)+newdir+"? (y/n): ").upper() == "Y":
                                os.remove(targetPath+newdir2+("" if newdir2 == "" else slh)+newdir)
                                if filecpy(sourcePath+newdir,targetPath+newdir2+("" if newdir2 == "" else slh)+newdir,bool(swBits&int('10000000'))):
                                    nFiles += 1
                        else:
                            if filecpy(sourcePath+newdir,targetPath+newdir2+("" if newdir2 == "" else slh)+newdir,bool(swBits&int('10000000'))):
                                nFiles += 1
    # Second argument is a new file
                else:
                    if trailingSlash or wildCardOp or swBits & int('000010',2):
                        if swBits & int('000010',2):
                            nFiles += multicpy(sourcePath,newdir,targetPath,newdir2,swBits)[0]
                        elif wildCardOp:
                            print("Target must be directory for wildcard copy ",enteredArg)
                        else:
                            print("Cannot find the specified path: ",enteredArg)
                    else:
                        if filecpy(sourcePath+(slh if sourcePath[-1] != slh else "")+newdir,targetPath+(slh if targetPath[-1] != slh else "")+newdir2,bool(swBits&int('10000000'))):
                            nFiles += 1

                print(" "*7,nFiles,"files(s) copied.")
            else:
                if not earlyError:
                    print("Invalid Target:",args[1])
        else:
            if not earlyError:
                if not validPath or newdir not in os.listdir(sourcePath):
                    print("No such file:",args[0])
                else:
                    print("The source file cannot be a directory")
    else:
        if swBits & (swAllB-int('10001010',2)):
            print("Illegal switch, Command Format: xcopy[/y][/s][/v] [path]file [path][file]")
        else:
            print("Wrong number of arguments")


if __name__ != "PyDOS":
    passedIn = input("Source File: ")
    passedIn = passedIn+" "+input("Destination Filename: ")
    envVars = {}
    envVars["_switches"] = (input("Command Switches: ").upper()).split("/")

xcopy()