# Developed by Scott Shawcroft (@tannewt) https://github.com/tannewt/basicpython
#
# This is an experiment to edit Python code like BASIC was edited.
# The idea is imagining this as the default mode on a Raspberry Pi 400
#
import os

if __name__ == "PyDOS":
    global envVars
    nCols = int((int(envVars["_scrWidth"])-1)/16)
else:
    nCols = 4

print("# Basic Python v0")

program = []
top = {}
no_ready = False

while True:
    if no_ready:
        line = input()
    else:
        line = input("READY.\n")
    lineno = None
    if " " in line:
        command, remainder = line.split(" ", 1)
        lineno = None
        try:
            lineno = int(command, 10)
        except ValueError:
            pass
    else:
        command = line
        remainder = ""
    no_ready = False
    if lineno is not None:
        if lineno < 1:
            print("Line must be 1+")
        else:
            if lineno >= len(program):
                program.extend([""] * (lineno - len(program)))
            program[lineno - 1] = remainder
            no_ready = True
    elif command.lower() == 'new':
        program.clear()
    elif command.lower() == 'dir':
        wideCount = 0
        for dir in os.listdir():
            if os.stat(dir)[0] & (2**15) == 0:
                if (wideCount % nCols) == 0:
                    print()
                wideCount += 1
                print(("<"+dir+">"+" "*(13-len(dir)))[:15]+" ",end="")

        for dir in os.listdir():
            if os.stat(dir)[0] & (2**15) != 0:
                if (wideCount % nCols) == 0:
                    print()
                wideCount += 1
                print((dir+" "*(15-len(dir)))[:15]+" ",end="")
        print()
    elif command.lower() == "del":
        if remainder.strip(" \"") != "":
            if remainder.strip(" \"") in os.listdir():
                os.remove(remainder.strip(" \""))
            else:
                print("Unable to delete: "+remainder.strip(" \"")+". File not found.")
        else:
            print("No file specified!")
    elif command.lower() == "list":
        for i, line in enumerate(program):
            if line:
                print(i+1, line)
    elif command.lower() == "run":
        isolated = {}
        try:
            exec("\n".join(program), isolated, isolated)
        except Exception as e:
            print(e)
    elif command.lower() == "save":
        filename = remainder.strip(" \"")
        with open(filename, "w") as f:
            f.write("\n".join(program))
    elif command.lower() == "load":
        filename = remainder.strip(" \"")
        with open(filename, "r") as f:
            program = f.readlines()
            program = [line.strip("\r\n") for line in program]
    elif command.lower() in ["exit","quit","dos"]:
        break
    else:
        try:
            exec(line, top, top)
        except Exception as e:
            print(e)
