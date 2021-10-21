try:
    from pydos_ui import input
except:
    pass
def run(runargv):
    cf = open(runargv)
    exec(cf.read())
    cf.close()

if __name__ != "PyDOS":
    passedIn = ""

if passedIn == "":
    passedIn = input("Enter python file to run: ")

runargv = passedIn
passedIn = ""
run(runargv)
