import sys
print("\nRestarting PyDOS....\n")
print("If PyDOS doesn't load, press Ctrl-D at the >>> REPL prompt")
print("==========================================================\n\n")
if sys.implementation.name.upper() == "CIRCUITPYTHON":
    from supervisor import reload
    reload()
elif sys.implementation.name.upper() == "MICROPYTHON":
    sys.exit()