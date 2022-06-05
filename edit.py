##Created by Joseph Long 2016
##Modified to resemble DOS edlin by David Hunter 2021
##First python project
##Simple Text Editor

import os
import sys
try:
    from pydos_ui import input
except:
    pass

loaded = []
autosave = False
filename = ""
lineNum = 0

def chkPath(tstPath):
    validPath = True

    if tstPath == []:
        validPath = True
    else:

        savDir = os.getcwd()

        for path in tstPath:
            if path == "":
                os.chdir("/")

            elif os.getcwd() == "/" and path == "..":
                validPath = False
                break

            elif path == "." or path == "..":
                os.chdir(path)

            elif path in os.listdir() and (os.stat(path)[0] & (2**15) == 0):
                os.chdir(path)

            else:
                validPath = False
                break

        os.chdir(savDir)

    return(validPath)

def open_text(name):

    if name == "":
        name = input("Enter file name: ")

    aPath = name.split("/")
    newdir = aPath.pop(-1)

    text = []
    if chkPath(aPath) and newdir in os.listdir(name[0:len(name)-len(newdir)]) and os.stat(name)[0] & (2**15) != 0:
        f = open(name, "r")

        for line in f:
            text.append(line.replace("\n",""))

        f.close()
    else:
        print("Unable to open: "+name+". File not found.")
        name = ""

    return(name,text)

def proc_text(lineNum,func,strt,end,text):
    if len(text) > 0:
        x = min(max(0,strt),len(text)-1)
        popIndx = x
        staticEnd = max(0,min(end,len(text)-1))
        if x == staticEnd:
            lineNum = staticEnd
        while x <= staticEnd:
            if func == "L":
                if x == lineNum:
                    print("   *", x, text[x])
                else:
                    print("    ", x, text[x])
            elif func == "D":
                text.pop(popIndx)
                lineNum = popIndx
            x+=1

    return(lineNum,text)

def save_text(name,text):
    if name == "":
        name = input("Enter file name: ")

    f = open(name, "w")

    for line in text:
        f.write(line + "\n")

    f.close()

    return(name)

def parseInput(command):

    global parseMap

    cmdList = []
    parseMap = "C"
    cmdFound = False
    cnfrmFound = False
    buildingNum = False
    builtNum =""
    txtParam = ""
    for sChar in command:
        if not cmdFound:
            if sChar not in "0123456789,.+-$?":
                cmd = sChar.upper()
                cmdFound = True
                if buildingNum:
                    cmdList.append(int(builtNum))
                    buildingNum = False
                    builtNum = ""
                    parseMap += "-"
            elif sChar in "0123456789+-":
                builtNum += sChar
                buildingNum = True
            elif sChar == "?" and not cmdFound:
                if not cnfrmFound:
                    parseMap += sChar
                cnfrmFound = True
            else:
                if buildingNum:
                    cmdList.append(int(builtNum))
                    buildingNum = False
                    builtNum = ""
                    parseMap += "-"
        else:
            txtParam += sChar

    if txtParam != "":
        cmdList.append(txtParam.strip())
        parseMap += "+"

    if not cmdFound:
        if buildingNum:
            cmdList.append(int(builtNum))
            parseMap += "-"
            cmd = "*"
        else:
            cmd = "#"

    cmdList.insert(0,cmd)
    return cmdList

def interperit(command,text):
    global filename
    global autosave
    global lineNum
    global parseMap

    confirmCmd = False
    loop = True
    command_list = parseInput(command)
    #print (lineNum,command_list,parseMap)
    if "?" in parseMap:
        confirmCmd = True
        parseMap = parseMap.replace("?","")

    if command_list[0] == "O":
        if parseMap == "C+":
            (filename,text) = open_text(command_list[1])
        else:
            (filename,text) = open_text(filename)

    elif command_list[0] == "W":
        if parseMap == "C+":
            filename = save_text(command_list[1],text)
        else:
            filename = save_text(filename,text)

    elif command_list[0] == "E":
        if parseMap == "C+":
            filename = save_text(command_list[1],text)
        else:
            filename = save_text(filename,text)
        loop = False

    elif command_list[0] == "Q":
        loop = False

    elif command_list[0] == "autosave":
        if autosave:
            autosave = False
            print("\tAutosave disabled")
        else:
            autosave = True
            print("\tAutosave enabled")

    elif command_list[0] == "new":
        if len(command_list) > 1:
            filename = save_text(command_list[1][1:],text)
        else:
            filename = save_text(filename,text)

        text[:] = []

    elif command_list[0] == "H":
        print(" ")
        print(" ")
        print("h                      - DISPLAY COMMANDS")
        print("#                      - REPLACE A SINGLE LINE")
        print("[#][,#]d               - DELETE A BLOCK OF LINES")
        print("[#]i                   - INSERT")
        print("[#]a['str']            - APPEND LINES")
        print("[#][,#]l               - LIST LINES")
        print("[#][,#][?]r'str','str' - REPLACE STRING")
        print("[#][,#][?]s'str'       - SEARCH FOR STRING")
        print("o [filename]           - OPEN FILE")
        print("w [filename]           - WRITE FILE")
        print("e [filename]           - SAVE AND QUIT")
        print("q                      - QUIT")

    elif command_list[0] == "L" or command_list[0] == "D":
        if parseMap == "C-":
            (lineNum,text) = proc_text(lineNum,command_list[0],int(command_list[1]),int(command_list[1]),text)
        elif parseMap == "C--":
            (lineNum,text) = proc_text(lineNum,command_list[0],int(command_list[1]),int(command_list[2]),text)
        elif parseMap == "C":
            (lineNum,text) = proc_text(lineNum,command_list[0],0,len(text)-1,text)
        else:
            print("* Wrong command format. use: [#][,#]"+command_list[0].lower())

    elif command_list[0] == "I":
        if parseMap == "C-":
            text.insert(int(command_list[1]), input("."))
        elif parseMap == "C":
            text.insert(lineNum, input("."))
        else:
            print("* Wrong command format. use: [#]i")

    elif command_list[0] == "A":
        if parseMap == "C":
            text.append(input("."))
        elif parseMap == "C-":
            for a in range(0, int(command_list[1])):
                text.append(input("."))
        elif parseMap == "C+" or parseMap == "C-+":
            strngs = command_list[-1].strip()
            if strngs.count(strngs[0]) !=2:
                print("* Wrong command format. Use: [#]a 'str'")
            else:
                strngs = strngs.replace(strngs[0],"")
                if parseMap == "C+":
                    text.append(strngs)
                elif parseMap == "C-+":
                    for a in range(0, int(command_list[1])):
                        text.append(strngs)
        else:
            print("* Wrong command format, use: [#]a 'str'")


    elif command_list[0] == "find":
        for b in range(0, len(text)):
            if text[b].find(command_list[1][1:]) != -1:
                print("    ", b, text[b])

    elif command_list[0] == "R":
        strt = lineNum
        if parseMap == "C+":
            strt = lineNum
            end = lineNum
        elif parseMap == "C-+":
            strt = int(command_list[1])
            end = strt
        elif parseMap == "C--+":
            strt = int(command_list[1])
            end = int(command_list[2])
        else:
            print("* Wrong command format. Use: [#][,#][?]r 'str1','str2'")
            strt = -1

        if strt != -1:
            strngs = command_list[-1].strip()
            delim = strngs[0]
            if strngs.count(delim) != 4:
                print("* Wrong command format. Use: [#][,#][?]r 'str1','str2'")
            else:

                x = 0
                token = []
                delimFound = True
                for achar in strngs:
                    if achar == delim:
                        if delimFound:
                            strtTk = x+1
                        else:
                            endTk = x
                            token.append(strngs[strtTk:endTk])
                        delimFound = not delimFound
                    x += 1
                if confirmCmd:
                    print("for lines:",strt,"to",end,"- replace:",token[0],"with:",token[1],":")
                for b in range(strt, end+1):
                    if confirmCmd:
                        print(text[b].replace(token[0], token[1]))
                        if input("Confirm change (y/n): ")[0].upper() == "Y":
                            text[b] = text[b].replace(token[0], token[1])
                    else:
                        text[b] = text[b].replace(token[0], token[1])

    elif command_list[0] == "S":
        strt = lineNum
        if parseMap == "C+":
            strt = 0
            end = len(text) - 1
        elif parseMap == "C-+":
            strt = int(command_list[1])
            end = strt
        elif parseMap == "C--+":
            strt = int(command_list[1])
            end = int(command_list[2])
        else:
            print("* Wrong command format. Use: [#][,#][?]s 'str'")
            strt = -1

        if strt != -1:
            strngs = command_list[-1].strip()
            if strngs.count(strngs[0]) !=2:
                print("* Wrong command format. Use: [#][,#][?]s 'str'")
            else:
                strngs = strngs.replace(strngs[0],"")
                for b in range(strt, end+1):
                    if text[b].count(strngs) > 0:
                        lineNum = b
                        proc_text(lineNum,"L",b,b,text)
                        if not confirmCmd:
                            break
                        else:
                            if input("Confirm find (y/n): ")[0].upper() == "Y":
                                break

    elif command_list[0] == "load":
        try:
            f = open(command_list[1][1:] + ".py", "r")
            f.close
            loaded.append(command_list[1][1:])
        except: print("\tCouldn't load " + command_list[1] + ",\n\t\tPlugin does not exist")
        print(loaded)

    elif command_list[0] in "*#":
        if command_list[0] == "*":
            lineNum = min(len(text)-1,max(0,command_list[1]))
        proc_text(lineNum,"L",lineNum,lineNum,text)
        strngs = input(".")
        if strngs != "":
            text.insert(lineNum,strngs)
            if lineNum < len(text)-1:
                text.pop(lineNum+1)

        if lineNum < len(text):
            lineNum += 1

    elif command_list[0] in loaded:
        save_text("text.temp",text)
        args = " ".join(command_list[1:])
        os.system(".\\" + command_list[0] + ".py " + args)
        open("text.temp")
        os.remove("text.temp")

    return(loop,text)

def main(passedIn):
    global filename
    global autosave
    global lineNum
    global parseMap

    text = []

    if passedIn != "":
        (filename,text) = open_text(passedIn)

    print("h for command list")

    loop = True
    while loop:
        (loop,text) = interperit(input(filename+": "),text)
        #if autosave:
            #filename = save_text()

    del filename
    del autosave
    del lineNum
    del parseMap


if __name__ != "PyDOS":
    passedIn = ""

main(passedIn)
