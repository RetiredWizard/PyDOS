#import _thread

#global threadLock
#threadLock = _thread.allocate_lock()

if __name__ != "PyDOS":
    passedIn = ""
    global envVars
    envVars = {}

if passedIn == "":
    passedIn = input("Enter python file to launch in thread: ")

cf = open(passedIn)

newF = "import _thread\n"
#newF += "from machine import Timer\nimport sys\n"

newF += "def runAsThread(passedIn):\n"

# Experimenting to see if timer interrupts can shutdown a thread
#     Doesn't seem so....

#newF += "    timer = Timer()\n"
#newF += "    def chkForLockClosure(timer):\n"
#newF += "        global threadLock\n"
#newF += "        if threadLock.locked():\n"
#newF += "            print('DeInit-ing Timer...')\n"
#newF += "            timer.deinit()\n"
#newF += "            print('Raising SystemExit...')\n"
#newF += "            raise SystemExit\n"
#newF += "            print('Executing sys.exit()...')\n"
#newF += "            sys.exit()\n"
#newF += "            print('Executing _thread.exit()...')\n"
#newF += "            _thread.exit()\n"
#newF += "    #timer.init(period=1000, mode=Timer.PERIODIC, callback=chkForLockClosure)\n"

line = " "
while line !="":
    line = cf.readline()
    newF += "    "+line
newF += "\n"
newF += "    if 'stopthread' in envVars.keys():\n"
newF += "        envVars.pop('stopthread')\n"

newF += "\n"
newF += "passedIn = envVars.get('passedIn','')\n"
newF += "envVars['stopthread'] = 'go'\n"
newF += "try:\n"
newF += "    _thread.start_new_thread(runAsThread,(passedIn,))\n"
newF += "except:\n"
newF += '    print("Thread failed, possible core in use")\n'
print(newF)
print('----------- OUTPUT --------------')
print('---------------------------------')
exec(newF)