import sys
try:
    from pydos_ui import input
except:
    pass

if sys.implementation.name.upper() == "CIRCUITPYTHON":
    from supervisor import reload
    startupfile = 'code'
else:
    startupfile = 'main'
    
import os

def runvm(runargv):
    def chkPath(tstPath):
        validPath = True
        simpPath = ""

        if tstPath != []:
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

    def pFmt(dPath,trailSlh=True):
        if dPath == "":
            return '/'
        elif dPath == '/':
            return dPath
        elif trailSlh:
            return dPath+('/' if dPath[-1]!='/' else "")
        else:
            return dPath[:(-1 if dPath[-1] == '/' else None)]

    args = runargv.split(" ")
    savDir = os.getcwd()
    args[0] = absolutePath(args[0],savDir)

    aPath = args[0].split("/")
    newdir = aPath.pop(-1)
    (validPath, tmpDir) = chkPath(aPath)
    if tmpDir == "" or tmpDir[-1] != "/":
        tmpDir += "/"

    if validPath:
        if newdir in os.listdir(pFmt(tmpDir,False)):
            if startupfile+'.py' in os.listdir('/'):
                if startupfile+'._PyD' in os.listdir('/'):
                    os.remove('/'+startupfile+'.py')
                os.rename('/'+startupfile+'.py','/'+startupfile+'._PyD')

            t = open('/'+startupfile+'.py','w')
            r = open(tmpDir+newdir,'r')

            if sys.implementation.name.upper() == "CIRCUITPYTHON":
                t.write('from supervisor import reload\n')
            elif sys.implementation.name.upper() == "MICROPYTHON":
                t.write('from sys import exit\n')
            t.write('import os\nos.chdir("'+tmpDir[:(-1 if tmpDir != "/" else None)]+'")\n')
            t.write("global passedIn\n")
            t.write("passedIn = '"+" ".join(args[1:])+"'\n")
            t.write("global envVars\n")
            t.write("envVars = {}\n")
            for _ in envVars:
                if _ != ".neopixel":
                    t.write("envVars['"+_+"']='"+str(envVars[_]).replace("'",chr(92)+"'")+"'\n")

            t.write("__name__ = 'PyDOS'\n")
            t.write(r.read())
            t.write("\nos.chdir('/')\n")
            t.write("os.remove('/"+startupfile+".py')\n")
            t.write("os.rename('/"+startupfile+"._PyD','/"+startupfile+".py')\n")
            t.write('print("\\n\\nIf PyDOS doesn'+"'"+'t start, press Ctrl-D at the >>> REPL prompt")\n')
            t.write('print("===========================================================\\n\\n")\n')
            if sys.implementation.name.upper() == "CIRCUITPYTHON":
                t.write('reload()\n')
            elif sys.implementation.name.upper() == "MICROPYTHON":
                t.write('exit()\n')

            t.close()
            r.close()

            #supervisor.set_next_code_file('/PyD-code.py',reload_on_success=True,reload_on_error=True)

            print("\n\nIf "+tmpDir+newdir+" doesn't start, press Ctrl-D at the >>> REPL prompt")
            print("======================================================"+len(tmpDir+newdir)*"="+"\n\n")
            if sys.implementation.name.upper() == "CIRCUITPYTHON":
                reload()
            elif sys.implementation.name.upper() == "MICROPYTHON":
                sys.exit()
        else:
            print("Invalid Python file: "+tmpDir+newdir)
    else:
        print("Invalid target path: "+args[0])

if __name__ != "PyDOS":
    passedIn = ""

if passedIn == "":
    passedIn = input("Python script to run: ")

runargv = passedIn
passedIn = ""

argline = runargv.split(" ")
runargv = argline[0]
if "." not in runargv:
    runargv = runargv + ".py"

if len(argline) > 1:
    runargv = runargv + " " + " ".join(argline[1:])

runvm(runargv)
