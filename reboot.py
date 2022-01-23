import sys
if sys.implementation.name.upper() == "CIRCUITPYTHON":
    from supervisor import reload
    reload()
elif sys.implementation.name.upper() == "MICROPYTHON":
    sys.exit()