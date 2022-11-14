@echo off
pexec from sys import implementation
pexec envVars["_implementation"] = implementation.name.upper()
if %_implementation% == MICROPYTHON goto micropython
if exist autoexec.bat copy/y autoexec.bat autoexec.sav
copy/y 3.aut autoexec.bat
runvm "PyBasic/PyBasic adventure-fast.pgm"
:micropython
cd /PyBasic
pexec import PyBasic
pexec PyBasic.main("adventure-fast.pgm")
cd /
menu.bat