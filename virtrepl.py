import os
try:
    from pydos_ui import input
except:
    pass
try:
    from codeop import compile_command
except:
    pass

__cmd = ""
while True:
    if 'compile_command' in dir():
# 9.0.0 alpha 7 or later supports multiple line statements
        __line = input(",,,     " if __cmd else "=>> " )

        if __cmd:
            __cmd += ("\n" + ("    " if __line != "" else "") + __line)
        else:
            if __line.lower() == 'exit':
                break
            __cmd = __line
        try:
            if compile_command(__cmd):
                exec(compile_command(__cmd))
                __cmd = ""
        except Exception as __err:
            print("*ERROR* Exception:",str(__err))
            __cmd = ""
    else:
# Pre 9.0.0 alpha 7 code (single line statments only)
        __line = input("=>> ")
        if __line.lower() == 'exit':
            break
        __result = None
        try:
            exec('__result='+__line)
        except:
            try:
                exec(__line)
            except Exception as err:
                print("*ERROR* Exception:",str(err))

        if __result != None and __line.find('=') == -1:
            print(__result)
